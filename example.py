#!/usr/bin/env python3
"""
Example usage of Social Agent workflow.

This script demonstrates how to use the Social Agent workflow
to create social media content using AI agents.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def example_workflow():
    """Example of running the social media workflow."""
    
    print("🤖 Social Agent - AI-Powered Content Creation Workflow")
    print("=" * 60)
    
    # Check if configuration is available
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Configuration not found!")
        print("Please copy .env.example to .env and configure your Azure AI credentials.")
        print("\nExample configuration:")
        print("AZURE_AI_ENDPOINT=https://your-ai-foundry-endpoint.cognitiveservices.azure.com/")
        print("AZURE_AI_API_KEY=your-api-key-here")
        print("AZURE_AI_DEPLOYMENT_NAME=gpt-4")
        return
    
    try:
        from social_agent.workflow import SocialMediaWorkflow
        
        print("✓ All dependencies loaded successfully")
        print("\n🚀 Initializing workflow...")
        
        # Initialize the workflow
        workflow = SocialMediaWorkflow()
        
        print("✓ Workflow initialized with all agents:")
        print("  • Researcher/Trend Analyst")
        print("  • Social Media Editor/Copywriter") 
        print("  • Social Media Manager")
        print("  • Reviewer")
        
        print("\n📊 Running example workflow...")
        
        # Example workflow parameters
        result = await workflow.run_workflow(
            topic="sustainable technology trends",
            platform="LinkedIn",
            target_audience="tech professionals and sustainability advocates",
            content_type="thought leadership post",
            tone="professional and inspiring",
            goals="establish thought leadership and drive engagement",
            industry="clean technology"
        )
        
        print("\n✅ Workflow completed!")
        print(f"Status: {result.get('status')}")
        print(f"Final Approval: {result.get('final_approval_status')}")
        print(f"Retries Used: {result.get('retries_used', 0)}")
        
        # Display key results
        if result.get('status') == 'completed':
            research_phase = result.get('research_phase', {})
            content_phase = result.get('content_creation_phase', {})
            
            print(f"\n📈 Research Insights Available: {'✓' if research_phase.get('research_insights') else '✗'}")
            print(f"📝 Content Created: {'✓' if content_phase.get('created_content') else '✗'}")
            print(f"🎯 Strategy Provided: {'✓' if result.get('optimization_phase', {}).get('optimization_strategy') else '✗'}")
            print(f"🔍 Review Completed: {'✓' if result.get('review_phase', {}).get('review_feedback') else '✗'}")
            
            # Show a snippet of the created content
            created_content = content_phase.get('created_content', '')
            if created_content:
                print(f"\n📄 Content Preview:")
                preview = created_content[:200] + "..." if len(created_content) > 200 else created_content
                print(f"   {preview}")
        
        else:
            print(f"❌ Workflow failed: {result.get('error_message', 'Unknown error')}")
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\nTo install dependencies, run:")
        print("pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error running workflow: {e}")


async def show_configuration():
    """Show current configuration."""
    
    print("🔧 Configuration Status")
    print("=" * 30)
    
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file found")
        
        # Check for required environment variables
        required_vars = [
            "AZURE_AI_ENDPOINT",
            "AZURE_AI_DEPLOYMENT_NAME"
        ]
        
        auth_vars = [
            "AZURE_AI_API_KEY",
            "AZURE_CLIENT_ID"
        ]
        
        for var in required_vars:
            value = os.getenv(var)
            status = "✓" if value else "✗"
            print(f"{status} {var}: {'Set' if value else 'Not set'}")
        
        # Check authentication method
        api_key = os.getenv("AZURE_AI_API_KEY")
        client_id = os.getenv("AZURE_CLIENT_ID")
        
        if api_key:
            print("✓ Authentication: API Key")
        elif client_id:
            print("✓ Authentication: Azure Identity")
        else:
            print("✗ Authentication: Not configured")
        
    else:
        print("✗ .env file not found")
        print("Please copy .env.example to .env and configure your credentials.")


def main():
    """Main entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Social Agent Example")
    parser.add_argument("--config", action="store_true", help="Show configuration status")
    parser.add_argument("--run", action="store_true", help="Run example workflow")
    
    args = parser.parse_args()
    
    if args.config:
        asyncio.run(show_configuration())
    elif args.run:
        asyncio.run(example_workflow())
    else:
        print("Social Agent - AI-Powered Content Creation")
        print("Usage:")
        print("  python example.py --config   # Show configuration status")
        print("  python example.py --run      # Run example workflow")
        print("  social-agent create --help   # See CLI options (after pip install)")


if __name__ == "__main__":
    main()