"""
main.py – Entry point for RUA (Real life Universal Assistant).

Run with:
    cd c:\\Users\\yanil\\Desktop\\alexa
    python -m rua.main

or directly:
    python main.py
"""

import sys
import os

# Allow running as `python main.py` from within the rua/ folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rua.core.assistant import run

if __name__ == "__main__":
    run()