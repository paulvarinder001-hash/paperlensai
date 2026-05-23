# Configuration for PaperLensAI Streamlit Frontend

# Backend API Configuration
BACKEND_URL = "http://localhost:8000"

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "client": {
        "showErrorDetails": True,
        "toolbarMode": "developer"
    },
    "theme": {
        "primaryColor": "#6366f1",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f8f9fa",
        "textColor": "#262730",
        "font": "sans serif"
    }
}

# Timeouts (in seconds)
API_TIMEOUT = 120
CHAT_TIMEOUT = 60
SEARCH_TIMEOUT = 30

# Page titles and icons
PAGES = {
    "🏠 Home": "home",
    "📤 Upload Paper": "upload",
    "💬 Chat": "chat",
    "🔍 Search": "search",
    "📋 Sections": "sections",
    "🏷️ Terms": "terms",
    "📊 Diagrams": "diagrams",
    "📈 Analysis": "analysis"
}

# Default sections for section extraction
DEFAULT_SECTIONS = [
    "Abstract",
    "Introduction",
    "Literature Review",
    "Methodology",
    "Results",
    "Discussion",
    "Conclusion",
    "References"
]
