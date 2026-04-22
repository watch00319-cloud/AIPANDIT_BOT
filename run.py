#!/usr/bin/env python3
"""
Run the bot - set PYTHONPATH correctly.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

