"""
Command line interface for the LinkedIn Content Generator Agent.
"""

import argparse
import asyncio
import os
import sys
from typing import Dict, List, Optional

from socialagent.agent import LinkedInContentAgent


async def generate_post(agent: LinkedInContentAgent, args: argparse.Namespace) -> None:
    """Generate a LinkedIn post based on command line arguments."""
    post = await agent.generate_linkedin_post(
        topic=args.topic,
        audience=args.audience,
        tone=args.tone,
        include_hashtags=args.hashtags,
        length=args.length
    )
    
    print("\n=== Generated LinkedIn Post ===\n")
    print(post)
    print("\n==============================\n")


async def generate_series(agent: LinkedInContentAgent, args: argparse.Namespace) -> None:
    """Generate a LinkedIn content series based on command line arguments."""
    series = await agent.generate_content_series(
        main_topic=args.topic,
        number_of_posts=args.number,
        audience=args.audience,
        content_goal=args.goal
    )
    
    print("\n=== Generated Content Series ===\n")
    print(series)
    print("\n===============================\n")


async def analyze_post(agent: LinkedInContentAgent, args: argparse.Namespace) -> None:
    """Analyze a LinkedIn post based on command line arguments."""
    analysis = await agent.analyze_post(post_content=args.content)
    
    print("\n=== Post Analysis ===\n")
    print(analysis)
    print("\n====================\n")


async def interactive_mode(agent: LinkedInContentAgent) -> None:
    """Run the agent in interactive mode, prompting the user for input."""
    print("\n=== LinkedIn Content Generator Agent ===\n")
    print("Welcome to the LinkedIn Content Generator. What would you like to create today?\n")
    
    while True:
        print("Options:")
        print("1. Generate a single LinkedIn post")
        print("2. Create a content series plan")
        print("3. Analyze an existing post")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            # Single post generation
            topic = input("\nWhat topic would you like to write about? ")
            audience = input("Who is your target audience? (default: professionals) ") or "professionals"
            tone = input("What tone would you like? (professional, conversational, inspirational, etc.) (default: professional) ") or "professional"
            hashtags = input("Include hashtags? (yes/no) (default: yes) ").lower() != "no"
            length = input("Post length? (short, medium, long) (default: medium) ") or "medium"
            
            print("\nGenerating LinkedIn post...")
            post = await agent.generate_linkedin_post(
                topic=topic,
                audience=audience,
                tone=tone,
                include_hashtags=hashtags,
                length=length
            )
            
            print("\n=== Generated LinkedIn Post ===\n")
            print(post)
            print("\n==============================\n")
            
        elif choice == "2":
            # Content series generation
            topic = input("\nWhat is the main topic for your content series? ")
            number = int(input("How many posts would you like in the series? (default: 5) ") or "5")
            audience = input("Who is your target audience? (default: professionals) ") or "professionals"
            goal = input("What is your content goal? (e.g., establish thought leadership, drive engagement) (default: establish thought leadership) ") or "establish thought leadership"
            
            print("\nGenerating content series plan...")
            series = await agent.generate_content_series(
                main_topic=topic,
                number_of_posts=number,
                audience=audience,
                content_goal=goal
            )
            
            print("\n=== Generated Content Series ===\n")
            print(series)
            print("\n===============================\n")
            
        elif choice == "3":
            # Post analysis
            print("\nPaste the LinkedIn post you'd like to analyze (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if not line and lines and not lines[-1]:
                    break
                lines.append(line)
            
            content = "\n".join(lines[:-1])  # Remove the last empty line
            
            print("\nAnalyzing post...")
            analysis = await agent.analyze_post(post_content=content)
            
            print("\n=== Post Analysis ===\n")
            print(analysis)
            print("\n====================\n")
            
        elif choice == "4":
            print("\nThank you for using the LinkedIn Content Generator. Goodbye!")
            break
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.\n")


async def main(args: Optional[List[str]] = None) -> None:
    """Main entry point for the CLI."""
    # Add debug output to show if environment variables are loaded
    print("Initializing LinkedIn Content Generator...")
    
    # Debug output for environment variables
    if os.environ.get("AZURE_OPENAI_API_KEY"):
        print("Debug: AZURE_OPENAI_API_KEY is set in environment variables")
    if os.environ.get("AZURE_OPENAI_ENDPOINT"):
        print("Debug: AZURE_OPENAI_ENDPOINT is set in environment variables")
    if os.environ.get("AZURE_OPENAI_DEPLOYMENT"):
        print("Debug: AZURE_OPENAI_DEPLOYMENT is set in environment variables")
    if os.environ.get("AZURE_OPENAI_MODEL"):
        print("Debug: AZURE_OPENAI_MODEL is set in environment variables")
    
    parser = argparse.ArgumentParser(description="LinkedIn Content Generator Agent")
    
    # API configuration arguments
    parser.add_argument("--use-azure", action="store_true", default=True, help="Use Azure OpenAI (default: True)")
    parser.add_argument("--azure-api-key", help="Azure OpenAI API Key (or set AZURE_OPENAI_API_KEY environment variable)")
    parser.add_argument("--azure-endpoint", help="Azure OpenAI endpoint URL (or set AZURE_OPENAI_ENDPOINT environment variable)")
    parser.add_argument("--azure-deployment", help="Azure OpenAI deployment name (or set AZURE_OPENAI_DEPLOYMENT environment variable)")
    parser.add_argument("--azure-model", help="Azure OpenAI model ID (or set AZURE_OPENAI_MODEL environment variable)")
    
    parser.add_argument("--openai-api-key", help="OpenAI API Key (or set OPENAI_API_KEY environment variable)")
    parser.add_argument("--openai-model", default="gpt-4", help="OpenAI model to use (default: gpt-4)")
    
    # Personal style configuration
    parser.add_argument("--personal-style", help="Your personal writing style preferences (or set PERSONAL_STYLE environment variable)")
    parser.add_argument("--style-file", help="Path to a file containing your personal writing style guidelines")
    
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")
    
    # Parser for generating a single post
    post_parser = subparsers.add_parser("post", help="Generate a single LinkedIn post")
    post_parser.add_argument("--topic", required=True, help="The topic of the LinkedIn post")
    post_parser.add_argument("--audience", default="professionals", help="Target audience (default: professionals)")
    post_parser.add_argument("--tone", default="professional", help="Tone of the post (default: professional)")
    post_parser.add_argument("--hashtags", action="store_true", default=True, help="Include hashtags (default: True)")
    post_parser.add_argument("--length", default="medium", choices=["short", "medium", "long"], help="Length of the post (default: medium)")
    
    # Parser for generating a content series
    series_parser = subparsers.add_parser("series", help="Generate a LinkedIn content series plan")
    series_parser.add_argument("--topic", required=True, help="The main topic of the content series")
    series_parser.add_argument("--number", type=int, default=5, help="Number of posts in the series (default: 5)")
    series_parser.add_argument("--audience", default="professionals", help="Target audience (default: professionals)")
    series_parser.add_argument("--goal", default="establish thought leadership", help="Content goal (default: establish thought leadership)")
    
    # Parser for analyzing a post
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a LinkedIn post")
    analyze_parser.add_argument("--content", required=True, help="The content of the LinkedIn post to analyze")
    
    # Interactive mode
    subparsers.add_parser("interactive", help="Run in interactive mode")
    
    # Full pipeline mode - for testing the entire process
    subparsers.add_parser("full-pipeline", help="Run a full pipeline demo")
    
    parsed_args = parser.parse_args(args)
    
    # Determine whether to use Azure OpenAI or direct OpenAI
    use_azure = parsed_args.use_azure
    
    # Get API configuration
    if use_azure:
        api_key = parsed_args.azure_api_key or os.environ.get("AZURE_OPENAI_API_KEY")
        # Strip any quotes that might be in the environment variable
        if api_key and (api_key.startswith('"') and api_key.endswith('"') or 
                        api_key.startswith("'") and api_key.endswith("'")):
            api_key = api_key[1:-1]
            
        model_id = parsed_args.azure_model or os.environ.get("AZURE_OPENAI_MODEL")
        azure_endpoint = parsed_args.azure_endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
        azure_deployment = parsed_args.azure_deployment or os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        
        if not api_key:
            print("Error: Azure OpenAI API key is required. Provide it with --azure-api-key or set the AZURE_OPENAI_API_KEY environment variable.")
            sys.exit(1)
        
        if not azure_endpoint:
            print("Error: Azure OpenAI endpoint URL is required. Provide it with --azure-endpoint or set the AZURE_OPENAI_ENDPOINT environment variable.")
            sys.exit(1)
    else:
        api_key = parsed_args.openai_api_key or os.environ.get("OPENAI_API_KEY")
        model_id = parsed_args.openai_model or os.environ.get("OPENAI_MODEL", "gpt-4")
        
        if not api_key:
            print("Error: OpenAI API key is required. Provide it with --openai-api-key or set the OPENAI_API_KEY environment variable.")
            sys.exit(1)
    
    # Get personal style configuration
    personal_style = parsed_args.personal_style or os.environ.get("PERSONAL_STYLE")
    
    # If a style file is provided, read the style from the file
    if parsed_args.style_file and os.path.exists(parsed_args.style_file):
        try:
            with open(parsed_args.style_file, 'r') as f:
                personal_style = f.read().strip()
        except Exception as e:
            print(f"Warning: Could not read style file: {e}")
    
    # Initialize the agent
    try:
        if use_azure:
            agent = LinkedInContentAgent(
                api_key=api_key, 
                model_id=model_id, 
                use_azure=True,
                azure_endpoint=azure_endpoint,
                azure_deployment=azure_deployment,
                personal_style=personal_style
            )
        else:
            agent = LinkedInContentAgent(
                api_key=api_key, 
                model_id=model_id, 
                use_azure=False,
                personal_style=personal_style
            )
    except ValueError as e:
        print(f"Error initializing agent: {e}")
        sys.exit(1)
    
    # Execute the requested action
    if parsed_args.action == "post":
        await generate_post(agent, parsed_args)
    elif parsed_args.action == "series":
        await generate_series(agent, parsed_args)
    elif parsed_args.action == "analyze":
        await analyze_post(agent, parsed_args)
    elif parsed_args.action == "interactive":
        await interactive_mode(agent)
    elif parsed_args.action == "full-pipeline":
        # Demo the full pipeline - for testing
        print("=== LinkedIn Content Generator Full Pipeline Demo ===\n")
        
        # 1. Generate a post about AI
        print("1. Generating a post about AI in the workplace...\n")
        post = await agent.generate_linkedin_post(
            topic="The impact of AI on workplace productivity",
            audience="business professionals",
            tone="informative",
            include_hashtags=True,
            length="medium"
        )
        print(f"Generated Post:\n{post}\n\n")
        
        # 2. Analyze the post
        print("2. Analyzing the generated post...\n")
        analysis = await agent.analyze_post(post_content=post)
        print(f"Post Analysis:\n{analysis}\n\n")
        
        # 3. Generate a content series
        print("3. Generating a content series on AI in business...\n")
        series = await agent.generate_content_series(
            main_topic="Implementing AI in Business Operations",
            number_of_posts=3,
            audience="business leaders and decision makers",
            content_goal="provide practical insights for AI adoption"
        )
        print(f"Content Series Plan:\n{series}\n\n")
        
        print("=== Demo Complete ===")
    else:
        # Default to interactive mode if no action specified
        await interactive_mode(agent)


def cli_entry_point() -> None:
    """Entry point for the installed CLI script."""
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
