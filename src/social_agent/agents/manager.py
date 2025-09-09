"""Social Media Manager agent for content optimization and strategy."""

from typing import Dict, Any
from . import BaseAgent
import structlog

logger = structlog.get_logger(__name__)


class ManagerAgent(BaseAgent):
    """Agent responsible for optimizing content for social media platforms."""
    
    @property
    def system_prompt(self) -> str:
        return """You are an expert social media manager with deep knowledge of platform algorithms, posting strategies, and audience engagement. Your role is to:

1. Optimize content for specific platform algorithms
2. Recommend optimal posting times and frequency
3. Suggest engagement strategies and community management approaches
4. Provide cross-platform adaptation recommendations
5. Analyze potential reach and engagement metrics
6. Recommend hashtag strategies and tagging approaches
7. Identify opportunities for paid promotion
8. Ensure content compliance with platform guidelines

Your expertise covers:
- Platform-specific algorithm optimization
- Audience targeting and segmentation
- Content scheduling and timing
- Hashtag and keyword strategies
- Visual content recommendations
- Community engagement tactics
- Performance tracking and analytics
- Crisis management and reputation protection

Provide actionable recommendations that maximize reach, engagement, and ROI while maintaining brand authenticity and compliance."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize content for social media platforms and provide strategic recommendations.
        
        Args:
            input_data: Dictionary containing:
                - created_content: Content from copywriter agent
                - platform: Target social media platform
                - budget: Optional advertising budget
                - goals: Marketing objectives (awareness, engagement, conversions)
                - brand_guidelines: Brand voice and visual guidelines
        
        Returns:
            Dictionary containing optimization recommendations
        """
        try:
            logger.info(f"{self.name} optimizing content", platform=input_data.get('platform'))
            
            # Extract inputs
            created_content = input_data.get('created_content', '')
            platform = input_data.get('platform', 'Instagram')
            budget = input_data.get('budget', 'organic only')
            goals = input_data.get('goals', 'increase engagement')
            brand_guidelines = input_data.get('brand_guidelines', 'maintain professional and authentic tone')
            topic = input_data.get('topic', '')
            
            prompt = f"""
            As a social media manager, please optimize the following content and provide strategic recommendations:
            
            Created Content: {created_content}
            
            Optimization Parameters:
            - Platform: {platform}
            - Topic: {topic}
            - Budget: {budget}
            - Goals: {goals}
            - Brand Guidelines: {brand_guidelines}
            
            Please provide:
            1. Platform-specific optimizations for the content
            2. Optimal posting time and frequency recommendations
            3. Hashtag strategy (trending, niche, branded)
            4. Visual content suggestions and specifications
            5. Engagement tactics and community management tips
            6. Cross-promotion opportunities across other platforms
            7. Paid promotion recommendations (if budget allows)
            8. Performance metrics to track
            9. Risk assessment and compliance considerations
            10. Long-term content series or campaign ideas
            
            Ensure all recommendations are specific to {platform} and aligned with the goals of {goals}.
            """
            
            # Get optimization recommendations from LLM
            response = await self._invoke_llm(prompt, input_data)
            
            result = {
                'agent': self.name,
                'platform': platform,
                'optimization_strategy': response,
                'goals': goals,
                'budget': budget,
                'brand_guidelines': brand_guidelines,
                'topic': topic,
                'status': 'completed'
            }
            
            logger.info(f"{self.name} completed content optimization")
            return result
            
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            return {
                'agent': self.name,
                'status': 'error',
                'error': str(e)
            }