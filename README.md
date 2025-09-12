# LinkedIn Content Generator Agent

A Pyt4. Set up your Azure OpenAI or OpenAI API configuration:

   For Azure OpenAI (recommended):

   ```bash
   export AZURE_OPENAI_API_KEY=your-azure-api-key
   export AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   export AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   export AZURE_OPENAI_MODEL=gpt-4
   ```

   For direct OpenAI:

   ```bash
   export OPENAI_API_KEY=your-openai-api-key
   export OPENAI_MODEL=gpt-4
   ```

## Customizing Your Writing Style

You can customize the writing style of the agent to match your personal style:

### Option 1: Use the environment variable

```bash
export PERSONAL_STYLE="- Write with a technical focus
- Use industry-specific terminology
- Include data-driven insights
- Maintain a professional but approachable tone"
```

### Option 2: Use a style file

```bash
# Copy and edit the provided template file
cp personal_style_template.txt my_personal_style.txt
# Edit my_personal_style.txt with your preferences
```

### Option 3: Pass the style directly when running the agent

```bash
socialagent interactive --personal-style "- Be conversational and casual
- Use simple language
- Include rhetorical questions
- End with a strong call to action"
```

Or:

```bash
socialagent interactive --style-file my_personal_style.txt
```owered by Semantic Kernel that generates LinkedIn content based on user-provided topics.

## Features

- Generate professional LinkedIn posts on any topic
- Create content series plans with multiple posts
- Analyze existing LinkedIn posts for improvement
- Interactive CLI for easy content generation

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/chris4jahn/socialAgent.git
   cd socialAgent
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the dependencies:

   Option A: Using requirements.txt

   ```bash
   pip install -r requirements.txt
   ```

   Option B: Install the package in development mode

   ```bash
   pip install -e .
   ```

4. Set up your Azure OpenAI or OpenAI API configuration:

   For Azure OpenAI (recommended):

   ```bash
   export AZURE_OPENAI_API_KEY=your-azure-api-key
   export AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   export AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   export AZURE_OPENAI_MODEL=gpt-4
   ```

   Or for OpenAI:

   ```bash
   export OPENAI_API_KEY=your-api-key
   export OPENAI_MODEL=gpt-4
   ```

   Alternatively, you can copy the `.env.template` file to `.env` and edit it:

   ```bash
   cp .env.template .env
   # Then edit the .env file with your favorite text editor
   ```

## Usage

### Command Line Interface

The agent can be used through a command-line interface:

```bash
# Run in interactive mode
socialagent interactive

# Generate a single LinkedIn post
socialagent post --topic "AI in healthcare" --audience "healthcare professionals" --tone "informative"

# Generate a content series
socialagent series --topic "Sustainable business practices" --number 5

# Analyze an existing post
socialagent analyze --content "Your LinkedIn post content here..."

# Use with specific Azure OpenAI configuration
socialagent interactive --azure-api-key "your-key" --azure-endpoint "https://your-endpoint.openai.azure.com/" --azure-deployment "your-deployment"

# Use with OpenAI instead of Azure OpenAI
socialagent interactive --use-azure false --openai-api-key "your-key" --openai-model "gpt-4"
```

### Python API

You can also use the agent directly in your Python code:

```python
import asyncio
from socialagent.agent import LinkedInContentAgent

async def main():
    # Initialize the agent with Azure OpenAI
    agent = LinkedInContentAgent(
        api_key="your-azure-api-key",
        use_azure=True,
        azure_endpoint="https://your-resource-name.openai.azure.com/",
        azure_deployment="your-deployment-name",
        model_id="gpt-4"
    )
    
    # Or initialize with OpenAI
    # agent = LinkedInContentAgent(
    #     api_key="your-openai-api-key",
    #     use_azure=False,
    #     model_id="gpt-4"
    # )
    
    # Generate a LinkedIn post
    post = await agent.generate_linkedin_post(
        topic="Cloud computing trends",
        audience="IT professionals",
        tone="professional",
        include_hashtags=True,
        length="medium"
    )
    
    print(post)

if __name__ == "__main__":
    asyncio.run(main())
```

## Requirements

- Python 3.8+
- Semantic Kernel
- Azure OpenAI API key and endpoint or OpenAI API key

## License

[MIT License](LICENSE)
