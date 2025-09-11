"""
Tests for the LinkedIn Content Generator Agent.
"""

import os
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import asyncio

class TestLinkedInContentAgent(unittest.TestCase):
    """Tests for the LinkedInContentAgent class."""
    
    @patch('semantic_kernel.Kernel')
    def test_agent_initialization(self, mock_kernel):
        """Test that the agent initializes correctly."""
        from socialagent.agent import LinkedInContentAgent
        
        # Setup
        os.environ["OPENAI_API_KEY"] = "test-api-key"
        
        # Execute
        agent = LinkedInContentAgent()
        
        # Assert
        self.assertIsNotNone(agent)
        mock_kernel.assert_called_once()

    @patch('semantic_kernel.Kernel')
    @patch('semantic_kernel.functions.KernelFunction')
    def test_generate_linkedin_post(self, mock_function, mock_kernel):
        """Test generating a LinkedIn post."""
        from socialagent.agent import LinkedInContentAgent
        
        # Setup
        os.environ["OPENAI_API_KEY"] = "test-api-key"
        
        mock_kernel_instance = mock_kernel.return_value
        mock_kernel_instance.functions.get_function.return_value = MagicMock()
        mock_kernel_instance.invoke = AsyncMock(return_value="Generated LinkedIn post")
        
        # Execute
        agent = LinkedInContentAgent()
        
        # Run the async function in the test
        result = asyncio.run(agent.generate_linkedin_post(
            topic="Test topic",
            audience="Test audience",
            tone="professional",
            include_hashtags=True,
            length="medium"
        ))
        
        # Assert
        self.assertEqual(result, "Generated LinkedIn post")
        mock_kernel_instance.functions.get_function.assert_called_once_with(
            "linkedin_content", "generate_linkedin_post"
        )


if __name__ == "__main__":
    unittest.main()
