"""
Data Chef - Configuration Package
================================

Configuration settings for Data Chef.

Modules:
    - settings: Application settings and constants

Author: Data Chef Team
Version: 1.0.0
License: MIT
"""

from .settings import *

__all__ = [
    'APP_NAME',
    'APP_VERSION',
    'ELEVENLABS_CONFIG',
    'HYPERMODE_CONFIG',
    'UI_CONFIG',
    'get_elevenlabs_api_key',
    'get_mother_duck_api_key',
    'is_mock_mode',
    'is_debug_mode'
] 