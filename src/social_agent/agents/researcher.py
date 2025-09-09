"""Researcher/Trend Analyst agent for social media content creation."""

from typing import Dict, Any
from . import BaseAgent
import structlog

logger = structlog.get_logger(__name__)


class ResearcherAgent(BaseAgent):
    """Agent responsible for trend analysis and research."""
    
    @property
    def system_prompt(self) -> str:
        return """You are an expert social media researcher and trend analyst. Your role is to:

1. Analyze current trends and topics relevant to the given subject
2. Identify key insights, statistics, and data points
3. Research audience preferences and engagement patterns
4. Provide context and background information
5. Suggest relevant hashtags and keywords
6. Identify potential viral content angles

Your output should be structured and include:
- Key trends and insights
- Relevant statistics or data points
- Target audience analysis
- Suggested content angles
- Recommended hashtags and keywords
- Potential risks or considerations

Be thorough, accurate, and data-driven in your analysis. Focus on actionable insights that can inform content creation."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process research request and return insights.
        
        Args:
            input_data: Dictionary containing:
                - topic: The main topic to research
                - target_audience: Optional target audience description
                - platform: Optional social media platform focus
                - industry: Optional industry context
        
        Returns:
            Dictionary containing research insights
        """
        try:
            logger.info(f"{self.name} processing research request", topic=input_data.get('topic'))
            
            # Prepare the research prompt
            topic = input_data.get('topic', '')
            target_audience = input_data.get('target_audience', 'general audience')
            platform = input_data.get('platform', 'multiple platforms')
            industry = input_data.get('industry', 'general')
            
            prompt = f"""
            Please conduct a comprehensive trend analysis and research for:
            
            Topic: {topic}
            Target Audience: {target_audience}
            Platform Focus: {platform}
            Industry Context: {industry}
            
            Provide a detailed analysis including current trends, audience insights, content recommendations, and strategic considerations.
            """
            
            # Get insights from LLM
            response = await self._invoke_llm(prompt, input_data)
            
            result = {
                'agent': self.name,
                'topic': topic,
                'research_insights': response,
                'target_audience': target_audience,
                'platform': platform,
                'industry': industry,
                'status': 'completed'
            }
            
            logger.info(f"{self.name} completed research analysis")
            return result
            
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            return {
                'agent': self.name,
                'status': 'error',
                'error': str(e)
            }