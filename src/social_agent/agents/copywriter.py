"""Social Media Editor/Copywriter agent for content creation."""

from typing import Dict, Any
from . import BaseAgent
import structlog

logger = structlog.get_logger(__name__)


class CopywriterAgent(BaseAgent):
    """Agent responsible for creating engaging social media content."""
    
    @property
    def system_prompt(self) -> str:
        return """You are an expert social media copywriter and content creator. Your role is to:

1. Create compelling, engaging social media posts
2. Adapt content for different platforms and audiences
3. Write attention-grabbing headlines and captions
4. Incorporate trends and insights into content
5. Ensure content is brand-appropriate and authentic
6. Create call-to-actions that drive engagement
7. Optimize content length for each platform

Your content should be:
- Engaging and conversational
- Platform-optimized
- Trend-aware
- Authentic and relatable
- Action-oriented
- Visually descriptive when needed

Consider platform-specific best practices:
- Twitter: Concise, witty, hashtag-optimized
- LinkedIn: Professional, thought-leadership focused
- Instagram: Visual-first, story-driven
- Facebook: Community-focused, shareable
- TikTok: Trendy, entertaining, discovery-focused

Always include relevant hashtags and suggest visual elements when appropriate."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create social media content based on research insights.
        
        Args:
            input_data: Dictionary containing:
                - research_insights: Research data from researcher agent
                - content_type: Type of content to create
                - platform: Target social media platform
                - tone: Desired tone (professional, casual, humorous, etc.)
                - call_to_action: Desired action from audience
        
        Returns:
            Dictionary containing created content
        """
        try:
            logger.info(f"{self.name} creating content", platform=input_data.get('platform'))
            
            # Extract inputs
            research_insights = input_data.get('research_insights', '')
            content_type = input_data.get('content_type', 'general post')
            platform = input_data.get('platform', 'Instagram')
            tone = input_data.get('tone', 'engaging and professional')
            call_to_action = input_data.get('call_to_action', 'engage with the content')
            topic = input_data.get('topic', '')
            
            prompt = f"""
            Based on the following research insights, create compelling social media content:
            
            Research Insights: {research_insights}
            
            Content Requirements:
            - Platform: {platform}
            - Content Type: {content_type}
            - Topic: {topic}
            - Tone: {tone}
            - Call to Action: {call_to_action}
            
            Please create:
            1. Main post content (optimized for {platform})
            2. Engaging headline/caption
            3. Relevant hashtags
            4. Suggested visual elements or descriptions
            5. Alternative versions for A/B testing
            
            Ensure the content is platform-optimized, engaging, and incorporates the research insights effectively.
            """
            
            # Generate content with LLM
            response = await self._invoke_llm(prompt, input_data)
            
            result = {
                'agent': self.name,
                'platform': platform,
                'content_type': content_type,
                'created_content': response,
                'tone': tone,
                'call_to_action': call_to_action,
                'topic': topic,
                'status': 'completed'
            }
            
            logger.info(f"{self.name} completed content creation")
            return result
            
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            return {
                'agent': self.name,
                'status': 'error',
                'error': str(e)
            }