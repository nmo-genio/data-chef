#!/usr/bin/env python3
"""
Data Chef - Main Entry Point
============================

Voice-powered data analysis assistant with ElevenLabs integration.
This is the main entry point for the Data Chef application.

Author: Data Chef Team
Version: 1.0.0
License: MIT
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.app import main

if __name__ == "__main__":
    main() 