"""
LinkedIn Content Generator Agent powered by Semantic Kernel
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / '.env'
load_dotenv(dotenv_path=env_path)

__version__ = "0.1.0"
