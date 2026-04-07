import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestRouterFunctions(unittest.TestCase):
    def test_find_first_sentence(self):
        from sources.router import AgentRouter
        
        agents = []
        router = AgentRouter(agents)
        
        text1 = "Hello\nHow are you?"
        result1 = router.find_first_sentence(text1)
        self.assertEqual(result1, "Hello")
        
        text2 = "Only one line"
        result2 = router.find_first_sentence(text2)
        self.assertEqual(result2, "Only one line")
        
        text3 = "\n\n   \n   spaces"
        result3 = router.find_first_sentence(text3)
        self.assertEqual(result3.strip(), "spaces")
        
        text4 = ""
        result4 = router.find_first_sentence(text4)
        self.assertEqual(result4, "")

    def test_estimate_complexity_high_confidence(self):
        from sources.router import AgentRouter
        
        agents = []
        router = AgentRouter(agents)
        
        result = router.estimate_complexity("Find the latest research papers on AI and build save in a file")
        self.assertIn(result, ["HIGH", "LOW"])

    def test_estimate_complexity_low_task(self):
        from sources.router import AgentRouter
        
        agents = []
        router = AgentRouter(agents)
        
        result = router.estimate_complexity("hi")
        self.assertIn(result, ["HIGH", "LOW"])

    def test_router_vote_short_text(self):
        from sources.router import AgentRouter
        
        agents = []
        router = AgentRouter(agents)
        
        result = router.router_vote("hi", ["talk", "web", "code"])
        self.assertEqual(result, "talk")

    def test_select_agent_single_agent(self):
        from sources.agents.casual_agent import CasualAgent
        from sources.router import AgentRouter
        
        agent = CasualAgent("test", None, None)
        router = AgentRouter([agent])
        
        result = router.select_agent("Hello")
        self.assertEqual(result, agent)


if __name__ == '__main__':
    unittest.main()
