"""Base agent class for Social Agent workflow."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from semantic_kernel import Kernel
from semantic_kernel.services import AzureChatCompletion
from azure.identity import DefaultAzureCredential
import structlog

logger = structlog.get_logger(__name__)


class BaseAgent(ABC):
    """Base class for all agents in the social media workflow."""
    
    def __init__(
        self,
        name: str,
        endpoint: str,
        api_key: Optional[str] = None,
        deployment_name: str = "gpt-4",
        use_azure_identity: bool = False
    ):
        """Initialize the base agent.
        
        Args:
            name: Name of the agent
            endpoint: Azure AI endpoint
            api_key: Azure AI API key (if not using Azure Identity)
            deployment_name: Azure AI deployment name
            use_azure_identity: Whether to use Azure Identity for authentication
        """
        self.name = name
        self.kernel = Kernel()
        
        # Set up Azure Chat Completion service
        if use_azure_identity:
            credential = DefaultAzureCredential()
            chat_service = AzureChatCompletion(
                service_id=f"{name}_chat",
                endpoint=endpoint,
                deployment_name=deployment_name,
                ad_token_provider=credential
            )
        else:
            chat_service = AzureChatCompletion(
                service_id=f"{name}_chat",
                endpoint=endpoint,
                api_key=api_key,
                deployment_name=deployment_name
            )
        
        self.kernel.add_service(chat_service)
        logger.info(f"Initialized {self.name} agent")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results.
        
        Args:
            input_data: Dictionary containing input data for the agent
            
        Returns:
            Dictionary containing the agent's output
        """
        pass
    
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        pass
    
    async def _invoke_llm(self, user_prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Invoke the LLM with the agent's system prompt and user input.
        
        Args:
            user_prompt: The user's prompt
            context: Optional context data
            
        Returns:
            The LLM's response
        """
        try:
            # Prepare the full prompt
            full_prompt = f"{self.system_prompt}\n\nUser Input: {user_prompt}"
            if context:
                full_prompt += f"\n\nContext: {context}"
            
            # Get the chat completion service
            chat_service = self.kernel.get_service(f"{self.name}_chat")
            
            # Invoke the service
            response = await chat_service.get_chat_message_content(
                chat_history=[],
                settings={"messages": [{"role": "user", "content": full_prompt}]}
            )
            
            return str(response)
        
        except Exception as e:
            logger.error(f"Error invoking LLM for {self.name}: {e}")
            raise