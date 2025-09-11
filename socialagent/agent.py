"""
LinkedIn Content Generator Agent
"""

import os
from typing import Dict, List, Optional

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.functions.kernel_function import KernelFunction
from semantic_kernel.functions.kernel_function_metadata import KernelFunctionMetadata


class LinkedInContentAgent:
    """
    A Semantic Kernel agent that generates LinkedIn content based on user input.
    """

    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model_id: Optional[str] = None,
                 use_azure: bool = True,
                 azure_endpoint: Optional[str] = None,
                 azure_deployment: Optional[str] = None):
        """
        Initialize the LinkedIn Content Agent.

        Args:
            api_key (Optional[str]): API key. If not provided, will try to use environment variable.
            model_id (Optional[str]): The model ID to use for content generation.
            use_azure (bool): Whether to use Azure OpenAI or direct OpenAI.
            azure_endpoint (Optional[str]): Azure OpenAI endpoint URL.
            azure_deployment (Optional[str]): Azure OpenAI deployment name.
        """
        # Get configuration from environment if not provided
        if api_key is None:
            api_key = os.environ.get("AZURE_OPENAI_API_KEY" if use_azure else "OPENAI_API_KEY")
            # Strip any quotes that might be in the environment variable
            if api_key and (api_key.startswith('"') and api_key.endswith('"') or 
                           api_key.startswith("'") and api_key.endswith("'")):
                api_key = api_key[1:-1]
                
            if api_key is None:
                raise ValueError(
                    f"{'Azure OpenAI' if use_azure else 'OpenAI'} API key is required. "
                    f"Either pass it directly or set the {'AZURE_OPENAI_API_KEY' if use_azure else 'OPENAI_API_KEY'} environment variable."
                )
        
        if model_id is None:
            model_id = os.environ.get("AZURE_OPENAI_MODEL" if use_azure else "OPENAI_MODEL", "gpt-4")
        
        if use_azure:
            if azure_endpoint is None:
                azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
                if azure_endpoint is None:
                    raise ValueError(
                        "Azure OpenAI endpoint URL is required. Either pass it directly or set the AZURE_OPENAI_ENDPOINT environment variable."
                    )
            
            if azure_deployment is None:
                azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", model_id)

        # Initialize the kernel
        self.kernel = sk.Kernel()
        
        # Add the appropriate chat completion service
        if use_azure:
            self.kernel.add_service(
                AzureChatCompletion(
                    service_id="azure_openai",
                    deployment_name=azure_deployment,
                    endpoint=azure_endpoint,
                    api_key=api_key
                )
            )
            self.service_id = "azure_openai"
        else:
            self.kernel.add_service(
                OpenAIChatCompletion(
                    service_id="openai", 
                    ai_model_id=model_id, 
                    api_key=api_key
                )
            )
            self.service_id = "openai"
        
        # Register the content generation functions
        self._register_functions()

    def _register_functions(self):
        """Register semantic functions for content generation."""
        # Create a function for generating LinkedIn post content
        generate_post_function = self.kernel.create_function_from_prompt(
            function_name="generate_linkedin_post",
            plugin_name="linkedin_content",
            description="Generates a professional LinkedIn post about a specific topic.",
            prompt="""
            You are an expert LinkedIn content creator who helps professionals craft engaging posts
            that drive engagement and establish thought leadership.
            
            Create a professional LinkedIn post about the following topic: {{$topic}}
            
            Target audience: {{$audience}}
            Tone: {{$tone}}
            Include hashtags: {{$include_hashtags}}
            Post length: {{$length}}
            
            The post should be well-structured, professional, and engage the target audience effectively.
            If hashtags are requested, include 3-5 relevant hashtags at the end of the post.
            """,
            execution_settings={
                self.service_id: {
                    "temperature": 0.7,
                    "top_p": 1.0,
                    "max_tokens": 1000
                }
            }
        )
        
        # Create a function for generating a content series plan
        generate_series_function = self.kernel.create_function_from_prompt(
            function_name="generate_content_series",
            plugin_name="linkedin_content",
            description="Generates a series of LinkedIn post ideas based on a main topic.",
            prompt="""
            You are an expert LinkedIn content strategist who helps professionals plan engaging content series
            that establish thought leadership and provide value to their network.
            
            Create a content series plan of {{$number_of_posts}} LinkedIn posts around the main topic: {{$main_topic}}
            
            Target audience: {{$audience}}
            Content goal: {{$content_goal}}
            
            For each post in the series, provide:
            1. A catchy headline
            2. The main points to cover (3-5 bullet points)
            3. A suggested call-to-action
            4. 3-5 relevant hashtags
            
            Make sure the series has a logical flow, with each post building on previous ones while still being valuable as standalone content.
            """,
            execution_settings={
                self.service_id: {
                    "temperature": 0.7,
                    "top_p": 1.0,
                    "max_tokens": 2000
                }
            }
        )
        
        # Create a function for analyzing post performance
        analyze_post_function = self.kernel.create_function_from_prompt(
            function_name="analyze_post",
            plugin_name="linkedin_content",
            description="Analyzes a LinkedIn post and provides feedback for improvement.",
            prompt="""
            You are an expert LinkedIn content analyst who helps professionals improve their posts
            for better engagement and impact.
            
            Analyze the following LinkedIn post and provide detailed feedback:
            
            POST:
            {{$post_content}}
            
            In your analysis, cover:
            1. Overall impression and impact
            2. Clarity and structure of the message
            3. Engagement potential
            4. Use of hashtags (if any)
            5. Call-to-action effectiveness
            6. Specific suggestions for improvement
            
            Be constructive and specific in your feedback, highlighting both strengths and areas for improvement.
            """,
            execution_settings={
                self.service_id: {
                    "temperature": 0.5,
                    "top_p": 1.0,
                    "max_tokens": 1500
                }
            }
        )

    async def generate_linkedin_post(
        self, 
        topic: str, 
        audience: str = "professionals", 
        tone: str = "professional",
        include_hashtags: bool = True,
        length: str = "medium"
    ) -> str:
        """
        Generate a LinkedIn post about a specific topic.
        
        Args:
            topic (str): The main topic of the LinkedIn post.
            audience (str): The target audience for the post.
            tone (str): The tone of the post (professional, conversational, inspirational, etc.).
            include_hashtags (bool): Whether to include hashtags at the end of the post.
            length (str): The desired length of the post (short, medium, long).
            
        Returns:
            str: The generated LinkedIn post.
        """
        # Get the LinkedIn post generation function
        generate_post = self.kernel.functions.get_function("linkedin_content", "generate_linkedin_post")
        
        # Set the arguments for the function
        context_variables = sk.ContextVariables()
        context_variables["topic"] = topic
        context_variables["audience"] = audience
        context_variables["tone"] = tone
        context_variables["include_hashtags"] = "yes" if include_hashtags else "no"
        context_variables["length"] = length
        
        # Invoke the function
        result = await self.kernel.invoke(generate_post, variables=context_variables)
        return str(result)

    async def generate_content_series(
        self, 
        main_topic: str, 
        number_of_posts: int = 5,
        audience: str = "professionals",
        content_goal: str = "establish thought leadership"
    ) -> str:
        """
        Generate a series of LinkedIn post ideas based on a main topic.
        
        Args:
            main_topic (str): The main topic for the content series.
            number_of_posts (int): The number of posts to include in the series.
            audience (str): The target audience for the posts.
            content_goal (str): The goal of the content series.
            
        Returns:
            str: The generated content series plan.
        """
        # Get the content series generation function
        generate_series = self.kernel.functions.get_function("linkedin_content", "generate_content_series")
        
        # Set the arguments for the function
        context_variables = sk.ContextVariables()
        context_variables["main_topic"] = main_topic
        context_variables["number_of_posts"] = str(number_of_posts)
        context_variables["audience"] = audience
        context_variables["content_goal"] = content_goal
        
        # Invoke the function
        result = await self.kernel.invoke(generate_series, variables=context_variables)
        return str(result)

    async def analyze_post(self, post_content: str) -> str:
        """
        Analyze a LinkedIn post and provide feedback for improvement.
        
        Args:
            post_content (str): The content of the LinkedIn post to analyze.
            
        Returns:
            str: Analysis and feedback for the post.
        """
        # Get the post analysis function
        analyze_post = self.kernel.functions.get_function("linkedin_content", "analyze_post")
        
        # Set the arguments for the function
        context_variables = sk.ContextVariables()
        context_variables["post_content"] = post_content
        
        # Invoke the function
        result = await self.kernel.invoke(analyze_post, variables=context_variables)
        return str(result)
