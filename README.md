
# 🎨 Textile-Pattern-Pro

Welcome to **Textile-Pattern-Pro** (The AI Textile Design Suite)[cite: 4]! Whether you're a seasoned fashion designer or just playing around with patterns, this app blends cutting-edge AI with classic fashion rules to help you "make your dream design"[cite: 4]. 

## ✨ What It Does

* **Smart Pattern Generation:** Just describe what you want, and the app uses the Stability API (specifically the `stable-diffusion-xl-1024-v1-0` engine) to whip up four stunning, high-quality 8k seamless textile tiles.
* **Built-in Fashion Stylist:** We don't just generate random patterns! Our built-in fashion engine customizes your design prompt based on the wearer's height, body type, skin tone, and silhouette goals[cite: 2].
* **Virtual Try-On:** Want to see how the fabric looks in the real world? The app applies your generated pattern directly onto garment images using a custom "deep blend" method[cite: 2].
* **Studio-Quality Mockups:** We make the fabric look incredibly realistic by automatically bumping up the contrast to 1.8, sharpness to 3.5, and brightness to 1.2, which makes every fold and seam pop[cite: 2].
* **AI Style Blending:** You can mix and match visual vibes with our AI style transfer tool, powered by TensorFlow's Magenta model (`arbitrary-image-stylization-v1-256`)[cite: 2].
* **Secure & Beautiful:** Everything is wrapped up in a gorgeous custom lavender and violet gradient interface[cite: 4]. Plus, you can securely save your progress using the built-in "Sign Up" and "Login" system backed by a local SQLite database[cite: 3, 4].

## 🛠️ Tech Stack

* **Frontend:** Streamlit for a smooth and responsive user interface[cite: 2, 4].
* **AI Brains:** The Stability SDK for pattern creation and TensorFlow/Magenta for style transfer[cite: 2].
* **Image Magic:** Pillow (PIL) and NumPy handle all the masking, blending, and resizing under the hood[cite: 2].
* **Database:** SQLite3 handles user credentials and ensures unique usernames.

## 💻 Getting Started

Follow these steps to get the project running on your local machine.

### 1. Clone the repository
```bash
git clone [https://github.com/Minnu745/Textile-Pattern-Pro.git](https://github.com/Minnu745/Textile-Pattern-Pro.git)
cd Textile-Pattern-Pro
