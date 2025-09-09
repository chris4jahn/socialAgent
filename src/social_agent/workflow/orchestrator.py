"""Workflow orchestrator for the social media agent pipeline."""

import asyncio
from typing import Dict, Any, Optional
from ..agents.researcher import ResearcherAgent
from ..agents.copywriter import CopywriterAgent
from ..agents.manager import ManagerAgent
from ..agents.reviewer import ReviewerAgent
from ..config import settings
import structlog

logger = structlog.get_logger(__name__)


class SocialMediaWorkflow:
    """Orchestrates the multi-agent workflow for social media content creation."""
    
    def __init__(self):
        """Initialize the workflow with all agents."""
        # Determine authentication method
        use_azure_identity = (
            settings.azure_client_id is not None and 
            settings.azure_client_secret is not None and 
            settings.azure_tenant_id is not None
        )
        
        # Initialize all agents
        self.researcher = ResearcherAgent(
            name="Researcher",
            endpoint=settings.azure_ai_endpoint,
            api_key=settings.azure_ai_api_key,
            deployment_name=settings.azure_ai_deployment_name,
            use_azure_identity=use_azure_identity
        )
        
        self.copywriter = CopywriterAgent(
            name="Copywriter",
            endpoint=settings.azure_ai_endpoint,
            api_key=settings.azure_ai_api_key,
            deployment_name=settings.azure_ai_deployment_name,
            use_azure_identity=use_azure_identity
        )
        
        self.manager = ManagerAgent(
            name="Manager",
            endpoint=settings.azure_ai_endpoint,
            api_key=settings.azure_ai_api_key,
            deployment_name=settings.azure_ai_deployment_name,
            use_azure_identity=use_azure_identity
        )
        
        self.reviewer = ReviewerAgent(
            name="Reviewer",
            endpoint=settings.azure_ai_endpoint,
            api_key=settings.azure_ai_api_key,
            deployment_name=settings.azure_ai_deployment_name,
            use_azure_identity=use_azure_identity
        )
        
        logger.info("Social Media Workflow initialized with all agents")
    
    async def run_workflow(
        self,
        topic: str,
        platform: str = "Instagram",
        target_audience: str = "general audience",
        content_type: str = "general post",
        tone: str = "engaging and professional",
        goals: str = "increase engagement",
        budget: str = "organic only",
        brand_guidelines: str = "maintain professional and authentic tone",
        compliance_requirements: str = "standard social media policies",
        call_to_action: str = "engage with the content",
        industry: Optional[str] = None,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """Run the complete social media content creation workflow.
        
        Args:
            topic: Main topic for content creation
            platform: Target social media platform
            target_audience: Description of target audience
            content_type: Type of content to create
            tone: Desired tone for the content
            goals: Marketing objectives
            budget: Available budget for promotion
            brand_guidelines: Brand voice and guidelines
            compliance_requirements: Legal and policy requirements
            call_to_action: Desired audience action
            industry: Industry context (optional)
            max_retries: Maximum retries for conditional approvals
            
        Returns:
            Dictionary containing complete workflow results
        """
        workflow_id = f"workflow_{asyncio.current_task().get_name() if asyncio.current_task() else 'main'}"
        logger.info(f"Starting workflow {workflow_id}", topic=topic, platform=platform)
        
        try:
            # Step 1: Research and trend analysis
            logger.info("Step 1: Starting research phase")
            research_input = {
                'topic': topic,
                'target_audience': target_audience,
                'platform': platform,
                'industry': industry or 'general'
            }
            
            research_result = await self.researcher.process(research_input)
            if research_result.get('status') == 'error':
                return self._create_error_result(workflow_id, "Research phase failed", research_result)
            
            # Step 2: Content creation
            logger.info("Step 2: Starting content creation phase")
            copywriter_input = {
                'research_insights': research_result.get('research_insights'),
                'content_type': content_type,
                'platform': platform,
                'tone': tone,
                'call_to_action': call_to_action,
                'topic': topic,
                'target_audience': target_audience
            }
            
            content_result = await self.copywriter.process(copywriter_input)
            if content_result.get('status') == 'error':
                return self._create_error_result(workflow_id, "Content creation phase failed", content_result)
            
            # Step 3: Content optimization and strategy
            logger.info("Step 3: Starting optimization phase")
            manager_input = {
                'created_content': content_result.get('created_content'),
                'platform': platform,
                'budget': budget,
                'goals': goals,
                'brand_guidelines': brand_guidelines,
                'topic': topic,
                'target_audience': target_audience
            }
            
            optimization_result = await self.manager.process(manager_input)
            if optimization_result.get('status') == 'error':
                return self._create_error_result(workflow_id, "Optimization phase failed", optimization_result)
            
            # Step 4: Review and approval (with retry logic)
            retries = 0
            final_result = None
            
            while retries <= max_retries:
                logger.info(f"Step 4: Starting review phase (attempt {retries + 1})")
                reviewer_input = {
                    'created_content': content_result.get('created_content'),
                    'optimization_strategy': optimization_result.get('optimization_strategy'),
                    'brand_guidelines': brand_guidelines,
                    'compliance_requirements': compliance_requirements,
                    'target_audience': target_audience,
                    'platform': platform,
                    'topic': topic
                }
                
                review_result = await self.reviewer.process(reviewer_input)
                if review_result.get('status') == 'error':
                    return self._create_error_result(workflow_id, "Review phase failed", review_result)
                
                approval_status = review_result.get('approval_status')
                
                if approval_status == 'approved':
                    logger.info("Content approved - workflow complete")
                    final_result = review_result
                    break
                elif approval_status == 'conditional_approval' and retries < max_retries:
                    logger.info(f"Content requires modifications - retrying (attempt {retries + 1})")
                    # In a more sophisticated implementation, we could parse the feedback
                    # and automatically apply modifications or re-run specific agents
                    retries += 1
                elif approval_status == 'rejected' or retries >= max_retries:
                    logger.warning("Content rejected or max retries reached")
                    final_result = review_result
                    break
                else:
                    retries += 1
            
            # Compile complete workflow results
            complete_result = {
                'workflow_id': workflow_id,
                'status': 'completed',
                'input_parameters': {
                    'topic': topic,
                    'platform': platform,
                    'target_audience': target_audience,
                    'content_type': content_type,
                    'tone': tone,
                    'goals': goals,
                    'budget': budget
                },
                'research_phase': research_result,
                'content_creation_phase': content_result,
                'optimization_phase': optimization_result,
                'review_phase': final_result,
                'final_approval_status': final_result.get('approval_status') if final_result else 'failed',
                'retries_used': retries
            }
            
            logger.info(f"Workflow {workflow_id} completed", 
                       approval_status=complete_result['final_approval_status'])
            return complete_result
            
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed with exception: {e}")
            return self._create_error_result(workflow_id, f"Workflow failed: {str(e)}", {'error': str(e)})
    
    def _create_error_result(self, workflow_id: str, message: str, error_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a standardized error result."""
        return {
            'workflow_id': workflow_id,
            'status': 'error',
            'error_message': message,
            'error_data': error_data
        }