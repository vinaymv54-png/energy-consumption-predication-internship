"""Styling and theme configuration for the Streamlit app."""

# Dark theme CSS - Professional Enterprise Style
DARK_THEME_CSS = """
<style>
    /* Main app styling */
    body {
        color: #e1e4e8;
        background: linear-gradient(135deg, #0d1117 0%, #1a1f26 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Streamlit container */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #1a1f26 100%);
    }
    
    /* Premium metric cards with gradient */
    .metric-card {
        background: linear-gradient(135deg, #1f6feb 0%, #0969da 50%, #238636 100%);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5), 
                    0 0 1px rgba(31, 111, 235, 0.3);
        color: white;
        margin: 12px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(31, 111, 235, 0.4),
                    0 0 1px rgba(31, 111, 235, 0.5);
    }
    
    /* Premium dashboard cards */
    .dashboard-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 12px;
        padding: 24px;
        margin: 12px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .dashboard-card:hover {
        border-color: rgba(88, 166, 255, 0.4);
        box-shadow: 0 8px 24px rgba(31, 111, 235, 0.2);
    }
    
    /* Titles with gradient */
    h1 {
        background: linear-gradient(135deg, #58a6ff 0%, #1f6feb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #58a6ff;
        font-size: 1.8em;
        font-weight: 600;
        margin-top: 24px;
        margin-bottom: 16px;
        border-bottom: 2px solid rgba(88, 166, 255, 0.3);
        padding-bottom: 12px;
    }
    
    h3 {
        color: #79c0ff;
        font-size: 1.3em;
        font-weight: 600;
    }
    
    /* Premium buttons */
    .stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        color: white;
        border-radius: 8px;
        border: 1px solid #3fb950;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%);
        box-shadow: 0 6px 20px rgba(46, 160, 67, 0.5);
        transform: translateY(-2px);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: rgba(13, 17, 23, 0.7) !important;
        color: #e1e4e8 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        font-size: 0.95em !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1) !important;
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border-right: 1px solid #30363d;
    }
    
    /* Alert messages */
    .stSuccess, .stInfo {
        background: linear-gradient(135deg, rgba(46, 160, 67, 0.2) 0%, rgba(31, 111, 235, 0.2) 100%);
        border-left: 4px solid #3fb950;
        color: #a6e3a1;
        border-radius: 8px;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(218, 54, 51, 0.2) 0%, rgba(244, 81, 30, 0.2) 100%);
        border-left: 4px solid #f85149;
        color: #f85149;
        border-radius: 8px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(158, 106, 3, 0.2) 0%, rgba(206, 167, 0, 0.2) 100%);
        border-left: 4px solid #d29922;
        color: #e3b341;
        border-radius: 8px;
    }
    
    /* Separator line */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #30363d, transparent);
        margin: 24px 0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] button {
        color: #8b949e !important;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #58a6ff !important;
        border-bottom: 3px solid #1f6feb !important;
    }
    
    /* Data editor */
    .stDataFrame {
        background-color: rgba(22, 27, 34, 0.5);
    }
    
    /* Charts */
    .stPlotlyChart {
        background: rgba(22, 27, 34, 0.3);
        border-radius: 12px;
        padding: 12px;
    }
    
    /* Columns gap */
    .stColumn {
        gap: 20px;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-card, .dashboard-card {
        animation: fadeIn 0.5s ease-in-out;
    }
</style>
"""

# Color scheme
COLORS = {
    "primary": "#1f6feb",
    "success": "#238636",
    "danger": "#da3633",
    "warning": "#9e6a03",
    "info": "#39c5cf",
    "dark_bg": "#0d1117",
    "card_bg": "#161b22",
    "text_primary": "#e1e4e8",
    "text_secondary": "#8b949e",
    "border": "#30363d",
}

# Icon mapping
ICONS = {
    "dashboard": "🏠",
    "dataset": "📂",
    "preprocessing": "🧹",
    "analytics": "📊",
    "visualization": "📈",
    "train": "🤖",
    "compare": "🏆",
    "predict": "🔮",
    "history": "📋",
    "reports": "📄",
    "profile": "👤",
    "about": "ℹ️",
    "logout": "🚪",
    "temperature": "🌡️",
    "humidity": "💧",
    "wind": "💨",
    "weather": "⛅",
    "sunrise": "🌅",
    "sunset": "🌇",
    "users": "👥",
    "predictions": "📊",
    "model": "🤖",
    "accuracy": "🎯",
    "consumption": "⚡",
}


def apply_custom_css():
    """Apply custom CSS styling to the app."""
    import streamlit as st

    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)


def get_metric_style(value, max_val=100):
    """Get color based on metric value."""
    if value >= max_val * 0.8:
        return COLORS["success"]
    elif value >= max_val * 0.5:
        return COLORS["warning"]
    else:
        return COLORS["danger"]
