from colorama import Fore
from typing import List, Tuple, Type, Dict, Optional
import queue
import threading
import numpy as np
import torch
import time
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import librosa
import pyaudio

audio_queue = queue.Queue()
done = False

SUPPORTED_LANGUAGES = {
    "es": "Spanish",
    "fr": "French", 
    "zh": "Chinese",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "en": "English"
}

LANGUAGE_CODES = list(SUPPORTED_LANGUAGES.keys())

class AudioRecorder:
    """
    AudioRecorder is a class that records audio from the microphone and adds it to the audio queue.
    """
    def __init__(self, format: int = pyaudio.paInt16, channels: int = 1, rate: int = 4096, chunk: int = 8192, record_seconds: int = 5, verbose: bool = False):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.record_seconds = record_seconds
        self.verbose = verbose
        self.audio = pyaudio.PyAudio()
        self.thread = threading.Thread(target=self._record, daemon=True)

    def _record(self) -> None:
        """
        Record audio from the microphone and add it to the audio queue.
        """
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate,
                                 input=True, frames_per_buffer=self.chunk)
        if self.verbose:
            print(Fore.GREEN + "AudioRecorder: Started recording..." + Fore.RESET)

        while not done:
            frames = []
            for _ in range(0, int(self.rate / self.chunk * self.record_seconds)):
                try:
                    data = stream.read(self.chunk, exception_on_overflow=False)
                    frames.append(data)
                except Exception as e:
                    print(Fore.RED + f"AudioRecorder: Failed to read stream - {e}" + Fore.RESET)
            
            raw_data = b''.join(frames)
            audio_data = np.frombuffer(raw_data, dtype=np.int16)
            audio_queue.put((audio_data, self.rate))
            if self.verbose:
                print(Fore.GREEN + "AudioRecorder: Added audio chunk to queue" + Fore.RESET)

        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        if self.verbose:
            print(Fore.GREEN + "AudioRecorder: Stopped" + Fore.RESET)

    def start(self) -> None:
        """Start the recording thread."""
        self.thread.start()

    def join(self) -> None:
        """Wait for the recording thread to finish."""
        self.thread.join()

class Transcript:
    """
    Transcript is a class that transcribes audio from the audio queue and adds it to the transcript.
    Supports multilingual speech recognition with automatic language detection.
    """
    def __init__(self, language: Optional[str] = None):
        self.last_read = None
        self.language = language
        device = self.get_device()
        torch_dtype = torch.float16 if device == "cuda" else torch.float32
        model_id = "distil-whisper/distil-large-v3"
        
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, use_safetensors=True
        )
        model.to(device)
        processor = AutoProcessor.from_pretrained(model_id)
        
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=24,
            torch_dtype=torch_dtype,
            device=device,
        )
    
    def detect_language(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        """Detect the language of the audio input."""
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32) / np.iinfo(audio_data.dtype).max
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        if sample_rate != 16000:
            audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
        
        inputs = self.pipe.feature_extractor(audio_data, sampling_rate=16000, return_tensors="pt")
        input_features = inputs.input_features.to(self.pipe.device)
        
        with torch.no_grad():
            logits = self.pipe.model(input_features).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            detected_lang = self.pipe.tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        for lang_code in LANGUAGE_CODES:
            if lang_code in detected_lang.lower() or detected_lang.lower() in lang_code:
                return lang_code
        return "en"
    
    def get_device(self) -> str:
        if torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda:0"
        else:
            return "cpu"
        
    def remove_hallucinations(self, text: str) -> str:
        """Remove model hallucinations from the text."""
        # TODO find a better way to do this
        common_hallucinations = ['Okay.', 'Thank you.', 'Thank you for watching.', 'You\'re', 'Oh', 'you', 'Oh.', 'Uh', 'Oh,', 'Mh-hmm', 'Hmm.', 'going to.', 'not.']
        for hallucination in common_hallucinations:
            text = text.replace(hallucination, "")
        return text
    
    def transcript_job(self, audio_data: np.ndarray, sample_rate: int = 16000, language: Optional[str] = None) -> str:
        """Transcribe the audio data."""
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32) / np.iinfo(audio_data.dtype).max
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        if sample_rate != 16000:
            audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
        
        lang = language or self.language or "auto"
        
        if lang == "auto":
            lang = self.detect_language(audio_data, 16000)
        
        generate_kwargs = {}
        if lang in LANGUAGE_CODES:
            generate_kwargs["language"] = lang
        
        result = self.pipe(audio_data, generate_kwargs=generate_kwargs if generate_kwargs else None)
        return self.remove_hallucinations(result["text"])
    
class AudioTranscriber:
    """
    AudioTranscriber is a class that transcribes audio from the audio queue and adds it to the transcript.
    """
    def __init__(self, ai_name: str, verbose: bool = False, language: Optional[str] = None):
        self.verbose = verbose
        self.ai_name = ai_name
        self.language = language
        self.transcriptor = Transcript(language=language)
        self.thread = threading.Thread(target=self._transcribe, daemon=True)
        self.trigger_words = {
            'EN': [f"{self.ai_name}", "hello", "hi"],
            'FR': [f"{self.ai_name}", "bonjour", "salut"],
            'ZH': [f"{self.ai_name}", "你好", "hi"],
            'ES': [f"{self.ai_name}", "hola", "hi"],
            'DE': [f"{self.ai_name}", "hallo", "hi"],
            'IT': [f"{self.ai_name}", "ciao", "hi"],
            'PT': [f"{self.ai_name}", "olá", "hi"]
        }
        self.confirmation_words = {
            'EN': ["do it", "go ahead", "execute", "run", "start", "thanks", "would ya", "please", "okay?", "proceed", "continue", "go on", "do that", "go it", "do you understand?"],
            'FR': ["fais-le", "vas-y", "exécute", "lance", "commence", "merci", "tu veux bien", "s'il te plaît", "d'accord ?", "poursuis", "continue", "vas-y", "fais ça", "compris"],
            'ZH_CHT': ["做吧", "繼續", "執行", "運作看看", "開始", "謝謝", "可以嗎", "請", "好嗎", "進行", "做吧", "go", "do it", "執行吧", "懂了"],
            'ZH_SC': ["做吧", "继续", "执行", "运作看看", "开始", "谢谢", "可以吗", "请", "好吗", "运行", "做吧", "go", "do it", "执行吧", "懂了"],
            'ES': ["hazlo", "adelante", "ejecuta", "corre", "empieza", "gracias", "lo harías", "por favor", "¿vale?", "procede", "continúa", "sigue", "haz eso", "haz esa cosa"],
            'DE': ["mach es", "los", "ausführen", "starten", "beginnen", "danke", "bitte", "OK?", "fortfahren", "weiter", "mache das", "verstanden?"],
            'IT': ["fallo", "avanti", "esegui", "avvia", "inizia", "grazie", "per favore", "ok?", "procedi", "continua", "fa quello", "capito?"],
            'PT': ["faça", "em frente", "execute", "rode", "comece", "obrigado", "por favor", "ok?", "proceda", "continue", "faça isso", "entendeu?"]
        }
        self.recorded = ""

    def get_transcript(self) -> str:
        global done
        buffer = self.recorded
        self.recorded = ""
        done = False
        return buffer

    def _transcribe(self) -> None:
        """
        Transcribe the audio data using AI stt model.
        """
        global done
        if self.verbose:
            print(Fore.BLUE + "AudioTranscriber: Started processing..." + Fore.RESET)
        
        while not done or not audio_queue.empty():
            try:
                audio_data, sample_rate = audio_queue.get(timeout=1.0)
                
                start_time = time.time()
                text = self.transcriptor.transcript_job(audio_data, sample_rate, self.language)
                end_time = time.time()
                self.recorded += text
                print(Fore.YELLOW + f"Transcribed: {text} in {end_time - start_time} seconds" + Fore.RESET)
                for language, words in self.trigger_words.items():
                    if any(word in text.lower() for word in words):
                        print(Fore.GREEN + f"Listening again..." + Fore.RESET)
                        self.recorded = text
                for language, words in self.confirmation_words.items():
                    if any(word in text.lower() for word in words):
                        print(Fore.GREEN + f"Trigger detected. Sending to AI..." + Fore.RESET)
                        audio_queue.task_done()
                        done = True
                        break
            except queue.Empty:
                time.sleep(0.1)
                continue
            except Exception as e:
                print(Fore.RED + f"AudioTranscriber: Error - {e}" + Fore.RESET)
        if self.verbose:
            print(Fore.BLUE + "AudioTranscriber: Stopped" + Fore.RESET)

    def start(self):
        """Start the transcription thread."""
        self.thread.start()

    def join(self):
        """Wait for the transcription thread to finish."""
        self.thread.join()


if __name__ == "__main__":
    recorder = AudioRecorder(verbose=True)
    transcriber = AudioTranscriber(verbose=True, ai_name="jarvis")
    recorder.start()
    transcriber.start()
    recorder.join()
    transcriber.join()