"""Main application entry point for Social Agent."""

import asyncio
import sys
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import structlog
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_agent.workflow import SocialMediaWorkflow
from social_agent.config import settings

# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

console = Console()
logger = structlog.get_logger(__name__)


@click.group()
@click.option('--log-level', default='INFO', help='Set the logging level')
def cli(log_level):
    """Social Agent - AI-powered social media content creation workflow."""
    # Set up logging level
    import logging
    logging.basicConfig(level=getattr(logging, log_level.upper()))


@cli.command()
@click.option('--topic', required=True, help='Main topic for content creation')
@click.option('--platform', default='Instagram', help='Target social media platform')
@click.option('--audience', default='general audience', help='Target audience description')
@click.option('--content-type', default='general post', help='Type of content to create')
@click.option('--tone', default='engaging and professional', help='Desired tone for content')
@click.option('--goals', default='increase engagement', help='Marketing objectives')
@click.option('--budget', default='organic only', help='Available budget for promotion')
@click.option('--brand-guidelines', default='maintain professional and authentic tone', help='Brand voice and guidelines')
@click.option('--compliance', default='standard social media policies', help='Compliance requirements')
@click.option('--cta', default='engage with the content', help='Call to action')
@click.option('--industry', help='Industry context (optional)')
@click.option('--output', help='Output file to save results (optional)')
def create(
    topic: str,
    platform: str,
    audience: str,
    content_type: str,
    tone: str,
    goals: str,
    budget: str,
    brand_guidelines: str,
    compliance: str,
    cta: str,
    industry: Optional[str],
    output: Optional[str]
):
    """Create social media content using the AI workflow."""
    
    console.print(Panel.fit(
        f"[bold blue]Social Agent Workflow[/bold blue]\n"
        f"Topic: {topic}\n"
        f"Platform: {platform}\n"
        f"Audience: {audience}",
        title="Starting Content Creation"
    ))
    
    async def run_workflow():
        try:
            # Initialize workflow
            workflow = SocialMediaWorkflow()
            
            # Run the workflow with progress indication
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                
                task = progress.add_task("Running AI workflow...", total=None)
                
                result = await workflow.run_workflow(
                    topic=topic,
                    platform=platform,
                    target_audience=audience,
                    content_type=content_type,
                    tone=tone,
                    goals=goals,
                    budget=budget,
                    brand_guidelines=brand_guidelines,
                    compliance_requirements=compliance,
                    call_to_action=cta,
                    industry=industry
                )
                
                progress.remove_task(task)
            
            # Display results
            display_results(result)
            
            # Save to file if requested
            if output:
                save_results(result, output)
                console.print(f"[green]Results saved to {output}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            logger.error("Workflow failed", error=str(e))
            sys.exit(1)
    
    # Run the async workflow
    asyncio.run(run_workflow())


def display_results(result: dict):
    """Display workflow results in a formatted way."""
    
    # Overall status
    status = result.get('status', 'unknown')
    approval_status = result.get('final_approval_status', 'unknown')
    
    if status == 'error':
        console.print(Panel(
            f"[red]Workflow failed: {result.get('error_message', 'Unknown error')}[/red]",
            title="Error"
        ))
        return
    
    # Status panel
    status_color = "green" if approval_status == "approved" else "yellow" if approval_status == "conditional_approval" else "red"
    console.print(Panel(
        f"[{status_color}]Status: {approval_status.upper()}[/{status_color}]\n"
        f"Retries used: {result.get('retries_used', 0)}",
        title="Workflow Results"
    ))
    
    # Create results table
    table = Table(title="Workflow Phase Results")
    table.add_column("Phase", style="cyan", no_wrap=True)
    table.add_column("Agent", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Output Summary", style="white")
    
    phases = [
        ("Research", result.get('research_phase')),
        ("Content Creation", result.get('content_creation_phase')),
        ("Optimization", result.get('optimization_phase')),
        ("Review", result.get('review_phase'))
    ]
    
    for phase_name, phase_data in phases:
        if phase_data:
            agent = phase_data.get('agent', 'Unknown')
            status = phase_data.get('status', 'Unknown')
            
            # Get a summary of the output
            if phase_name == "Research":
                summary = "Trends and insights analyzed"
            elif phase_name == "Content Creation":
                summary = "Social media content created"
            elif phase_name == "Optimization":
                summary = "Strategy and optimization provided"
            elif phase_name == "Review":
                summary = f"Review completed - {phase_data.get('approval_status', 'unknown')}"
            else:
                summary = "Completed"
            
            table.add_row(phase_name, agent, status, summary)
    
    console.print(table)
    
    # Show final content if approved
    if approval_status in ['approved', 'conditional_approval']:
        content_phase = result.get('content_creation_phase', {})
        created_content = content_phase.get('created_content', '')
        if created_content:
            console.print(Panel(
                created_content,
                title="Final Content",
                title_align="left"
            ))


def save_results(result: dict, filename: str):
    """Save results to a file."""
    import json
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


@cli.command()
def config():
    """Show current configuration."""
    
    console.print(Panel.fit(
        f"[bold blue]Current Configuration[/bold blue]\n\n"
        f"Azure AI Endpoint: {settings.azure_ai_endpoint}\n"
        f"Deployment Name: {settings.azure_ai_deployment_name}\n"
        f"API Key Set: {'Yes' if settings.azure_ai_api_key else 'No'}\n"
        f"Azure Identity: {'Yes' if settings.azure_client_id else 'No'}\n"
        f"Log Level: {settings.log_level}\n"
        f"Workflow Timeout: {settings.workflow_timeout}s",
        title="Configuration"
    ))


if __name__ == "__main__":
    cli()