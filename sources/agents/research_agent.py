from sources.agents.agent import Agent
from sources.tools.tools import Tools
from sources.tools.searxSearch import searxSearch
from sources.memory import Memory
from sources.utility import pretty_print
from sources.logger import Logger


class ResearchAgent(Agent):
    def __init__(self, name, prompt_path, provider, verbose=False, browser=None):
        super().__init__(name, prompt_path, provider, verbose, None)
        self.tools = {
            "web_search": searxSearch()
        }
        self.role = "research"
        self.type = "research_agent"
        self.memory = Memory(self.load_prompt(prompt_path),
                                recover_last_session=False,
                                memory_compression=False,
                                model_provider=provider.get_model_name())
        self.logger = Logger("research_agent.log")

    async def process(self, prompt, speech_module):
        """
        Process the research request by searching, parsing and synthesizing results.
        """
        self.status_message = "Researching..."
        self.logger.info(f"Starting research with prompt: {prompt}")
        
        self.memory.push('user', prompt)
        
        search_query = self._extract_search_query(prompt)
        if not search_query:
            search_query = prompt
            pretty_print("Using full prompt as search query", color="info")
        
        pretty_print(f"Searching for: {search_query}", color="status")
        
        search_results = self.tools["web_search"].execute([search_query])
        feedback = self.tools["web_search"].interpreter_feedback(search_results)
        
        if self.tools["web_search"].execution_failure_check(search_results):
            self.success = False
            return f"Research failed: {search_results}", ""
        
        self.memory.push('user', feedback)
        
        synthesize_prompt = f"""Based on the following search results, provide a structured synthesis of the information:

Search Query: {search_query}

Search Results:
{search_results}

Please provide:
1. A brief summary of key findings
2. Main sources with their URLs
3. Any relevant conclusions or insights

Format the response clearly."""
        
        answer, reasoning = await self.llm_request()
        
        self.last_answer = answer
        self.last_reasoning = reasoning
        
        pretty_print("Research completed", color="success")
        self.logger.info(f"Research completed successfully")
        
        return answer, reasoning

    def _extract_search_query(self, prompt: str) -> str:
        """
        Extract the search query from the user's prompt.
        """
        keywords = ["search", "find", "research", "look up", "information", "query", "buscar", "encontrar"]
        lower_prompt = prompt.lower()
        
        for keyword in keywords:
            if keyword in lower_prompt:
                idx = lower_prompt.find(keyword)
                query = prompt[idx + len(keyword):].strip()
                if query:
                    return query.strip('"\':,;')
        
        return ""