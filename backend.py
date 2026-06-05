
import streamlit as st
import numpy as np

import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image, ImageChops, ImageFilter,ImageEnhance
import os
import requests 
import base64
import io
from stability_sdk import client

# Force a new, clean cache directory in your project folder
os.environ["TFHUB_CACHE_DIR"] = os.path.join(os.getcwd(), "tfhub_cache")

# The function now only asks for 'theme'

# This path is usually more reliable for Pylance to find
from stability_sdk.api import generation
def get_stability_api():
    api_key = os.environ.get('STABILITY_KEY')
    if not api_key:
        raise ValueError("STABILITY_KEY not found in environment variables")
    return client.StabilityInference(key=api_key, verbose=True)
@st.cache_data(show_spinner=False)
def generate_pattern(theme):
    """Generates 4 seamless tiles based on the theme."""
    api = get_stability_api()
    prompt = f"Seamless textile pattern , {theme},semi sized textile high quality, 8k tiling texture, professional fabric design"
    try:
        answers = api.generate(prompt=prompt, width=1024, height=1024, steps=30, samples=4)
        img_list = []
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img_list.append(artifact.binary)
        return img_list, None
    except Exception as e:
        return None, str(e)
    
try:
    import pillow_avif
except ImportError:
    pass
def apply_pattern_to_garment(pattern_bytes, garment_path):
    try:
        # 1. Load images
        pattern = Image.open(io.BytesIO(pattern_bytes)).convert("RGBA")
        garment = Image.open(garment_path).convert("RGBA")
        pattern = pattern.resize(garment.size)

        # 2. ENHANCE THE "GEOMETRY" OF THE FABRIC
        # Contrast @ 1.8: Deepens shadows without losing color detail.
        garment = ImageEnhance.Contrast(garment).enhance(1.8)
        
        # Sharpness @ 3.5: This is the "Magic" value for shirts. 
        # It makes the collar, seams, and tiny wrinkles pop.
        garment = ImageEnhance.Sharpness(garment).enhance(3.5)
        
        # Brightness @ 1.2: Keeps the 'peaks' of the folds white 
        # so the pattern looks like it's under a studio light.
        garment = ImageEnhance.Brightness(garment).enhance(1.2)

        # 3. THE "DEEP" BLEND
        # We multiply the pattern by the high-detail garment
        patterned_base = ImageChops.multiply(pattern, garment)
        
        # 4. TRANSPARENCY FIX (The 'Alpha' Mask)
        # Since it's a JPG, we extract the shape based on brightness
        # We use a threshold of 15 to catch even the faint edges
        mask = garment.convert("L").point(lambda x: 255 if x > 15 else 0)
        # Smooth the edge just a tiny bit
        mask = mask.filter(ImageFilter.GaussianBlur(radius=0.3))

        # 5. FINAL ASSEMBLY
        final_img = Image.new("RGBA", garment.size, (0, 0, 0, 0))
        final_img.paste(patterned_base, (0, 0), mask=mask)

        buf = io.BytesIO()
        final_img.save(buf, format="PNG")
        return buf.getvalue()  # CRITICAL: Returns bytes, not the Image object
    except Exception as e:
        return pattern_bytes
    
    
# --- FUNCTION 2: Style Blending ---
# Move model loading outside to avoid reloading every time the slider moves
@st.cache_resource(show_spinner=False)
def load_magenta_model():
      
    # Local imports to keep startup fast
    import tensorflow as tf
    import tensorflow_hub as hub
    # Pre-configure environment for compressed model loading
    os.environ["TFHUB_MODEL_LOAD_FORMAT"] = "COMPRESSED"
    return hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
@st.cache_data(show_spinner=False)
def style_transfer_blend(content_file, style_file, intensity=0.5):
    import tensorflow as tf
    try:
        model = load_magenta_model()

        def preprocess_img(file):
            # Uses Image and np from global scope
            img = Image.open(file).convert('RGB').resize((512, 512))
            img_array = np.array(img)
            img_tensor = tf.image.convert_image_dtype(img_array, tf.float32)
            return img_tensor[tf.newaxis, :]

        content_tensor = preprocess_img(content_file)
        style_tensor = preprocess_img(style_file)

        # 1. Stylize
        outputs = model(tf.constant(content_tensor), tf.constant(style_tensor))
        stylized_image = outputs[0]

        # 2. Blend
        blend = tf.add(
            tf.multiply(stylized_image[0], intensity),
            tf.multiply(content_tensor[0], (1.0 - intensity))
        )

        # 3. Post-Process
        final_tensor = tf.image.adjust_contrast(blend, contrast_factor=1.2)
        final_tensor = tf.clip_by_value(final_tensor, 0.0, 1.0)

        # Output conversion
        result_array = (final_tensor.numpy() * 255).astype(np.uint8)
        result_img = Image.fromarray(result_array)
        
        buf = io.BytesIO()
        result_img.save(buf, format="PNG")
        return buf.getvalue(), None

    except Exception as e:
        return None, f"AI Error: {str(e)}"

import streamlit as st
import requests
import base64
import json

# --- 1. THE FASHION ENGINE (Must be defined before the function) ---
FASHION_RULES = {
    "height": {
        "tall": "large-scale patterns, oversized motifs, elongated vertical elements",
        "short": "micro-patterns, ditsy print, fine-scale delicate details",
        "average": "standard scale, balanced proportions"
    },
    "body_type": {
        "slim": "horizontal flow, wide-set motifs, airy arrangement",
        "curvy": "micro patterns, small,small diagonal flow,small cascading organic shapes, flattering bias movement",
        "athletic": "bold geometric structures, weighted bottom density,medium sized patterns"
    },
   "skin_tone": {
        "bright": (
            "High-saturation primary colors: Scarlet red, royal blue, canary yellow, "
            "vibrant magenta, and luminous silver accents. (Clear, high-contrast palette)"
        ),
        "warm": (
            "Yellow-based earth tones: Terracotta, amber, olive green, "
            "burnt orange, mustard, and golden metallic highlights. (Golden undertone palette)"
        ),
        "cool": (
            "Blue-based jewel tones: Emerald green, sapphire blue, amethyst violet, "
            "crisp navy, and silver threading. (Blue/Pink undertone palette)"
        ),
        "deep": (
            "Low-value rich tones: Chocolate mahogany, midnight plum, forest green, "
            "deep charcoal, and metallic copper highlights. (Heavy, saturated palette)"
        ),
        "neutral_muted": (
            "Desaturated soft tones: Dusty rose, sage green, taupe, "
            "sand beige, and soft lagoon blue. (Grey-based, low-contrast palette)"
        )
    },

        "silhouette_goal": {
            "balance_shoulders": "gradient density, bottom-heavy weighted motifs",
            "create_curves": "curvilinear abstract shapes",
            "lengthen": "pinstripe-inspired verticality, cascading vine structures"
    }
}
# --- 2. THE UPDATED STABILITY API ENGINE (Your Code) ---
def feature_pattern(user_concept, garment_type="fabric", height="average", body_type="slim", skin_tone="bright", goal="lengthen"):
    try:
        # Fetch rules from dictionary
        h_rule = FASHION_RULES["height"].get(height.lower(), FASHION_RULES["height"]["average"])
        b_rule = FASHION_RULES["body_type"].get(body_type.lower(), FASHION_RULES["body_type"]["slim"])
        s_rule = FASHION_RULES["skin_tone"].get(skin_tone.lower(), FASHION_RULES["skin_tone"]["bright"])
        g_rule = FASHION_RULES["silhouette_goal"].get(goal.lower(), FASHION_RULES["silhouette_goal"]["lengthen"])

        # Master Rule Override for Curvy
        neg_add = ""
        if body_type.lower() == "curvy":
            h_rule = "micro-scale ditsy texture, tiny miniature motifs"
            neg_add = ", large flowers, bold shapes, oversized patterns"

        # Construct final design brief
        final_prompt = (
            f"Professional standard elegant seamless textile pattern for a {garment_type}, {user_concept}. "
            f"Scale and Proportion: {h_rule}. Structure: {b_rule}, {g_rule}. "
            f"Color Palette: {s_rule}. "
            f"Detailed fashion print, symmetrical, high-resolution, 8k, repeating tile."
        )

        API_KEY = st.secrets.get("STABILITY_KEY")
        API_HOST = "https://api.stability.ai"
        ENGINE_ID = "stable-diffusion-xl-1024-v1-0"

        if not API_KEY:
            return None, "API Key missing! Add STABILITY_KEY to your secrets.toml."

        # The API Request - SAMPLES SET TO 4
        response = requests.post(
            f"{API_HOST}/v1/generation/{ENGINE_ID}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
            json={
                "text_prompts": [
                    {"text": final_prompt, "weight": 1},
                    {"text": f"blurry, low quality, distorted, watermark{neg_add}", "weight": -1} 
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 4, 
                "steps": 30,
            },
        )

        if response.status_code != 200:
            return None, f"Status {response.status_code}: {response.text}"

        data = response.json()
        img_list = []
        
        for artifact in data["artifacts"]:
            image_binary = base64.b64decode(artifact["base64"])
            img_list.append(image_binary)

        return img_list, None

    except Exception as e:
        return None, str(e)


    