"""
LinkedIn Content Generator Agent
"""

import os
from typing import Dict, List, Optional

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.functions.kernel_function import KernelFunction
from semantic_kernel.functions.kernel_function_metadata import KernelFunctionMetadata
from semantic_kernel.functions import KernelPlugin, KernelFunctionFromPrompt
from semantic_kernel.functions.kernel_arguments import KernelArguments


class LinkedInContentAgent:
    """
    A Semantic Kernel agent that generates LinkedIn content based on user input.
    """

    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model_id: Optional[str] = None,
                 use_azure: bool = True,
                 azure_endpoint: Optional[str] = None,
                 azure_deployment: Optional[str] = None,
                 personal_style: Optional[str] = None):
        """
        Initialize the LinkedIn Content Agent.

        Args:
            api_key (Optional[str]): API key. If not provided, will try to use environment variable.
            model_id (Optional[str]): The model ID to use for content generation.
            use_azure (bool): Whether to use Azure OpenAI or direct OpenAI.
            azure_endpoint (Optional[str]): Azure OpenAI endpoint URL.
            azure_deployment (Optional[str]): Azure OpenAI deployment name.
            personal_style (Optional[str]): Your personal writing style preferences. If provided,
                                            this will override the default style guidelines.
        """
        # Store personal style preferences
        self.personal_style = personal_style or """
        - Write in a concise, clear, and direct style
        - Use a conversational and approachable tone that still maintains professionalism
        - Include occasional personal anecdotes or experiences when relevant
        - Ask thoughtful questions to engage the audience
        - Use bullet points for clarity when listing information
        - Add a touch of humor when appropriate
        - Balance technical expertise with accessibility
        - Avoid jargon unless necessary for the target audience
        - Use a mix of short and medium-length sentences for rhythm
        - End with a clear call to action or thought-provoking question
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
        # Plugin name for all LinkedIn functions
        plugin_name = "linkedin_content"
        
        # Create a function for generating LinkedIn post content
        linkedin_post_prompt = f"""
        You are an expert LinkedIn content creator who helps professionals craft engaging posts
        that drive engagement and establish thought leadership.
        
        Create a professional LinkedIn post about the following topic: {{{{$topic}}}}
        
        Target audience: {{{{$audience}}}}
        Tone: {{{{$tone}}}}
        Include hashtags: {{{{$include_hashtags}}}}
        Post length: {{{{$length}}}}
        
        Writing Style Guidelines:
        {self.personal_style}
        
        The post should be well-structured, professional, and engage the target audience effectively.
        If hashtags are requested, include 3-5 relevant hashtags at the end of the post.
        """
        
        # Add the function directly to the kernel
        self.kernel.add_function(
            function_name="generate_linkedin_post",
            plugin_name=plugin_name,
            description="Generates a professional LinkedIn post about a specific topic.",
            prompt=linkedin_post_prompt,
            prompt_execution_settings={
                self.service_id: {
                    "temperature": 0.7,
                    "top_p": 1.0,
                    "max_tokens": 1000
                }
            }
        )
        
        # Create a function for generating a content series plan
        series_prompt = f"""
        You are an expert LinkedIn content strategist who helps professionals plan engaging content series
        that establish thought leadership and provide value to their network.
        
        Create a content series plan of {{{{$number_of_posts}}}} LinkedIn posts around the main topic: {{{{$main_topic}}}}
        
        Target audience: {{{{$audience}}}}
        Content goal: {{{{$content_goal}}}}
        
        Writing Style Guidelines:
        {self.personal_style}
        
        For each post in the series, provide:
        1. A catchy headline
        2. The main points to cover (3-5 bullet points)
        3. A suggested call-to-action
        4. 3-5 relevant hashtags
        
        Make sure the series has a logical flow, with each post building on previous ones while still being valuable as standalone content.
        """
        
        # Add the function directly to the kernel
        self.kernel.add_function(
            function_name="generate_content_series",
            plugin_name=plugin_name,
            description="Generates a series of LinkedIn post ideas based on a main topic.",
            prompt=series_prompt,
            prompt_execution_settings={
                self.service_id: {
                    "temperature": 0.7,
                    "top_p": 1.0,
                    "max_tokens": 2000
                }
            }
        )
        
        # Create a function for analyzing post performance
        analyze_prompt = f"""
        You are an expert LinkedIn content analyst who helps professionals improve their posts
        for better engagement and impact.
        
        Analyze the following LinkedIn post and provide detailed feedback:
        
        POST:
        {{{{$post_content}}}}
        
        Writing Style Guidelines:
        {self.personal_style}
        
        In your analysis, cover:
        1. Overall impression and impact
        2. Clarity and structure of the message
        3. Engagement potential
        4. Use of hashtags (if any)
        5. Call-to-action effectiveness
        6. Specific suggestions for improvement
        
        Be constructive and specific in your feedback, highlighting both strengths and areas for improvement.
        Also provide an example of how to improve the post based on your feedback, maintaining the original topic and intent but enhancing the style and engagement.
        """
        
        # Add the function directly to the kernel
        self.kernel.add_function(
            function_name="analyze_post",
            plugin_name=plugin_name,
            description="Analyzes a LinkedIn post and provides feedback for improvement.",
            prompt=analyze_prompt,
            prompt_execution_settings={
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
        linkedin_plugin = self.kernel.get_plugin("linkedin_content")
        generate_post = linkedin_plugin["generate_linkedin_post"]
        
        # Set the arguments for the function
        arguments = KernelArguments(
            topic=topic,
            audience=audience,
            tone=tone,
            include_hashtags="yes" if include_hashtags else "no",
            length=length
        )
        
        # Invoke the function
        result = await self.kernel.invoke(generate_post, arguments=arguments)
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
        linkedin_plugin = self.kernel.get_plugin("linkedin_content")
        generate_series = linkedin_plugin["generate_content_series"]
        
        # Set the arguments for the function
        arguments = KernelArguments(
            main_topic=main_topic,
            number_of_posts=str(number_of_posts),
            audience=audience,
            content_goal=content_goal
        )
        
        # Invoke the function
        result = await self.kernel.invoke(generate_series, arguments=arguments)
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
        linkedin_plugin = self.kernel.get_plugin("linkedin_content")
        analyze_post = linkedin_plugin["analyze_post"]
        
        # Set the arguments for the function
        arguments = KernelArguments(
            post_content=post_content
        )
        
        # Invoke the function
        result = await self.kernel.invoke(analyze_post, arguments=arguments)
        return str(result)
