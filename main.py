import streamlit as st
from database import init_db
import base64

# --- 1. CONFIG (MUST BE FIRST) ---
st.set_page_config(page_title="Textile AI Home", layout="wide")

def set_lavender_theme():
    style = """
    <style>
    /* 1. Double Shade Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #E6E6FA 0%, #D8BFD8 100%);
        background-attachment: fixed;
    }

    /* 2. Double Shade for Buttons (Violet to Indigo) */
    div.stButton > button {
        background: linear-gradient(to right, #7F00FF, #4B0082);
        color: white;
        border: none;
        border-radius: 50px;
        width: 320px !important;
        padding: 12px 0px;
        font-weight: bold;
        transition: transform 0.2s ease;
    }

    div.stButton > button:hover {
        transform: scale(1.05); /* Slight pop-out effect */
        box-shadow: 0px 5px 15px rgba(127, 0, 255, 0.4);
    }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)
set_lavender_theme()

# Initialize Database
init_db()

# Stay Logged In Logic
if st.session_state.get('logged_in', False):
    st.switch_page("pages/welcome.py")

# --- UI LAYOUT ---

# Centered Title and Subtitle
st.markdown("""
<h1 style="
    background: -webkit-linear-gradient(#7F00FF, #4B0082);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
">
    Welcome to the AI Textile Design Suite
</h1>
""", unsafe_allow_html=True)
#st.write("##")
st.markdown("""
<h1 style="
    background: -webkit-linear-gradient(#7F00FF, #4B0082);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
">
   make your dream design
</h1>
""", unsafe_allow_html=True)


# Spacing to push content down slightly
st.write("##")

# THE SQUEEZE: Using 3 columns to force the buttons into a centered, 300px-wide container
left_spacer, center_col, right_spacer = st.columns([1, 0.7, 1])

with center_col:
    if st.button("Sign Up"):
        st.switch_page("pages/signup.py")
    
    st.write("") # Small gap between buttons
    st.markdown('<h5 class="center-text",style="color: #4B0082;>already have an account</h5>',unsafe_allow_html=True)
    if st.button("Login"):
        st.switch_page("pages/login.py")