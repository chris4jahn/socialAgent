"""Reviewer agent for final content approval and quality assurance."""

from typing import Dict, Any
from . import BaseAgent
import structlog

logger = structlog.get_logger(__name__)


class ReviewerAgent(BaseAgent):
    """Agent responsible for reviewing and approving final content."""
    
    @property
    def system_prompt(self) -> str:
        return """You are an expert content reviewer and quality assurance specialist for social media. Your role is to:

1. Review content for accuracy, clarity, and effectiveness
2. Ensure brand consistency and voice alignment
3. Check for potential legal, ethical, or reputational risks
4. Verify compliance with platform guidelines and policies
5. Assess content quality and engagement potential
6. Identify potential improvements or concerns
7. Provide final approval or rejection with detailed feedback
8. Suggest last-minute optimizations

Your review criteria include:
- Content accuracy and fact-checking
- Brand voice and messaging consistency
- Legal and ethical compliance
- Platform policy adherence
- Cultural sensitivity and inclusivity
- Grammar, spelling, and formatting
- Visual content appropriateness
- Hashtag relevance and effectiveness
- Call-to-action clarity and effectiveness
- Overall engagement potential

Provide constructive feedback and actionable recommendations. Be thorough but efficient in your review process."""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Review final content and provide approval status with feedback.
        
        Args:
            input_data: Dictionary containing:
                - created_content: Original content from copywriter
                - optimization_strategy: Recommendations from manager
                - brand_guidelines: Brand voice and guidelines
                - compliance_requirements: Legal and policy requirements
                - target_audience: Intended audience
        
        Returns:
            Dictionary containing review results and final recommendations
        """
        try:
            logger.info(f"{self.name} reviewing content for approval")
            
            # Extract inputs
            created_content = input_data.get('created_content', '')
            optimization_strategy = input_data.get('optimization_strategy', '')
            brand_guidelines = input_data.get('brand_guidelines', 'maintain professional tone')
            compliance_requirements = input_data.get('compliance_requirements', 'standard social media policies')
            target_audience = input_data.get('target_audience', 'general audience')
            platform = input_data.get('platform', 'Instagram')
            topic = input_data.get('topic', '')
            
            prompt = f"""
            Please conduct a comprehensive review of the following social media content and strategy:
            
            Content to Review: {created_content}
            
            Optimization Strategy: {optimization_strategy}
            
            Review Criteria:
            - Platform: {platform}
            - Topic: {topic}
            - Brand Guidelines: {brand_guidelines}
            - Compliance Requirements: {compliance_requirements}
            - Target Audience: {target_audience}
            
            Please provide a detailed review covering:
            1. Content Quality Assessment (accuracy, clarity, engagement potential)
            2. Brand Consistency Check (voice, messaging, visual alignment)
            3. Compliance Review (platform policies, legal considerations, cultural sensitivity)
            4. Risk Assessment (potential controversies, misinterpretations, negative reactions)
            5. Technical Review (grammar, spelling, formatting, hashtags)
            6. Strategy Alignment (goals, audience, platform optimization)
            7. Final Recommendation (APPROVE, APPROVE WITH MODIFICATIONS, or REJECT)
            8. Specific Improvement Suggestions (if any)
            9. Alternative Approaches (if content is rejected)
            10. Performance Predictions (expected reach, engagement, impact)
            
            Be thorough and constructive in your feedback. If approving, highlight strengths. If rejecting or suggesting modifications, provide clear, actionable guidance.
            """
            
            # Get review from LLM
            response = await self._invoke_llm(prompt, input_data)
            
            # Parse approval status (simplified - could be enhanced with more sophisticated parsing)
            approval_status = "pending"
            if "APPROVE WITH MODIFICATIONS" in response.upper():
                approval_status = "conditional_approval"
            elif "APPROVE" in response.upper():
                approval_status = "approved"
            elif "REJECT" in response.upper():
                approval_status = "rejected"
            
            result = {
                'agent': self.name,
                'platform': platform,
                'topic': topic,
                'review_feedback': response,
                'approval_status': approval_status,
                'brand_guidelines': brand_guidelines,
                'compliance_requirements': compliance_requirements,
                'target_audience': target_audience,
                'status': 'completed'
            }
            
            logger.info(f"{self.name} completed content review", approval_status=approval_status)
            return result
            
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            return {
                'agent': self.name,
                'status': 'error',
                'error': str(e)
            }