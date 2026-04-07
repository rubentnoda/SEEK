import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestPlannerAgentParsing(unittest.TestCase):
    def test_get_task_names_with_hashes(self):
        from sources.agents.planner_agent import PlannerAgent
        
        class MockProvider:
            def get_model_name(self):
                return "test"
            async def generate(self, *args, **kwargs):
                return "", ""
        
        planner = PlannerAgent("test", None, MockProvider(), verbose=False)
        
        text = """## Task 1: Search the web
## Task 2: Write code
## Task 3: Analyze results"""
        
        result = planner.get_task_names(text)
        self.assertEqual(len(result), 3)
        self.assertIn("## Task 1: Search the web", result)
        
    def test_get_task_names_with_digits(self):
        from sources.agents.planner_agent import PlannerAgent
        
        class MockProvider:
            def get_model_name(self):
                return "test"
            async def generate(self, *args, **kwargs):
                return "", ""
        
        planner = PlannerAgent("test", None, MockProvider(), verbose=False)
        
        text = """1. First task
2. Second task
3. Third task"""
        
        result = planner.get_task_names(text)
        self.assertEqual(len(result), 3)
        
    def test_get_task_names_mixed(self):
        from sources.agents.planner_agent import PlannerAgent
        
        class MockProvider:
            def get_model_name(self):
                return "test"
            async def generate(self, *args, **kwargs):
                return "", ""
        
        planner = PlannerAgent("test", None, MockProvider(), verbose=False)
        
        text = """## Search task
Just a regular line
1. Second task
Another regular line"""
        
        result = planner.get_task_names(text)
        self.assertEqual(len(result), 2)
        
    def test_get_task_names_empty(self):
        from sources.agents.planner_agent import PlannerAgent
        
        class MockProvider:
            def get_model_name(self):
                return "test"
            async def generate(self, *args, **kwargs):
                return "", ""
        
        planner = PlannerAgent("test", None, MockProvider(), verbose=False)
        
        text = """Just regular lines
No task markers here"""
        
        result = planner.get_task_names(text)
        self.assertEqual(len(result), 0)
        
    def test_make_prompt_without_infos(self):
        from sources.agents.planner_agent import PlannerAgent
        
        class MockProvider:
            def get_model_name(self):
                return "test"
            async def generate(self, *args, **kwargs):
                return "", ""
        
        planner = PlannerAgent("test", None, MockProvider(), verbose=False)
        
        result = planner.make_prompt("Test task", None)
        self.assertIn("Test task", result)
        self.assertIn("No needed informations", result)
        
    def test_make_prompt_with_infos(self):
        from sources.agents.planner_agent import PlannerAgent
        
        class MockProvider:
            def get_model_name(self):
                return "test"
            async def generate(self, *args, **kwargs):
                return "", ""
        
        planner = PlannerAgent("test", None, MockProvider(), verbose=False)
        
        infos = {"agent1": "Found some info", "agent2": "More data"}
        result = planner.make_prompt("Test task", infos)
        self.assertIn("Test task", result)
        self.assertIn("agent1", result)
        
    def test_show_plan_empty(self):
        from sources.agents.planner_agent import PlannerAgent
        from io import StringIO
        import sys as sys_mod
        
        class MockProvider:
            def get_model_name(self):
                return "test"
            async def generate(self, *args, **kwargs):
                return "", ""
        
        planner = PlannerAgent("test", None, MockProvider(), verbose=False)
        
        old_stdout = sys_mod.stdout
        sys_mod.stdout = StringIO()
        planner.show_plan([], "No plan")
        output = sys_mod.stdout.getvalue()
        sys_mod.stdout = old_stdout
        
        self.assertIn("Failed to make a plan", output)


if __name__ == '__main__':
    unittest.main()