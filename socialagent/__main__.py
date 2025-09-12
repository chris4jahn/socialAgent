"""
Command line entry point for the package.
"""

import sys
import asyncio
from socialagent.cli import main

def run_cli():
    """Run the CLI with the provided arguments."""
    asyncio.run(main(sys.argv[1:]))

# Call the run_cli function when module is executed
if __name__ == "__main__":
    run_cli()
