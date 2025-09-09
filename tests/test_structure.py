"""Basic tests for Social Agent project structure."""

import sys
import unittest
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestProjectStructure(unittest.TestCase):
    """Test that the project structure is valid."""
    
    def test_package_import(self):
        """Test that the main package can be imported."""
        try:
            import social_agent
            self.assertTrue(hasattr(social_agent, '__version__'))
            self.assertTrue(hasattr(social_agent, '__author__'))
        except ImportError as e:
            self.fail(f"Failed to import social_agent package: {e}")
    
    def test_agent_classes_exist(self):
        """Test that all agent classes can be imported."""
        try:
            from social_agent.agents.researcher import ResearcherAgent
            from social_agent.agents.copywriter import CopywriterAgent
            from social_agent.agents.manager import ManagerAgent
            from social_agent.agents.reviewer import ReviewerAgent
            
            # Check that classes inherit from BaseAgent
            from social_agent.agents import BaseAgent
            
            self.assertTrue(issubclass(ResearcherAgent, BaseAgent))
            self.assertTrue(issubclass(CopywriterAgent, BaseAgent))
            self.assertTrue(issubclass(ManagerAgent, BaseAgent))
            self.assertTrue(issubclass(ReviewerAgent, BaseAgent))
            
        except ImportError as e:
            self.fail(f"Failed to import agent classes: {e}")
    
    def test_workflow_import(self):
        """Test that the workflow orchestrator can be imported."""
        try:
            from social_agent.workflow import SocialMediaWorkflow
            self.assertTrue(callable(SocialMediaWorkflow))
        except ImportError as e:
            self.fail(f"Failed to import workflow: {e}")
    
    def test_agent_abstract_methods(self):
        """Test that agents implement required abstract methods."""
        from social_agent.agents.researcher import ResearcherAgent
        from social_agent.agents.copywriter import CopywriterAgent
        from social_agent.agents.manager import ManagerAgent
        from social_agent.agents.reviewer import ReviewerAgent
        
        agents = [ResearcherAgent, CopywriterAgent, ManagerAgent, ReviewerAgent]
        
        for agent_class in agents:
            # Check that required methods exist
            self.assertTrue(hasattr(agent_class, 'process'))
            self.assertTrue(hasattr(agent_class, 'system_prompt'))
            
            # Check that system_prompt is a property
            self.assertIsInstance(agent_class.system_prompt, property)


class TestConfiguration(unittest.TestCase):
    """Test configuration management."""
    
    def test_settings_import(self):
        """Test that settings can be imported."""
        try:
            from social_agent.config import settings, Settings
            self.assertIsNotNone(settings)
            self.assertTrue(callable(Settings))
        except ImportError as e:
            self.fail(f"Failed to import settings: {e}")


class TestFileStructure(unittest.TestCase):
    """Test that required files exist."""
    
    def setUp(self):
        self.project_root = Path(__file__).parent.parent
    
    def test_required_files_exist(self):
        """Test that all required project files exist."""
        required_files = [
            "README.md",
            "LICENSE", 
            "requirements.txt",
            ".gitignore",
            ".env.example",
            "setup.py",
            "example.py",
            "src/social_agent/__init__.py",
            "src/social_agent/main.py",
            "src/social_agent/config/__init__.py",
            "src/social_agent/config/settings.py",
            "src/social_agent/agents/__init__.py",
            "src/social_agent/agents/researcher.py",
            "src/social_agent/agents/copywriter.py",
            "src/social_agent/agents/manager.py",
            "src/social_agent/agents/reviewer.py",
            "src/social_agent/workflow/__init__.py",
            "src/social_agent/workflow/orchestrator.py"
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            self.assertTrue(full_path.exists(), f"Required file {file_path} does not exist")


if __name__ == "__main__":
    unittest.main()