"""
Data Chef - Voice Utilities
==========================

Voice generation utilities for the Data Chef application.
Provides helper functions for ElevenLabs integration and voice processing.

Author: Data Chef Team
Version: 1.0.0
License: MIT
"""

import elevenlabs
import streamlit as st
from typing import Optional, Dict, Any
import os

from ..config.settings import ELEVENLABS_CONFIG, ERROR_MESSAGES, SUCCESS_MESSAGES


class VoiceUtils:
    """
    Voice generation utilities for Data Chef.
    
    Provides helper methods for ElevenLabs voice generation,
    voice validation, and audio processing.
    """
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validate ElevenLabs API key format.
        
        Args:
            api_key (str): API key to validate
            
        Returns:
            bool: True if valid format, False otherwise
        """
        if not api_key:
            return False
        
        # Check for placeholder patterns
        if "your_" in api_key or "placeholder" in api_key:
            return False
        
        # Check for minimum length (typical API keys are 32+ characters)
        if len(api_key) < 20:
            return False
        
        return True
    
    @staticmethod
    def get_available_voices() -> Dict[str, str]:
        """
        Get list of available ElevenLabs voices.
        
        Returns:
            Dict[str, str]: Dictionary of voice IDs and names
        """
        try:
            voices = elevenlabs.voices()
            return {voice.voice_id: voice.name for voice in voices}
        except Exception as e:
            st.error(f"Failed to fetch voices: {str(e)}")
            return {}
    
    @staticmethod
    def generate_voice_sample(text: str, api_key: str, voice_id: Optional[str] = None) -> Optional[bytes]:
        """
        Generate a voice sample for testing.
        
        Args:
            text (str): Text to convert to speech
            api_key (str): ElevenLabs API key
            voice_id (str, optional): Voice ID to use
            
        Returns:
            bytes: Audio data in MP3 format, or None if generation fails
        """
        try:
            if not VoiceUtils.validate_api_key(api_key):
                st.error(ERROR_MESSAGES["api_key_missing"])
                return None
            
            # Set API key
            elevenlabs.set_api_key(api_key)
            
            # Use default voice if none specified
            if not voice_id:
                voice_id = ELEVENLABS_CONFIG["default_voice"]
            
            # Generate audio
            audio = elevenlabs.generate(
                text=text,
                voice=voice_id,
                model=ELEVENLABS_CONFIG["default_model"]
            )
            
            return audio
            
        except Exception as e:
            st.error(f"Voice generation failed: {str(e)}")
            return None
    
    @staticmethod
    def format_voice_response(audio_data: bytes, filename: str = "voice_response.mp3") -> Dict[str, Any]:
        """
        Format voice response for Streamlit display.
        
        Args:
            audio_data (bytes): Raw audio data
            filename (str): Filename for the audio file
            
        Returns:
            Dict[str, Any]: Formatted response with audio data and metadata
        """
        return {
            "audio_data": audio_data,
            "filename": filename,
            "format": "audio/mp3",
            "success": True
        }
    
    @staticmethod
    def create_voice_test_message() -> str:
        """
        Create a test message for voice generation.
        
        Returns:
            str: Test message for voice generation
        """
        return "This is a test of the Data Chef voice generation system. Hello, world!"
    
    @staticmethod
    def get_voice_status_message(api_key: str) -> str:
        """
        Get status message for voice configuration.
        
        Args:
            api_key (str): ElevenLabs API key
            
        Returns:
            str: Status message
        """
        if VoiceUtils.validate_api_key(api_key):
            return "✅ ElevenLabs configured"
        else:
            return "❌ ElevenLabs not configured" 