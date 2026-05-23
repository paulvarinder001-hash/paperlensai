"""
Utility functions for PaperLensAI Streamlit frontend
Handles API communication and data processing
"""

import requests
import json
from typing import Dict, List, Optional, Any
import streamlit as st


class APIClient:
    """Client for communicating with PaperLensAI backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def upload_paper(self, file_data, timeout: int = 120) -> Dict[str, Any]:
        """Upload and process a PDF paper"""
        try:
            files = {"file": file_data}
            response = requests.post(
                f"{self.base_url}/upload-paper",
                files=files,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def chat(self, query: str, timeout: int = 60) -> Dict[str, Any]:
        """Send a chat query about the paper"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                params={"query": query},
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def search(self, query: str, timeout: int = 30) -> Dict[str, Any]:
        """Search for relevant chunks in the paper"""
        try:
            response = requests.post(
                f"{self.base_url}/search",
                params={"query": query},
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def explain_section(self, section_name: str, timeout: int = 60) -> Dict[str, Any]:
        """Get explanation of a specific paper section"""
        try:
            response = requests.post(
                f"{self.base_url}/explain-section",
                params={"section_name": section_name},
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def simplify_terms(self, timeout: int = 120) -> Dict[str, Any]:
        """Extract and simplify technical terms from the paper"""
        try:
            response = requests.post(
                f"{self.base_url}/simplify-terms",
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def generate_diagram(self, timeout: int = 60) -> Dict[str, Any]:
        """Generate methodology flowchart diagram"""
        try:
            response = requests.post(
                f"{self.base_url}/generate-diagram",
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def generate_analysis(self, timeout: int = 60) -> Dict[str, Any]:
        """Generate comprehensive paper analysis report"""
        try:
            response = requests.post(
                f"{self.base_url}/generate-analysis",
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


def format_chat_message(role: str, content: str) -> Dict[str, str]:
    """Format a chat message for display"""
    return {
        "role": role,  # "user" or "assistant"
        "content": content
    }


def parse_search_results(results: List[str]) -> List[Dict[str, Any]]:
    """Parse and format search results for display"""
    parsed = []
    for i, result in enumerate(results, 1):
        parsed.append({
            "index": i,
            "content": result,
            "preview": result[:150] + "..." if len(result) > 150 else result
        })
    return parsed


def format_term_data(terms: List[Dict]) -> List[Dict[str, str]]:
    """Format term extraction data for display"""
    formatted = []
    for term_data in terms:
        formatted.append({
            "term": term_data.get("term", "Unknown"),
            "meaning": term_data.get("meaning", "No explanation available"),
            "simplified": True
        })
    return formatted


@st.cache_data
def load_api_config(config_module: str = "config"):
    """Load API configuration from config module"""
    try:
        import importlib
        config = importlib.import_module(config_module)
        return {
            "backend_url": getattr(config, "BACKEND_URL", "http://localhost:8000"),
            "api_timeout": getattr(config, "API_TIMEOUT", 120),
            "chat_timeout": getattr(config, "CHAT_TIMEOUT", 60),
            "search_timeout": getattr(config, "SEARCH_TIMEOUT", 30),
        }
    except Exception as e:
        st.warning(f"Could not load config: {e}")
        return {
            "backend_url": "http://localhost:8000",
            "api_timeout": 120,
            "chat_timeout": 60,
            "search_timeout": 30,
        }


def check_backend_health(client: APIClient) -> bool:
    """Check if backend is running and accessible"""
    try:
        response = requests.get(
            f"{client.base_url}/docs",
            timeout=5
        )
        return response.status_code == 200
    except:
        return False


def convert_seconds_to_readable(seconds: int) -> str:
    """Convert seconds to readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        return f"{hours}h"
