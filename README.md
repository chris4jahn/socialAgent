# Social Agent

A sophisticated AI-powered social media content creation workflow using Azure AI Foundry and Semantic Kernel. This multi-agent system automates the entire content creation process from research to final approval.

## 🤖 Agent Workflow

The Social Agent implements a 4-stage workflow with specialized AI agents:

1. **Researcher/Trend Analyst** - Analyzes current trends, gathers insights, and provides data-driven recommendations
2. **Social Media Editor/Copywriter** - Creates engaging, platform-optimized content based on research insights
3. **Social Media Manager** - Optimizes content for specific platforms, suggests posting strategies and engagement tactics
4. **Reviewer** - Reviews content for quality, compliance, and brand consistency before final approval

## 🚀 Features

- **Multi-Agent Workflow**: Specialized AI agents for each stage of content creation
- **Platform Optimization**: Tailored content for different social media platforms
- **Azure AI Integration**: Powered by Azure AI Foundry and Semantic Kernel
- **Flexible Configuration**: Support for API keys or Azure Identity authentication
- **Rich CLI Interface**: Beautiful command-line interface with progress indicators
- **Comprehensive Logging**: Structured logging for monitoring and debugging
- **Retry Logic**: Automatic retries for content that needs modifications
- **Export Capabilities**: Save workflow results to files

## 📋 Prerequisites

- Python 3.8 or higher
- Azure AI Foundry account with deployed model
- Azure AI API key or Azure Identity credentials

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/chris4jahn/socialAgent.git
   cd socialAgent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package:**
   ```bash
   pip install -e .
   ```

## ⚙️ Configuration

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your Azure AI credentials:**
   ```env
   # Azure AI Configuration
   AZURE_AI_ENDPOINT=https://your-ai-foundry-endpoint.cognitiveservices.azure.com/
   AZURE_AI_API_KEY=your-api-key-here
   AZURE_AI_DEPLOYMENT_NAME=gpt-4
   
   # Application Settings
   LOG_LEVEL=INFO
   WORKFLOW_TIMEOUT=300
   ```

### Authentication Options

**Option 1: API Key (Simpler)**
```env
AZURE_AI_API_KEY=your-api-key-here
```

**Option 2: Azure Identity (Recommended for production)**
```env
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
```

## 🎯 Usage

### Command Line Interface

**Basic usage:**
```bash
social-agent create --topic "sustainable fashion trends" --platform Instagram
```

**Advanced usage with all options:**
```bash
social-agent create \
  --topic "AI in healthcare" \
  --platform LinkedIn \
  --audience "healthcare professionals" \
  --content-type "thought leadership post" \
  --tone "professional and informative" \
  --goals "establish thought leadership" \
  --budget "500 USD for promoted posts" \
  --brand-guidelines "maintain scientific accuracy and ethical tone" \
  --industry "healthcare technology" \
  --output results.json
```

**View current configuration:**
```bash
social-agent config
```

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--topic` | Main topic for content creation | Required |
| `--platform` | Target social media platform | Instagram |
| `--audience` | Target audience description | general audience |
| `--content-type` | Type of content to create | general post |
| `--tone` | Desired tone for content | engaging and professional |
| `--goals` | Marketing objectives | increase engagement |
| `--budget` | Available budget for promotion | organic only |
| `--brand-guidelines` | Brand voice and guidelines | maintain professional and authentic tone |
| `--compliance` | Compliance requirements | standard social media policies |
| `--cta` | Call to action | engage with the content |
| `--industry` | Industry context (optional) | None |
| `--output` | Output file to save results | None |

### Supported Platforms

- Instagram
- LinkedIn
- Twitter/X
- Facebook
- TikTok
- YouTube (Shorts/Community)

## 📊 Example Output

The workflow generates comprehensive results including:

- **Research insights** with trend analysis and audience recommendations
- **Created content** optimized for the target platform
- **Optimization strategy** with posting recommendations and hashtag strategies
- **Review feedback** with approval status and improvement suggestions

## 🔧 Development

### Project Structure

```
src/social_agent/
├── __init__.py
├── agents/
│   ├── __init__.py           # Base agent class
│   ├── researcher.py         # Researcher/Trend Analyst
│   ├── copywriter.py         # Social Media Editor/Copywriter
│   ├── manager.py            # Social Media Manager
│   └── reviewer.py           # Reviewer
├── workflow/
│   ├── __init__.py
│   └── orchestrator.py       # Workflow orchestration
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration management
└── main.py                   # CLI entry point
```

### Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

### Code Formatting

```bash
black src/ tests/
flake8 src/ tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Semantic Kernel](https://github.com/microsoft/semantic-kernel) for the AI orchestration framework
- [Azure AI Foundry](https://azure.microsoft.com/en-us/products/ai-foundry/) for the AI capabilities
- [Rich](https://github.com/Textualize/rich) for the beautiful CLI interface

## 📞 Support

If you encounter any issues or have questions:

1. Check the existing [Issues](https://github.com/chris4jahn/socialAgent/issues)
2. Create a new issue with detailed information
3. Include your configuration (without sensitive data) and error logs
