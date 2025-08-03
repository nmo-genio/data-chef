"""
Data Chef - Core Application
============================

Main Streamlit application for voice-powered data analysis.
Integrates ElevenLabs voice generation with HyperMode data analysis.

Classes:
    - HyperModeMCP: Mock data analysis through Mother Duck database
    - ElevenLabsClient: Voice generation using ElevenLabs API
    - DataChef: Main application orchestrator

Author: Data Chef Team
Version: 1.0.0
License: MIT
"""

import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import elevenlabs
import asyncio
import websockets
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Data Chef",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, minimalist styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4ECDC4;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .status-box {
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #4ECDC4;
    }
    .success-box {
        background-color: #f8f9fa;
        border-left-color: #28a745;
    }
    .error-box {
        background-color: #f8f9fa;
        border-left-color: #dc3545;
    }
    .info-box {
        background-color: #f8f9fa;
        border-left-color: #17a2b8;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .button-container {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    .sidebar-section {
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e9ecef;
    }
    .sidebar-section:last-child {
        border-bottom: none;
    }
</style>
""", unsafe_allow_html=True)


class HyperModeMCP:
    """
    HyperMode MCP (Model Context Protocol) Client
    
    Handles data analysis requests through Mother Duck database.
    Currently running in mock mode for demonstration purposes.
    
    Attributes:
        connected (bool): Connection status to HyperMode
        request_id (int): Request counter for tracking
    """
    
    def __init__(self):
        """Initialize HyperMode MCP client."""
        self.connected = False
        self.request_id = 0
        
    async def connect(self):
        """
        Connect to HyperMode through Mother Duck database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # HyperMode uses Mother Duck for data connections and queries
            # This is a mock implementation since actual HyperMode integration
            # would require proper Mother Duck database setup
            self.connected = True
            return True
                
        except Exception as e:
            st.error(f"Failed to connect to HyperMode: {str(e)}")
            return False
    
    def _get_request_id(self):
        """Generate unique request ID for tracking."""
        self.request_id += 1
        return self.request_id
    
    async def send_message(self, message):
        """
        Process data analysis requests through Mother Duck database.
        
        Args:
            message (dict): Message containing analysis request
            
        Returns:
            dict: Analysis results (mock data in current implementation)
        """
        if not self.connected:
            return None
        try:
            # Mock response - in real implementation, this would:
            # 1. Connect to Mother Duck database
            # 2. Execute queries through HyperMode
            # 3. Return actual data analysis results
            
            mock_response = {
                "status": "mock",
                "message": "HyperMode queries are processed through Mother Duck database",
                "timestamp": datetime.now().isoformat(),
                "user_query": message.get("content", ""),
                "analysis": {
                    "summary": "This is a mock response. Real HyperMode integration requires Mother Duck database setup.",
                    "data_source": "Mother Duck Database",
                    "query_type": "Data Analysis",
                    "recommendations": [
                        "Set up Mother Duck database connection",
                        "Configure HyperMode with proper database credentials",
                        "Implement actual data querying logic"
                    ]
                }
            }
            
            # Simulate processing delay
            await asyncio.sleep(1)
            
            return mock_response
                
        except Exception as e:
            st.error(f"Error processing HyperMode request: {str(e)}")
            return None
    
    async def close(self):
        """Close HyperMode connection."""
        self.connected = False


class ElevenLabsClient:
    """
    ElevenLabs Voice Generation Client
    
    Handles text-to-speech conversion using ElevenLabs API.
    Provides voice generation capabilities for the Data Chef application.
    
    Attributes:
        api_key (str): ElevenLabs API key
    """
    
    def __init__(self, api_key=None):
        """
        Initialize ElevenLabs client.
        
        Args:
            api_key (str, optional): ElevenLabs API key. If None, loads from environment.
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if self.api_key and self.api_key != "your_elevenlabs_api_key_here":
            try:
                elevenlabs.set_api_key(self.api_key)
            except Exception as e:
                st.error(f"Failed to initialize ElevenLabs client: {str(e)}")
    
    def generate_speech(self, text, voice="EXAVITQu4vr4xnSDxMaL", model="eleven_monolingual_v1"):
        """
        Generate speech from text using ElevenLabs API.
        
        Args:
            text (str): Text to convert to speech
            voice (str): Voice ID to use for generation
            model (str): Model to use for generation
            
        Returns:
            bytes: Audio data in MP3 format, or None if generation fails
        """
        try:
            if not self.api_key or self.api_key == "your_elevenlabs_api_key_here":
                st.error("ElevenLabs API key not set. Please set your API key.")
                return None
            
            # Use the ElevenLabs API for text-to-speech conversion
            audio = elevenlabs.generate(
                text=text,
                voice=voice,
                model=model
            )
            
            return audio
                
        except Exception as e:
            st.error(f"Error generating speech: {str(e)}")
            return None


class DataChef:
    """
    Main Data Chef Application Orchestrator
    
    Coordinates between HyperMode data analysis and ElevenLabs voice generation.
    Manages conversation history and provides the main application interface.
    
    Attributes:
        hypermode (HyperModeMCP): Data analysis client
        elevenlabs (ElevenLabsClient): Voice generation client
        conversation_history (list): List of conversation interactions
    """
    
    def __init__(self):
        """Initialize Data Chef application."""
        self.hypermode = HyperModeMCP()
        self.elevenlabs = ElevenLabsClient()
        self.conversation_history = []
    
    async def process_data_request(self, user_input):
        """
        Process data analysis requests through HyperMode MCP.
        
        Args:
            user_input (str): User's data analysis request
            
        Returns:
            dict: Analysis results (mock data in current implementation)
        """
        # Mock response since HyperMode doesn't support URL connections
        # Note: HyperMode currently connects through Mother Duck database, not direct URL connections
        # This mock demonstrates the expected response format for future HyperMode integration
        mock_response = {
            "status": "mock",
            "message": """🧑‍🍳 Data Chef Response

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
            "timestamp": datetime.now().isoformat(),
            "user_query": user_input,
            "analysis": {
                "summary": "Chef-themed data analysis with culinary insights",
                "data_source": "Mock Data (HyperMode URL connection not yet supported)",
                "query_type": "Data Analysis",
                "recommendations": [
                    "HyperMode connects through Mother Duck database",
                    "URL-based connections planned for future versions",
                    "Use ElevenLabs for voice generation of responses"
                ]
            }
        }
        
        # Simulate processing delay
        await asyncio.sleep(1)
        
        return mock_response
    
    def generate_voice_response(self, text):
        """
        Generate voice response using ElevenLabs.
        
        Args:
            text (str): Text to convert to speech
            
        Returns:
            bytes: Audio data in MP3 format, or None if generation fails
        """
        return self.elevenlabs.generate_speech(text)
    
    def add_to_history(self, user_input, response):
        """
        Add conversation to history.
        
        Args:
            user_input (str): User's input
            response (dict): System response
        """
        self.conversation_history.append({
            "user": user_input,
            "assistant": response,
            "timestamp": datetime.now().isoformat()
        })


def main():
    """
    Main application function.
    
    Sets up the Streamlit interface and handles user interactions.
    """
    # Header
    st.markdown('<h1 class="main-header">🍳 Data Chef</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1rem; color: #666; margin-bottom: 2rem;">Voice-powered data analysis</p>', unsafe_allow_html=True)
    
    # Initialize Data Chef
    if 'data_chef' not in st.session_state:
        st.session_state.data_chef = DataChef()
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown('<h3 class="sub-header">⚙️ Configuration</h3>', unsafe_allow_html=True)
        
        # ElevenLabs Configuration
        with st.container():
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            elevenlabs_api_key = st.text_input(
                "ElevenLabs API Key",
                type="password",
                help="Your ElevenLabs API key for voice generation"
            )
            
            if st.button("🎤 Test Voice", use_container_width=True):
                with st.spinner("Testing voice generation..."):
                    if elevenlabs_api_key:
                        st.session_state.data_chef.elevenlabs.api_key = elevenlabs_api_key
                        elevenlabs.set_api_key(elevenlabs_api_key)
                        
                        # Test voice generation
                        test_audio = st.session_state.data_chef.elevenlabs.generate_speech("🧑‍🍳 Data Chef Response: Ah, April — now that's a dish worth plating! Revenue: 32,000 — a double-stacked layer cake, rich and oh-so-satisfying.")
                        if test_audio:
                            st.success("✅ Voice generation working!")
                            st.audio(test_audio, format="audio/mp3")
                        else:
                            st.error("❌ Voice generation failed")
                    else:
                        st.warning("⚠️ Please enter your API key first")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Status
        with st.container():
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<h4 style="margin-bottom: 0.5rem;">📊 Status</h4>', unsafe_allow_html=True)
            
            # ElevenLabs status
            if st.session_state.data_chef.elevenlabs.api_key:
                st.success("🎤 ElevenLabs: Configured")
            else:
                st.info("🎤 ElevenLabs: Not configured")
            
            # Mock mode status
            st.info("🔧 Mock Mode: Active")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat interface
    user_input = st.text_area(
        "Ask Data Chef anything:",
        height=120,
        placeholder="Example: Analyze this data, create a report, or just say hello..."
    )
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Analyze Data", type="primary", use_container_width=True):
            if user_input:
                with st.spinner("Processing your request..."):
                    # Process through mock data
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(
                        st.session_state.data_chef.process_data_request(user_input)
                    )
                    loop.close()
                    
                    if response:
                        st.session_state.data_chef.add_to_history(user_input, response)
                        st.success("✅ Analysis completed!")
                        # Show the response
                        if isinstance(response, dict):
                            st.markdown(f"**Response:** {response.get('message', 'No message')}")
                    else:
                        st.error("❌ Failed to process request")
            else:
                st.warning("Please enter a data analysis request")
    
    with col2:
        if st.button("🎤 Generate Voice", use_container_width=True):
            # Check if we have conversation history or use default message
            if st.session_state.data_chef.conversation_history:
                latest_response = st.session_state.data_chef.conversation_history[-1]["assistant"]
                if isinstance(latest_response, dict):
                    response_text = latest_response.get("message", "🧑‍🍳 Data Chef Response: Ah, April — now that's a dish worth plating! Revenue: 32,000 — a double-stacked layer cake, rich and oh-so-satisfying.")
                else:
                    response_text = str(latest_response)
            else:
                # Use default message if no conversation history
                response_text = "🧑‍🍳 Data Chef Response: Ah, April — now that's a dish worth plating! Revenue: 32,000 — a double-stacked layer cake, rich and oh-so-satisfying."
            
            # Check if ElevenLabs is configured
            if not st.session_state.data_chef.elevenlabs.api_key:
                st.error("❌ ElevenLabs API key not configured!")
                st.info("💡 Please enter your API key in the sidebar")
            else:
                with st.spinner("Generating voice..."):
                    audio = st.session_state.data_chef.generate_voice_response(response_text)
                    if audio:
                        st.audio(audio, format="audio/mp3")
                        st.success("🎵 Voice generated!")
                    else:
                        st.error("❌ Voice generation failed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Conversation history
    if st.session_state.data_chef.conversation_history:
        st.markdown('<h4 style="margin-top: 2rem;">📝 Recent Conversations</h4>', unsafe_allow_html=True)
        for i, conv in enumerate(reversed(st.session_state.data_chef.conversation_history[-3:])):  # Show only last 3
            with st.expander(f"Conversation {len(st.session_state.data_chef.conversation_history) - i}", expanded=False):
                st.write(f"**User:** {conv['user']}")
                st.write(f"**Data Chef:** {conv['assistant']}")
                st.caption(f"Timestamp: {conv['timestamp']}")
        
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.data_chef.conversation_history = []
            st.success("History cleared!")
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 0.9rem;">Data Chef - Voice-powered data analysis 🍳</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main() 