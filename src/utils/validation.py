"""
Data Chef - Validation Utilities
===============================

Input validation utilities for the Data Chef application.
Provides helper functions for validating user inputs and API configurations.

Author: Data Chef Team
Version: 1.0.0
License: MIT
"""

import re
from typing import Dict, Any, List, Optional
import streamlit as st

from ..config.settings import SECURITY_CONFIG, ERROR_MESSAGES


class ValidationUtils:
    """
    Input validation utilities for Data Chef.
    
    Provides helper methods for validating user inputs,
    API keys, and configuration settings.
    """
    
    @staticmethod
    def validate_api_key_format(api_key: str, service_name: str = "API") -> bool:
        """
        Validate API key format for various services.
        
        Args:
            api_key (str): API key to validate
            service_name (str): Name of the service for error messages
            
        Returns:
            bool: True if valid format, False otherwise
        """
        if not api_key:
            st.error(f"{service_name} API key is required.")
            return False
        
        # Check for placeholder patterns
        placeholder_patterns = [
            "your_",
            "placeholder",
            "example",
            "template"
        ]
        
        for pattern in placeholder_patterns:
            if pattern in api_key.lower():
                st.error(f"{service_name} API key appears to be a placeholder. Please use a real API key.")
                return False
        
        # Check for minimum length
        if len(api_key) < 20:
            st.error(f"{service_name} API key appears to be too short.")
            return False
        
        return True
    
    @staticmethod
    def validate_voice_id(voice_id: str) -> bool:
        """
        Validate ElevenLabs voice ID format.
        
        Args:
            voice_id (str): Voice ID to validate
            
        Returns:
            bool: True if valid format, False otherwise
        """
        if not voice_id:
            return False
        
        # ElevenLabs voice IDs are typically alphanumeric with hyphens
        pattern = r'^[a-zA-Z0-9\-_]+$'
        return bool(re.match(pattern, voice_id))
    
    @staticmethod
    def validate_text_input(text: str, max_length: int = 1000) -> bool:
        """
        Validate text input for voice generation.
        
        Args:
            text (str): Text to validate
            max_length (int): Maximum allowed length
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not text or not text.strip():
            st.error("Text input cannot be empty.")
            return False
        
        if len(text) > max_length:
            st.error(f"Text input is too long. Maximum {max_length} characters allowed.")
            return False
        
        # Check for potentially harmful content
        harmful_patterns = [
            r'<script',
            r'javascript:',
            r'data:text/html',
            r'vbscript:'
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                st.error("Text input contains potentially harmful content.")
                return False
        
        return True
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str] = None) -> bool:
        """
        Validate file extension for security.
        
        Args:
            filename (str): Filename to validate
            allowed_extensions (List[str]): List of allowed extensions
            
        Returns:
            bool: True if valid extension, False otherwise
        """
        if not allowed_extensions:
            allowed_extensions = SECURITY_CONFIG["allowed_file_extensions"]
        
        if not filename:
            return False
        
        file_extension = filename.lower()
        for ext in allowed_extensions:
            if file_extension.endswith(ext):
                return True
        
        return False
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for safe file operations.
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Sanitized filename
        """
        if not filename:
            return "untitled"
        
        # Remove dangerous characters
        dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip('. ')
        
        # Ensure it's not empty
        if not sanitized:
            sanitized = "untitled"
        
        return sanitized
    
    @staticmethod
    def validate_environment_variables() -> Dict[str, bool]:
        """
        Validate that required environment variables are set.
        
        Returns:
            Dict[str, bool]: Dictionary of environment variable validation results
        """
        import os
        
        required_vars = {
            "ELEVENLABS_API_KEY": "ElevenLabs API Key",
            "MOTHER_DUCK_API_KEY": "Mother Duck API Key (optional)",
            "MOTHER_DUCK_DATABASE_URL": "Mother Duck Database URL (optional)"
        }
        
        results = {}
        
        for var_name, description in required_vars.items():
            value = os.getenv(var_name)
            if value and value != "your_" + var_name.lower() + "_here":
                results[var_name] = True
            else:
                results[var_name] = False
        
        return results
    
    @staticmethod
    def check_security_patterns(content: str) -> List[str]:
        """
        Check content for security-sensitive patterns.
        
        Args:
            content (str): Content to check
            
        Returns:
            List[str]: List of found security patterns
        """
        found_patterns = []
        
        for pattern in SECURITY_CONFIG["blocked_patterns"]:
            if re.search(pattern, content, re.IGNORECASE):
                found_patterns.append(pattern)
        
        return found_patterns
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid URL format, False otherwise
        """
        if not url:
            return False
        
        # Basic URL pattern
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(url_pattern, url))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email (str): Email to validate
            
        Returns:
            bool: True if valid email format, False otherwise
        """
        if not email:
            return False
        
        # Basic email pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email)) 