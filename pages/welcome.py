

from pydantic import conset
import streamlit as st
import time
from PIL import Image
import io
import streamlit.components.v1 as components

import os
from pydantic import Field


#from backend import feature_pattern, generate_pattern # Link to your generation logic
from database import add_user # or check_user for login.py
@st.cache_resource
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
        width: 320px !important;         /* Exact same length */
        
         }

    /* 3. Place the Eye Icon INSIDE the right end */
    /* Target the container of the password field */
    div[data-testid="stPasswordInput"] [data-baseweb="input"] {
        position: relative; /* Allows absolute positioning for the icon */
        background-color: transparent !important;
        border: none !important;
        width: 320px !important; 
    }

    /* Target the button (Eye Icon) specifically */
    div[data-testid="stPasswordInput"] button {
        position: absolute;
        right: 10px; /* Moves it inside the right edge */
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
        caret-color: #7F00FF !important;
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

    /* 5. Sidebar Styling: Light Lavender Shade */
    [data-testid="stSidebar"] {
        background-color: #F3E5F5 !important; /* Very Light Lavender */
        border-right: 2px solid #7F00FF !important; /* Optional Violet edge */
    }

    /* Target the text and icons inside the sidebar to be Violet */
    [data-testid="stSidebar"] .stText, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #4B0082 !important;
    }

    /* Targets the placeholder text color */
    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stPasswordInput"] input::placeholder {
        color: #7F00FF !important; /* Bright Violet */
        opacity: 0.6 !important;   /* Slightly faded so it looks like a placeholder */
        font-style: italic;        /* Optional: Makes it look distinct from typed text */
    }

    /* Support for Safari/Chrome */
    ::-webkit-input-placeholder {
        color: #7F00FF !important;
    }

    /* Support for Firefox */
    ::-moz-placeholder {
        color: #7F00FF !important;
    }

    /* 1. Target the File Uploader Container */
    [data-testid="stFileUploader"] {
        background-color: #E6E6FA !important; /* Lavender Shade */
        border: 2px dashed #7F00FF !important; /* Violet Dashed Outline */
        border-radius: 15px !important;
        padding: 20px !important;
        width: 320px !important; /* Matches your other inputs */
    }

    /* 2. Target the "Browse Files" button inside the uploader */
    [data-testid="stFileUploader"] button {
        background: linear-gradient(to right, #7F00FF, #4B0082) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
    }

    /* 3. Style the "Drag and drop" text color */
    [data-testid="stFileUploader"] section {
        color: #4B0082 !important; /* Deep Violet text */
    }

    /* 4. Fix the icon color */
    [data-testid="stFileUploader"] svg {
        fill: #7F00FF !important;
    }

    /* 1. Target the Selectbox main area */
    div[data-testid="stSelectbox"] [data-baseweb="select"] {
        background-color: #F3E5F5 !important; /* Light Lavender Shade */
        border: 2px solid #7F00FF !important; /* Violet Outline */
        border-radius: 12px !important;
        width: 320px !important;               /* Match other inputs */
    }

    /* 2. Target the text inside the box */
    div[data-testid="stSelectbox"] [data-testid="stMarkdownContainer"] p {
        color: #4B0082 !important;
        font-weight: bold;
    }

    /* 3. Style the Dropdown Menu (The list that pops out) */
    ul[role="listbox"] {
        background-color: #F3E5F5 !important; /* Lighter Lavender for the list */
        border: 1px solid #7F00FF !important;
    }

    /* 4. Style individual items in the dropdown */
    li[role="option"] {
        color: #4B0082 !important;
        transition: background 0.2s;
    }

    /* 5. Hover effect for dropdown items */
    li[role="option"]:hover {
        background-color: #D8BFD8 !important; /* Darker lavender on hover */
    }

    /* 6. Fix the arrow icon color */
    div[data-testid="stSelectbox"] svg {
        fill: #7F00FF !important;
    }
    /* 1. Global Background & Centering */
    .stApp {
        background: linear-gradient(135deg, #E6E6FA 0%, #D8BFD8 100%);
        background-attachment: fixed;
    }

    /* 2. Fix ALL Black Boxes (Inputs, Selectboxes, TextAreas) */
    /* This targets the internal 'BaseWeb' layers causing the black backgrounds */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="base-input"],
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input,
    div[data-testid="stPasswordInput"] input {
        background-color: #F3E5F5 !important; /* Light Lavender */
        color: #4B0082 !important;            /* Deep Violet Text */
        border: 2px solid #7F00FF !important; /* Violet Outline */
        border-radius: 12px !important;
    }

    /* 3. Remove default Streamlit dark wrappers */
    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stTextArea"] > div > div,
    div[data-testid="stTextInput"] > div > div,
    div[data-testid="stPasswordInput"] > div > div {
        background-color: transparent !important;
        border: none !important;
    }

    /* 4. Fix the Password Eye Icon Position & Color */
    div[data-testid="stPasswordInput"] [data-baseweb="input"] {
        position: relative;
    }

    div[data-testid="stPasswordInput"] button {
        position: absolute;
        right: 10px;
        color: #7F00FF !important;
        background-color: transparent !important;
    }

    /* 5. Style Dropdown Menus (The pop-up lists) */
    div[role="listbox"], [data-baseweb="menu"] {
        background-color: #F3E5F5 !important;
    }

    div[role="listbox"] li, [data-baseweb="menu"] li {
        color: #4B0082 !important;
    }

    /* 6. Fix Selectbox Arrow & Multi-select Icons */
    div[data-testid="stSelectbox"] svg {
        fill: #7F00FF !important;
    }
    /* 2. Fix the "Black Box" Dropdown Menu (Selectbox options) */
    /* This targets the pop-up list that was black in your screenshot */
    div[role="listbox"], [data-baseweb="menu"], ul {
        background-color: #F3E5F5 !important;
        border: 1px solid #7F00FF !important;
    }

    /* 3. Style the individual options in the list */
    div[role="listbox"] li, 
    [data-baseweb="menu"] li,
    li[role="option"] {
        color: #4B0082 !important;            /* Deep Violet Text */
        font-weight: 500 !important;
        background-color: transparent !important;
    }
    /* 4. Highlight the option when hovering with the mouse */
    li[role="option"]:hover, 
    div[role="option"]:hover {
        background-color: #E6E6FA !important; /* Slightly darker lavender on hover */
        color: #7F00FF !important;            /* Bright Violet text on hover */
    }

    /* 7. Center Labels & Title */
    label, [data-testid="stWidgetLabel"] p {
        color: #4B0082 !important;
        font-weight: bold !important;
        text-align: left; /* Keep left for dashboard layout */
    }

    
    /* Target ALL buttons including Analyze & Design */
    div.stButton > button {
        background-color: #E6E6FA !important; /* Lavender Shade */
        color: #4B0082 !important;            /* Deep Violet Text */
        border: 2px solid #7F00FF !important; /* Violet Outline */
        border-radius: 12px !important;
        padding: 10px !important;
        width: 320px !important;  
        font-weight: bold !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        margin-top: 10px !important;
    }

    /* Hover effect to make it feel interactive */
    div.stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0px 5px 15px rgba(127, 0, 255, 0.4) !important;
        color: #E6E6FA !important; /* Light lavender text on hover */
    }
    
    /* 3. Slider Customization (Intensity Changer to Violet) */
    /* Target the slider handle (the dot) */
    div[data-testid="stSlider"] [data-handle="0"] {
        background-color: #4B0082 !important; /* Dark Violet */
        border: 2px solid #7F00FF !important;
    }
    
    /* Target the active track (the line to the left of the dot) */
    div[data-testid="stSlider"] [role="slider"] > div {
        background-color: #7F00FF !important;
    }

    /* Target the inactive track (the line to the right of the dot) */
    div[data-testid="stSlider"] [data-baseweb="slider"] > div {
        background-color: #D8BFD8 !important;
    }

    /* Slider Value Text (the number) */
    div[data-testid="stSlider"] div[data-testid="stTickBarMin"],
    div[data-testid="stSlider"] div[data-testid="stTickBarMax"],
    div[data-testid="stSlider"] div {
        color: #4B0082 !important;
    }

    /* 4. Sidebar Selection Points (Change Orange to Violet) */
    /* Target the radio button outer circle */
    div[data-testid="stSidebar"] [role="radio"] div:first-child {
        border-color: #7F00FF !important;
    }
    /* 3. Slider Handle (The draggable dot) */
    div[data-testid="stSlider"] [data-handle="0"] {
        background-color: #4B0082 !important; /* Deep Violet Handle */
        border: 2px solid #7F00FF !important; /* Bright Violet Border */
        box-shadow: 0px 0px 10px rgba(127, 0, 255, 0.4) !important;
    }

    /* Targets the 'Analyze & Design' form submit button specifically */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(to right, #7F00FF, #4B0082) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        width: 320px !important;      /* Matches the width of your input boxes */
        padding: 12px 0px !important;
        font-weight: bold !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        margin-top: 15px !important;
        cursor: pointer !important;
    }

    /* Adds the hover effect for consistency */
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0px 5px 15px rgba(127, 0, 255, 0.4) !important;
    }
   
    
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(to right, #9370DB, #4B0082) !important; /* Medium to Deep Violet */
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        width: 320px !important;
        padding: 12px 0px !important;
        font-weight: bold !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        margin-top: 10px !important;
    }

    /* Hover effect for the Download Button */
    div[data-testid="stDownloadButton"] > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0px 8px 15px rgba(127, 0, 255, 0.4) !important;
        background: linear-gradient(to right, #7F00FF, #4B0082) !important;
    }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

set_lavender_theme()

# REFRESH GUARD
#if st.session_state.get('logged_in', False):
 #   st.switch_page("pages/welcomepage.py")

with st.sidebar:
    # Use 'username' from session state if available
    #st.title("Dashboard")
    st.markdown("""
    <h1 style='text-align: center; color: #4B0082; font-family: sans-serif;'>
        Dashboard
    </h1>
    """, unsafe_allow_html=True)
    
    choice = st.radio("create your pattern", ["Theme-Based", "Novel Blending", "Body-Feature Fit"])
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.switch_page("main.py")
# Set layout to wide for the side-by-side view
st.set_page_config(layout="wide")

import os
import streamlit as st
from backend import generate_pattern, apply_pattern_to_garment # Ensure these are imported

if choice == "Theme-Based":
    st.markdown("<h1 style='text-align: center; color: #4B0082;'>AI Fashion Design Preview</h1>", unsafe_allow_html=True)
    
    # --- SPLIT SCREEN LAYOUT ---
    col_input, col_display = st.columns([1, 2])

    with col_input:
        st.markdown("<h3 style='color: #4B0082;'>Design Settings</h3>", unsafe_allow_html=True)
        theme = st.text_input("Describe theme", value="floral pattern")
    
    # Store choice in session state immediately
        g_choice = st.selectbox("Select Garment Type", ["frock", "shirt"], key="garment_selection")
    
        if st.button("Generate Collection"):
            if theme:
                with st.spinner("Generating..."):
                    img_list, error = generate_pattern(theme)
                    if not error:
                        st.session_state.design_collection = {
                        "patterns": img_list,
                        "choice": g_choice  # Save the choice here!
                    }

    with col_display:
        st.markdown("<h3 style='color: #4B0082;'>Garment Visualization</h3>", unsafe_allow_html=True)
    
        if st.session_state.get("design_collection"):
            data = st.session_state.design_collection
        
        # Map filenames to your .avif files
            garment_map = {
                "frock": "assets/frock.jpg", # Ensure filename is exact
                "shirt": "assets/shirt.jpg"
            }
        
        # Use the choice saved during generation
            path = garment_map.get(data["choice"], "assets")

            for i, img_bytes in enumerate(data["patterns"]):
                col_left, col_right = st.columns([1, 1])
            
            # Apply the visualization
                mockup = apply_pattern_to_garment(img_bytes, path)
            
                with col_left:
                    st.image(img_bytes, caption=f"Pattern {i+1}", use_container_width=True)
                    st.download_button(
                        label="Download Pattern",
                        data=mockup,
                        file_name=f"pattern_{i+1}.png",
                        mime="image/png",
                        key=f"pat_bt_{i}" # Unique key
                    )
                with col_right:
                # If this is STILL a square, your .avif file does not have transparency.
                    st.image(mockup, caption="Visualized on Garment", use_container_width=True)
                st.divider()



          # --- NOVEL BLENDING PAGE ---
    
elif choice == "Novel Blending":
    import backend 
   
    st.markdown("""
    <h1 style='text-align: center; color: #4B0082; font-family: sans-serif;'>
        Pattern Blender
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="
        background: -webkit-linear-gradient(#7F00FF, #4B0082);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 1.5rem;
    ">
       Apply the artistic texture of one pattern to the structure of another
    </h1>
    """, unsafe_allow_html=True)
    
    # 1. Image Uploaders
    col1, col2 = st.columns(2)
    with col1:
        content_file = st.file_uploader("Upload Base Structure", type=['png', 'jpg', 'jpeg'], key="content")
    with col2:
        style_file = st.file_uploader("Upload Artistic Style", type=['png', 'jpg', 'jpeg'], key="style")
    
    
    
    # ADDED: Garment Selection for Visualization (matching your Theme-Based logic)
    v_garment = st.selectbox("Select Garment for Visualization", ["frock", "shirt"], key="blend_viz_garment")
    
    blend_intensity = st.slider("Blending Intensity", 0.0, 1.0, 0.5)

    # 3. Action Button
    if st.button("Generate Blend"):
        if content_file is not None and style_file is not None:
            msg_status = st.empty()
            msg_status.markdown("<h4 style='color: #7F00FF; text-align: center;'>AI is dreaming up your pattern...</h4>", unsafe_allow_html=True)    
                # Step A: Generate the blended pattern
            result, error = backend.style_transfer_blend(content_file, style_file, blend_intensity)
                
            if error:
                msg_status.update(label="Blend Failed", state="error", expanded=False)
                st.error(error)
            else:
                    # Step B: Visualization Mapping (The code you wanted to add)
                    garment_map = {
                        "frock": "assets/frock.jpg",
                        "shirt": "assets/shirt.jpg"
                    }
                    path = garment_map.get(v_garment, "assets")

                    # Step C: Apply pattern to garment
                    mockup = backend.apply_pattern_to_garment(result, path)
                    
                   
                    
                    # Display the Results
                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.image(result, caption="Blended Pattern", use_container_width=True)
                    with col_res2:
                        st.image(mockup, caption="Garment Visualization", use_container_width=True)
                    
                    # Provide Download Buttons
                    st.download_button(
                        label="Download Pattern Only",
                        data=result,
                        file_name="blended_pattern.png",
                        mime="image/png",
                        key="dl_pattern"
                    )
                    st.download_button(
                        label="Download Visualization",
                        data=mockup,
                        file_name="garment_mockup.png",
                        mime="image/png",
                        key="dl_mockup"
                    )
        else:
            st.warning("Please upload both a Base Structure and an Artistic Style image first.")

# --- FEATURE 3: BODY-FEATURE FIT ---
# --- FEATURE 3: BODY-FEATURE FIT ---
elif choice == "Body-Feature Fit":
    st.markdown("""
    <h1 style='text-align: center; color: #4B0082; font-family: sans-serif;'>
        Physical Feature Analysts
    </h1>
    <h3 style='text-align: center; color: #4B0082; font-family: sans-serif;'>
        Generate patterns for your style
    </h3>
    """, unsafe_allow_html=True)

    # We use a form to group all inputs together
    with st.form("feature_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            height = st.selectbox("Height Profile", ["Short", "Average", "Tall"])
            body_type = st.selectbox("Body Type", ["Slim", "Curvy", "Athletic"])
            skin_tone = st.selectbox("Skin Tone", ["Bright", "Warm", "Cool", "Deep", "Neutral_Muted"])
            
        with col2:
            goal = st.selectbox("Silhouette Goal", ["Lengthen", "Create_Curves", "Balance_Shoulders"])
            # This selection determines the mockup template
            g_choice = st.selectbox("Select Visualization Garment", ["frock", "shirt"])
            additional_details = st.text_area("Design Concept (e.g., Roses, Geometry)")

        submit_btn = st.form_submit_button("Analyze & Design")
        # Ensure both functions are imported from your backend
        from backend import feature_pattern, apply_pattern_to_garment
   
    # Execution Logic
    if submit_btn:
        if not additional_details:
            st.warning("Please provide a design concept.")
        else:
            with st.spinner("Applying fashion rules and generating 4 custom designs..."):
                # 1. Generate the Patterns (Now returns a list of 4)
                img_list, error = feature_pattern(
                    user_concept=additional_details,
                    garment_type=g_choice,
                    height=height,
                    body_type=body_type,
                    skin_tone=skin_tone,
                    goal=goal
                )
                
                if error:
                    st.error(f"Error: {error}")
                elif img_list:
                    # Determine the correct asset path
                    garment_map = {
                        "frock": "assets/frock.jpg",
                        "shirt": "assets/shirt.jpg"
                    }
                    
                    if body_type == "Curvy" and g_choice == "frock":
                        path = "assets/curvyfrock.png"
                    elif body_type.lower() == "athletic" and g_choice == "frock":
                        path = "assets/atfrock.png"
                    else:
                        path = garment_map.get(g_choice, "assets/frock.jpg")

                    st.divider()
                    st.subheader(f"✨ 4 Design Variations Optimized for {height} frame")

                    # --- LOOP THROUGH THE 4 GENERATED IMAGES ---
                    for i, img_data in enumerate(img_list):
                        st.markdown(f"### Variation {i+1}")
                        
                        # Generate the mockup for THIS specific variation
                        mockup = apply_pattern_to_garment(img_data, path)
                        
                        col_left, col_right = st.columns([1, 1])
                        
                        with col_left:
                            st.image(img_data, caption=f"Pattern {i+1}", use_container_width=True)
                            st.download_button(
                                label=f"Download Pattern {i+1}",
                                data=img_data,
                                file_name=f"pattern_{i+1}.png",
                                mime="image/png",
                                key=f"dl_pat_{i}" # Unique key for each button
                            )
                        
                        # ... (inside your loop)
                        with col_right:
                            st.image(mockup, caption=f"Visualization {i+1}", use_container_width=True)
    
    # --- FIX STARTS HERE ---
    # If mockup is already bytes, use it directly. 
    # If it's a PIL Image, convert it to bytes.
                            import io
                            from PIL import Image

                            if isinstance(mockup, bytes):
                                byte_im = mockup
                            else:
                                buf = io.BytesIO()
                                mockup.save(buf, format="PNG")
                                byte_im = buf.getvalue()
    # --- FIX ENDS HERE ---

                            st.download_button(
                                label=f"Download Mockup {i+1}",
                                data=byte_im,
                                file_name=f"mockup_{i+1}.png",
                                mime="image/png",
                                key=f"dl_mock_{i}" 
                            )
# ...
                        st.divider()
                    
                    st.success("All designs generated successfully!")