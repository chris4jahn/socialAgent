from setuptools import setup, find_packages

setup(
    name="socialagent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "semantic-kernel>=0.3.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "socialagent=socialagent.cli:cli_entry_point",
        ],
    },
    author="Christian Forjahn",
    author_email="your.email@example.com",
    description="A Semantic Kernel agent for generating LinkedIn content",
    keywords="semantic-kernel, linkedin, content, ai, agent",
    python_requires=">=3.8",
)
