#!/usr/bin/env python
"""
Entry point script for the LinkedIn Content Generator Agent.
"""

import sys
import asyncio
from socialagent.cli import main

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
