import streamlit as st
import requests
import io
import base64
import os
import random
import numpy as np
import json
import google.generativeai as genai
from google.api_core import exceptions

## Initialize personal library in session state FIRST
if 'personal_library' not in st.session_state:
    st.session_state.personal_library = []

# Set page config
st.set_page_config(
    page_title="Cool Chromebook Wallpapers",
    page_icon="🖼️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .wallpaper-image {
        border-radius: 10px;
        transition: transform 0.3s;
    }
    .wallpaper-image:hover {
        transform: scale(1.03);
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    h1, h2 {
        color: #1E3A8A;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini API
def initialize_gemini():
    # Replace this with your actual API key
    api_key = "AIzaSyA4O1-zyvh5PdWvQUt4hjTd1R5z6xI5A9w"  
    
    if not api_key:
        st.warning("Gemini API key not found.")
        return False
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Failed to initialize Gemini API: {str(e)}")
        return False

# Function to generate image using Gemini
def generate_gemini_image(prompt, style):
    try:
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 32,
        }
        
        enhanced_prompt = f"{prompt} in {style} style. High resolution wallpaper for Chromebook. Vibrant colors, detailed, professional quality. Reply with just the image. No text."
        
        # Revert to gemini-1.5-flash - Note: Still unlikely to generate images reliably via this method
        image_model = genai.GenerativeModel('gemini-2.0-flash')
        
        response = image_model.generate_content(
            enhanced_prompt,
            generation_config=generation_config,
            stream=False
        )
        
        # Updated response handling for current Gemini API format
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                # Check if the part is image data (less likely for flash/pro with generate_content)
                # This structure assumes a potential future where the API might return image data differently
                # For now, we primarily expect 'text' or errors.
                if hasattr(part, 'blob') and part.blob.mime_type.startswith('image/'):
                     # If image data is found in blob format
                     return part.blob.data
                elif hasattr(part, 'image'): # Check for potential direct image attribute (less common)
                     buf = io.BytesIO()
                     part.image.save(buf, format='PNG')
                     return buf.getvalue()
                elif hasattr(part, 'text'):
                    # Explicitly handle text response
                    st.warning("Gemini returned text instead of image data.")
                    # Log the text response for debugging if needed
                    # print(f"Gemini text response: {part.text}")
                    return None

        st.warning("No image data found in response or response format not recognized.")
        return None

    except exceptions.GoogleAPIError as e:
        # Handle specific API errors (like permission denied, quota exceeded)
        st.error(f"API Error: {str(e)}")
        return None
    except Exception as e:
        # Handle other potential errors during generation
        st.error(f"Error generating image: {str(e)}")
        return None

# Function to generate a random colored image as numpy array (fallback)
def generate_colored_image(width=1280, height=720):
    # Create a random colored image as numpy array
    color = [
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    ]
    
    # Create a solid color image as numpy array
    img_array = np.ones((height, width, 3), dtype=np.uint8)
    img_array[:, :] = color
    
    return img_array

# Title and description
st.title("🖼️ Cool Chromebook Wallpapers")
st.markdown("Get awesome wallpapers for your Chromebook! Choose from our collection or generate custom AI wallpapers with Gemini.")

# Function to download an image
def get_download_link(img_data, filename):
    if isinstance(img_data, np.ndarray):
        # Convert numpy array to bytes
        from io import BytesIO
        import matplotlib.pyplot as plt
        
        buf = BytesIO()
        plt.imsave(buf, img_data)
        buf.seek(0)
        img_bytes = buf.getvalue()
    else:
        img_bytes = img_data
        
    b64 = base64.b64encode(img_bytes).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">Download Wallpaper</a>'
    return href

# Create tabs for the three main functions
tab1, tab2, tab3 = st.tabs(["Browse Wallpapers", "Generate AI Wallpapers", "My Library"])

# Tab 1: Browse pre-made wallpapers
with tab1:
    st.header("Browse Our Collection")
    st.markdown("Click on any wallpaper to view it in full size, then download it!")
    
    # Create a grid layout for wallpapers
    cols = st.columns(3)
    
    # Sample wallpaper URLs (replace with actual URLs)
    wallpaper_urls = [
        "https://images.unsplash.com/photo-1579546929518-9e396f3cc809",  # Gradient
        "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a",  # Galaxy
        "https://images.unsplash.com/photo-1497250681960-ef046c08a56e",  # Nature
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",  # Beach
        "https://images.unsplash.com/photo-1510784722466-f2aa9c52fff6",  # Mountain
        "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3",  # Abstract
        "https://images.unsplash.com/photo-1446776653964-20c1d3a81b06",  # Forest
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b",  # Mountains
        "https://images.unsplash.com/photo-1519681393784-d120267933ba",  # Snow
        "https://images.unsplash.com/photo-1554629947-334ff61d85dc",  # Mountains
        "https://images.unsplash.com/photo-1494500764479-0c8f2919a3d8",  # Sunset
        "https://images.unsplash.com/photo-1534447677768-be436bb09401",  # Abstract
        "https://images.unsplash.com/photo-1518837695005-2083093ee35b",  # Geometric
        "https://images.unsplash.com/photo-1508739773434-c26b3d09e071",  # Neon
        "https://images.unsplash.com/photo-1541701494587-cb58502866ab",  # Abstract
    ]
    
    wallpaper_names = [
        "Colorful Gradient", "Cosmic Galaxy", "Spring Bloom", 
        "Serene Beach", "Mountain Vista", "Abstract Waves",
        "Mystic Forest", "Alpine Heights", "Winter Wonderland",
        "Mountain Majesty", "Golden Sunset", "Geometric Dreams",
        "Sacred Geometry", "Neon City", "Color Splash"
    ]
    
    wallpaper_descriptions = [
        "A vibrant gradient of colors flowing smoothly",
        "A breathtaking view of deep space with stars and nebulae",
        "Beautiful flowers and plants in vibrant colors",
        "A peaceful beach scene with crystal clear water",
        "Magnificent mountain peaks at sunrise",
        "Abstract wave patterns in blue and purple",
        "Deep forest with sunlight streaming through trees",
        "Majestic mountain peaks reaching into the clouds",
        "Snow-covered landscape with beautiful lighting",
        "Mountain range with dramatic lighting and atmosphere",
        "Stunning sunset with vivid orange and red hues",
        "Abstract geometric patterns in harmonious colors",
        "Sacred geometry patterns in vibrant colors",
        "City skyline with neon lights and reflections",
        "A splash of vibrant colors in abstract patterns"
    ]
    
    wallpapers = []
    for i in range(min(15, len(wallpaper_urls))):
        wallpapers.append({
            "url": wallpaper_urls[i],
            "name": wallpaper_names[i],
            "description": wallpaper_descriptions[i]
        })
    
    # Display wallpapers in grid
    for i, wallpaper in enumerate(wallpapers):
        col_idx = i % 3
        with cols[col_idx]:
            st.image(wallpaper["url"], caption=wallpaper["name"], use_container_width=True)
            
            # When clicking on a wallpaper, show it in a larger view
            if st.button(f"View {wallpaper['name']}", key=f"view_{i}"):
                st.session_state.selected_wallpaper = wallpaper
    
    # Display the selected wallpaper if any
    if "selected_wallpaper" in st.session_state:
        st.markdown("---")
        st.header(st.session_state.selected_wallpaper["name"])
        st.markdown(st.session_state.selected_wallpaper["description"])
        st.image(st.session_state.selected_wallpaper["url"], use_container_width=True)
        
        # For actual implementation, you'd fetch the image data first
        if st.button("Download This Wallpaper"):
            with st.spinner("Preparing download..."):
                try:
                    # Get the image data
                    response = requests.get(st.session_state.selected_wallpaper["url"])
                    if response.status_code == 200:
                        img_data = response.content
                        st.markdown(
                            get_download_link(img_data, f"{st.session_state.selected_wallpaper['name']}.jpg"),
                            unsafe_allow_html=True
                        )
                    else:
                        st.error("Failed to prepare download. Please try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Tab 2: Generate AI wallpapers
with tab2:
    st.header("Generate Your Own Wallpaper")
    st.markdown("Use Google's Gemini AI to create a unique wallpaper based on your description!")
    
    # User inputs for image generation
    prompt = st.text_area("Describe the wallpaper you want:", 
                        placeholder="Example: A mountain landscape with a sunset and a lake")
    
    col1, col2 = st.columns(2)
    
    with col1:
        style = st.selectbox("Choose a style:", [
            "Realistic", "Cartoon", "Anime", "Abstract", "Pixel Art", 
            "Watercolor", "Oil Painting", "3D Render", "Minimalist"
        ])
    
    with col2:
        resolution = st.selectbox("Select resolution:", [
            "1280x720 (HD)", "1920x1080 (Full HD)", "2560x1440 (2K)"
        ])
    
    # Generate button
    if st.button("Generate Wallpaper with Gemini"):
        if prompt:
            with st.spinner("Creating your wallpaper with Gemini AI..."):
                # Initialize Gemini API
                if initialize_gemini():
                    # Generate image with Gemini
                    generated_image = generate_gemini_image(prompt, style)
                    
                    if generated_image is not None:
                        st.success("Wallpaper created successfully!")
                        st.image(generated_image, caption=f"{prompt} in {style} style", use_container_width=True)
                        st.markdown(get_download_link(generated_image, "gemini_wallpaper.png"), unsafe_allow_html=True)
                        
                        # Option to save to collection - Updated logic
                        if st.button("Save to My Library", key="save_generated"):
                            # Add the generated image bytes and a name to the library
                            st.session_state.personal_library.append({
                                "name": f"Generated: {prompt[:30]}...", # Use part of the prompt as name
                                "data": generated_image
                            })
                            st.success("Wallpaper saved to My Library!")
                    else:
                        # Fallback to colored image if API fails
                        st.warning("Could not generate image with Gemini. Showing a placeholder instead.")
                        fallback_image = generate_colored_image()
                        st.image(fallback_image, caption="Placeholder Image", use_container_width=True)
                else:
                    st.error("Failed to initialize Gemini API. Please check your API key.")
        else:
            st.warning("Please enter a description for your wallpaper.")
    
    # Show some example prompts for inspiration
    with st.expander("Need inspiration? Try these prompts"):
        st.markdown("""
        - A futuristic city skyline with neon lights
        - Space scene with planets and a colorful nebula
        - Underwater coral reef with tropical fish
        - Abstract geometric patterns in blue and purple
        - Peaceful forest with sunlight streaming through trees
        - Mountain landscape with snow peaks and northern lights
        """)

# Tab 3: Personal Library
with tab3:
    st.header("My Personal Wallpaper Library")
    st.markdown("Upload your own wallpapers or view saved ones.")

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload your wallpapers (PNG, JPG, JPEG):",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Read image data
            img_data = uploaded_file.getvalue()
            # Add to personal library (avoid duplicates based on name for simplicity)
            if not any(item['name'] == uploaded_file.name for item in st.session_state.personal_library):
                st.session_state.personal_library.append({
                    "name": uploaded_file.name,
                    "data": img_data
                })
        st.success(f"Added {len(uploaded_files)} new wallpaper(s) to your library!")
        # Clear the uploader after processing to prevent re-adding on rerun
        # Note: Streamlit doesn't have a direct way to clear the uploader widget state easily after processing.
        # The check above helps prevent duplicates on subsequent interactions within the same session.

    st.markdown("---")
    st.subheader("Your Saved Wallpapers")

    if not st.session_state.personal_library:
        st.info("Your library is empty. Upload some images or save generated ones!")
    else:
        # Display library images in a grid
        num_library_cols = 3 # Adjust as needed
        library_cols = st.columns(num_library_cols)
        for i, item in enumerate(st.session_state.personal_library):
            col_idx = i % num_library_cols
            with library_cols[col_idx]:
                st.image(item["data"], caption=item["name"], use_container_width=True)
                # Add download link for each library image
                st.markdown(
                    get_download_link(item["data"], item["name"]),
                    unsafe_allow_html=True
                )
                # Optional: Add a remove button
                if st.button(f"Remove {item['name']}", key=f"remove_{i}"):
                    st.session_state.personal_library.pop(i)
                    st.rerun() # Rerun the script to update the display immediately

# Add a sidebar with additional options
with st.sidebar:
    st.header("About")
    st.markdown("This app was created to provide Chromebook wallpapers for students without requiring Google search.")
    
    st.header("Instructions")
    st.markdown("""
    1. Browse our collection of pre-made wallpapers
    2. Or generate your own using Google's Gemini AI
    3. Click on any wallpaper to view it in full size
    4. Download your favorite wallpapers
    """)
    
    # API Configuration
    st.header("API Configuration")
    with st.expander("Configure Gemini API"):
        api_key_input = st.text_input("Gemini API Key", type="password")
        if st.button("Save API Key"):
            os.environ["GEMINI_API_KEY"] = api_key_input
            st.success("API Key saved for this session")
    
    st.markdown("---")
    st.markdown("Created with ❤️ for our school by Nevaan Kant( Entity303 )")