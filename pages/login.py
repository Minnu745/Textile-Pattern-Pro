import streamlit as st
from database import check_user

def set_lavender_theme():
    style = """
    <style>
    /* 1. Remove Header (Deploy and 3 Dots) */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
    }

    /* 2. Global Background & Full-Page Centering */
    .stApp {
        background: linear-gradient(135deg, #E6E6FA 0%, #D8BFD8 100%);
        background-attachment: fixed;
    }
    /* 1. Global Background & Full-Page Centering */
    .stApp {
        background: linear-gradient(135deg, #E6E6FA 0%, #D8BFD8 100%);
        background-attachment: fixed;
    }

    .main .block-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        min-height: 100vh;
    }

    /* 2. Style the actual text entry area - Both same width */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stPasswordInput"] input {
        background-color: #E6E6FA !important; /* Lavender Shade */
        color: #4B0082 !important;            /* Deep Violet Text */
        border: 2px solid #7F00FF !important; /* Violet Outline */
        border-radius: 12px !important;
        padding: 10px !important;
        width: 320px !important;       /* Exact same length */
        caret-color: #7F00FF !important;
    }

    /* 3. Place the Eye Icon INSIDE the right end */
    /* Target the container of the password field */
    div[data-testid="stPasswordInput"] [data-baseweb="input"] {
        position: relative; /* Allows absolute positioning for the icon */
        background-color: transparent !important;
        color: #4B0082 !important;  
        border: none !important;
        width: 320px !important; 
    }

    /* Target the button (Eye Icon) specifically */
    div[data-testid="stPasswordInput"] button {
        position: absolute;
        right: 20px; /* Moves it inside the right edge */
        top: 50%;
        transform: translateY(-50%);
        background-color: transparent !important;
        border: none !important;
        color: #7F00FF !important; /* Matches violet outline */
        z-index: 10;
    }

    /* Remove the dark gray background wrapper that causes the "long bar" */
    div[data-testid="stTextInput"] > div,
    div[data-testid="stPasswordInput"] > div,
    div[data-baseweb="base-input"], 
    div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
    }

    /* 4. Center and Style Buttons */
    div.stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }

    div.stButton > button {
        background: linear-gradient(to right, #7F00FF, #4B0082);
        color: white !important;
        border: none;
        border-radius: 50px;
        width: 320px !important;
        padding: 12px 0px;
        font-weight: bold;
        transition: transform 0.2s ease;
        margin-top: 15px;
    }

    /* Center Labels */
    label, [data-testid="stWidgetLabel"] p {
        color: #4B0082 !important;
        text-align: center !important;
        width: 100%;
        font-weight: bold !important;
    }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

set_lavender_theme()

# Redirect if already logged in
if st.session_state.get('logged_in', False):
    st.switch_page("pages/welcome.py")

left_spacer, center_col, right_spacer = st.columns([1, 0.7, 1])

with center_col:
    st.markdown('<h1 style="text-align: center; color: #4B0082;">Login</h1>', unsafe_allow_html=True)


#st.title("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        # Check if both fields are filled
        if u and p: 
            if check_user(u, p):
                st.session_state['logged_in'] = True
                st.session_state['username'] = u
                st.success("Logged in successfully!")
                st.switch_page("pages/welcome.py")
            else:
                st.error("Invalid Username or Password.")
        else:
            # Alert the user if fields are empty
            st.warning("Please enter both a username and a password.")

#st.write("---")
    if st.button("Need an account? Sign Up"):
        st.switch_page("pages/signup.py")