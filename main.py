#!/usr/bin/env python3

import asyncio
import logging
import signal
import sys
from pathlib import Path

from dictation import DictationApp

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('/tmp/dictation.log')
        ]
    )

def signal_handler(signum, frame):
    print("\nShutting down...")
    sys.exit(0)

def main():
    setup_logging()
    signal.signal(signal.SIGINT, signal_handler)
    
    app = DictationApp()
    app.run()

if __name__ == "__main__":
    main()