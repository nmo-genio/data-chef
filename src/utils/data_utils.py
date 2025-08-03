"""
Data Chef - Data Utilities
==========================

Data processing utilities for the Data Chef application.
Provides helper functions for data analysis and processing.

Author: Data Chef Team
Version: 1.0.0
License: MIT
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import streamlit as st

from ..config.settings import DEFAULT_MESSAGES, ERROR_MESSAGES


class DataUtils:
    """
    Data processing utilities for Data Chef.
    
    Provides helper methods for data analysis, response formatting,
    and conversation management.
    """
    
    @staticmethod
    def format_mock_response(user_input: str) -> Dict[str, Any]:
        """
        Format a mock response for data analysis.
        
        Args:
            user_input (str): User's input query
            
        Returns:
            Dict[str, Any]: Formatted mock response
        """
        return {
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
    
    @staticmethod
    def validate_user_input(user_input: str) -> bool:
        """
        Validate user input for data analysis.
        
        Args:
            user_input (str): User's input to validate
            
        Returns:
            bool: True if input is valid, False otherwise
        """
        if not user_input or not user_input.strip():
            return False
        
        # Check for minimum length
        if len(user_input.strip()) < 3:
            return False
        
        # Check for maximum length (prevent abuse)
        if len(user_input) > 1000:
            return False
        
        return True
    
    @staticmethod
    def sanitize_user_input(user_input: str) -> str:
        """
        Sanitize user input for safe processing.
        
        Args:
            user_input (str): Raw user input
            
        Returns:
            str: Sanitized user input
        """
        # Remove leading/trailing whitespace
        sanitized = user_input.strip()
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&']
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized
    
    @staticmethod
    def format_conversation_entry(user_input: str, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a conversation entry for history.
        
        Args:
            user_input (str): User's input
            response (Dict[str, Any]): System response
            
        Returns:
            Dict[str, Any]: Formatted conversation entry
        """
        return {
            "user": user_input,
            "assistant": response,
            "timestamp": datetime.now().isoformat(),
            "id": f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
    
    @staticmethod
    def extract_response_text(response: Dict[str, Any]) -> str:
        """
        Extract text from response for voice generation.
        
        Args:
            response (Dict[str, Any]): Response dictionary
            
        Returns:
            str: Extracted text for voice generation
        """
        if isinstance(response, dict):
            # Try to get message from response
            if "message" in response:
                return response["message"]
            elif "analysis" in response and "summary" in response["analysis"]:
                return response["analysis"]["summary"]
            else:
                return str(response)
        else:
            return str(response)
    
    @staticmethod
    def create_analysis_summary(response: Dict[str, Any]) -> str:
        """
        Create a summary of analysis results.
        
        Args:
            response (Dict[str, Any]): Analysis response
            
        Returns:
            str: Formatted summary
        """
        if not isinstance(response, dict):
            return str(response)
        
        summary_parts = []
        
        if "message" in response:
            summary_parts.append(f"Response: {response['message']}")
        
        if "analysis" in response:
            analysis = response["analysis"]
            if "summary" in analysis:
                summary_parts.append(f"Summary: {analysis['summary']}")
            
            if "recommendations" in analysis:
                recs = analysis["recommendations"]
                if recs:
                    summary_parts.append(f"Recommendations: {', '.join(recs[:3])}")
        
        return " | ".join(summary_parts) if summary_parts else str(response)
    
    @staticmethod
    def get_conversation_stats(conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about conversation history.
        
        Args:
            conversation_history (List[Dict[str, Any]]): Conversation history
            
        Returns:
            Dict[str, Any]: Conversation statistics
        """
        if not conversation_history:
            return {
                "total_conversations": 0,
                "total_user_messages": 0,
                "average_message_length": 0,
                "last_conversation": None
            }
        
        total_conversations = len(conversation_history)
        total_user_messages = sum(
            len(conv.get("user", "")) for conv in conversation_history
        )
        average_length = total_user_messages / total_conversations if total_conversations > 0 else 0
        last_conversation = conversation_history[-1]["timestamp"] if conversation_history else None
        
        return {
            "total_conversations": total_conversations,
            "total_user_messages": total_user_messages,
            "average_message_length": round(average_length, 2),
            "last_conversation": last_conversation
        } 