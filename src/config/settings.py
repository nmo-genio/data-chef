"""
Data Chef - Configuration Settings
=================================

Centralized configuration for the Data Chef application.
Contains all application settings, API configurations, and constants.

Author: Data Chef Team
Version: 1.0.0
License: MIT
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application Configuration
APP_NAME = "Data Chef"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Voice-powered data analysis assistant"

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "🍳",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# ElevenLabs Configuration
ELEVENLABS_CONFIG = {
    "default_voice": "EXAVITQu4vr4xnSDxMaL",
    "default_model": "eleven_monolingual_v1",
    "api_key_env_var": "ELEVENLABS_API_KEY"
}

# HyperMode Configuration
HYPERMODE_CONFIG = {
    "default_timeout": 30,
    "protocol_version": "2024-11-05",
    "client_name": APP_NAME,
    "client_version": APP_VERSION
}

# Mother Duck Configuration
MOTHER_DUCK_CONFIG = {
    "database_url_env_var": "MOTHER_DUCK_DATABASE_URL",
    "api_key_env_var": "MOTHER_DUCK_API_KEY"
}

# UI Configuration
UI_CONFIG = {
    "main_header_color": "#FF6B6B",
    "sub_header_color": "#4ECDC4",
    "success_color": "#155724",
    "error_color": "#721c24",
    "info_color": "#0c5460"
}

# File Paths
PATHS = {
    "examples": "examples/",
    "docs": "docs/",
    "tests": "tests/",
    "scripts": "scripts/"
}

# Security Configuration
SECURITY_CONFIG = {
    "allowed_file_extensions": [".py", ".js", ".json", ".yml", ".yaml"],
    "blocked_patterns": [
        "ELEVENLABS_API_KEY",
        "MOTHER_DUCK_API_KEY",
        "api_key",
        "password",
        "secret",
        "token",
        "key",
        "credential"
    ],
    "placeholder_patterns": [
        "your_.*_here",
        "example",
        "placeholder",
        "template"
    ]
}

# Development Configuration
DEV_CONFIG = {
    "debug_mode": os.getenv("DEBUG", "False").lower() == "true",
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "mock_mode": True  # Set to False for real HyperMode integration
}

# API Endpoints (for future use)
API_ENDPOINTS = {
    "elevenlabs_base": "https://api.elevenlabs.io/v1",
    "hypermode_base": "https://api.hypermode.ai",
    "mother_duck_base": "https://api.motherduck.com"
}

# Error Messages
ERROR_MESSAGES = {
    "api_key_missing": "API key not configured. Please set your API key.",
    "connection_failed": "Failed to connect to service.",
    "voice_generation_failed": "Failed to generate voice. Check your API key and credits.",
    "data_analysis_failed": "Failed to process data analysis request."
}

# Success Messages
SUCCESS_MESSAGES = {
    "voice_generated": "Voice generated successfully!",
    "analysis_completed": "Analysis completed!",
    "connection_established": "Connection established successfully!"
}

# Default Messages
DEFAULT_MESSAGES = {
    "welcome": "Welcome to Data Chef! Ask me anything about data analysis.",
    "mock_response": """🧑‍🍳 Data Chef Response

Ah, April — now that's a dish worth plating:

Revenue: 32,000 — a double-stacked layer cake, rich and oh-so-satisfying.
Churn Rate: 0.03 — barely a pinch of bitterness, smooth as a velouté.
Bugs Reported: 3 — just a few crumbs on the table, easily swept away.
Team Mood Score: 8.7 — light and fluffy, like a perfectly risen soufflé.
Coffee Consumed: 130 liters — a gentle stream, not a raging river.

🧠 Insight: April was a chef's kiss! Revenue soared, bugs were nearly banished, and the team's spirits rose higher than a meringue in spring. With less churn and less caffeine, the kitchen ran like a dream.

🍲 Recipe Name: "April Ascension Soufflé with Sweet Revenue Reduction"

👨‍🍳 Chef's Quote: "When the bugs are few and the mood is high, every dish tastes like victory!"

📝 Note: This is a mock response. HyperMode currently connects through Mother Duck database, not direct URL connections. We hope to support URL-based data connections in future versions.""",
    "voice_test": "🧑‍🍳 Data Chef Response: Ah, April — now that's a dish worth plating! Revenue: 32,000 — a double-stacked layer cake, rich and oh-so-satisfying."
}

def get_elevenlabs_api_key():
    """Get ElevenLabs API key from environment."""
    return os.getenv(ELEVENLABS_CONFIG["api_key_env_var"])

def get_mother_duck_api_key():
    """Get Mother Duck API key from environment."""
    return os.getenv(MOTHER_DUCK_CONFIG["api_key_env_var"])

def get_mother_duck_database_url():
    """Get Mother Duck database URL from environment."""
    return os.getenv(MOTHER_DUCK_CONFIG["database_url_env_var"])

def is_mock_mode():
    """Check if application is running in mock mode."""
    return DEV_CONFIG["mock_mode"]

def is_debug_mode():
    """Check if debug mode is enabled."""
    return DEV_CONFIG["debug_mode"] 