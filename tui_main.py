#!/usr/bin/env python3
"""TUI entry point for Zefoy automation."""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tui.app import run_tui

if __name__ == "__main__":
    run_tui()
