"""
Command line entry point for the package.
"""

import sys
import asyncio
from socialagent.cli import main

def run_cli():
    """Run the CLI with the provided arguments."""
    asyncio.run(main(sys.argv[1:]))
