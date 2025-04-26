# Cool Chromebook Wallpapers Streamlit App 🖼️

This is a Streamlit application designed to provide cool wallpapers for Chromebooks, especially for environments where direct web searching might be restricted.

## Features

*   **Browse Collection:** View a curated list of wallpapers fetched from Unsplash.
*   **Generate AI Wallpapers:** Use Google's Gemini AI (requires API key configuration) to generate unique wallpapers based on text prompts and style choices. (Note: Current Gemini integration might primarily return text or placeholders).
*   **My Library:** Upload your own favorite wallpapers or save generated ones to a personal collection within the app session.
*   **Download:** Easily download any wallpaper from the collection, generated results, or your personal library.

## Running the App

1.  **Prerequisites:**
    *   Python 3.8+
    *   pip (Python package installer)

2.  **Clone the repository (Optional):**
    ```bash
    git clone <your-repository-url>
    cd HD_wallpaper_bank
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(You might need to create a `requirements.txt` file based on your imports: `streamlit`, `requests`, `numpy`, `google-generativeai`, `matplotlib`)*

4.  **Set up API Key (Optional, for AI Generation):**
    *   You can enter your Gemini API key directly in the sidebar of the running application.
    *   Alternatively, set it as an environment variable: `set GEMINI_API_KEY=YOUR_API_KEY` (Windows) or `export GEMINI_API_KEY=YOUR_API_KEY` (Linux/macOS).

5.  **Run the Streamlit app:**
    ```bash
    streamlit run .streamlit/main.py
    ```

6.  Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

## Project Structure

*   `.streamlit/main.py`: The main Streamlit application code.
*   `README.md`: This file.
*   `.gitignore`: Specifies intentionally untracked files for Git.