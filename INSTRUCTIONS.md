# LinkedIn Content Generator Agent Setup Instructions

## Installation

1. Make sure you have Python 3.8 or newer installed.
2. Install the required packages:

   ```bash
   pip install semantic-kernel openai
   ```

3. Copy the .env.template file to .env and add your OpenAI API key:

   ```bash
   cp .env.template .env
   # Edit the .env file with your favorite text editor to add your API key
   ```

## Running the Agent

You can run the agent in several ways:

### 1. Using the module directly

```bash
python -m socialagent interactive
```

### 2. Using the run.py script

```bash
python run.py interactive
```

### 3. Using the pip installation (after running pip install -e .)

```bash
socialagent interactive
```

## Example Commands

```bash
# Generate a LinkedIn post about AI
python -m socialagent post --topic "The future of AI in business" --audience "business leaders" --tone "insightful"

# Create a content series about cloud computing
python -m socialagent series --topic "Cloud migration strategies" --number 5 --audience "IT managers"

# Analyze a LinkedIn post
python -m socialagent analyze --content "Your LinkedIn post content here"

# Run a full demo pipeline showing all features
python -m socialagent full-pipeline
```