# creative-of-story
# 🧠 AI-Powered Store Story Generator (Creative Content Engine)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_square_white.svg)](https://creative-of-story-gaiwthmqz3a96bzd6tjish.streamlit.app/))
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

The **AI-Powered Store Story Generator** is a multi-modal application designed to create compelling, short-form marketing narratives directly from store interior or product imagery. Built using Streamlit and the Google Gemini API, this project automatically analyzes visual content and generates creative text designed to engage customers and drive sales.

This project successfully transitioned from local open-source models (YOLOv8 and local LLMs) to a robust external API solution to ensure high-quality, stable, and contextually accurate Turkish output.

## ✨ Key Features

* **Multi-Modal Analysis:** Directly analyzes image content (visual analysis) using the Gemini API (specifically, `gemini-2.5-flash`).
* **Creative Content Generation:** Generates short, persuasive marketing stories (in Turkish) based on the detected products and scene.
* **Persistent Data Handling (Optional):** Saves generated story text to the local file system (`data/stories`).
* **Secure Deployment:** Utilizes Streamlit's `st.secrets` for secure management of the Gemini API Key.
* **User-Friendly Interface:** Built with Streamlit for fast and intuitive web interaction.

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend/App** | Streamlit | User interface and application flow management. |
| **Core AI Model** | Google Gemini API (2.5 Flash) | Multi-modal analysis, visual understanding, and text generation. |
| **Language** | Python 3.10+ | Primary development language. |
| **API/Secrets** | `google-genai`, `streamlit.secrets` | Secure API connection and key management. |
| **Image Handling** | PIL (Pillow) | Handling image objects for API transmission. |

## 🚀 Getting Started

Follow these steps to set up and run the project locally or deploy it to Streamlit Community Cloud.

### Prerequisites

1.  Python 3.10+
2.  A valid **Gemini API Key** from [Google AI Studio](https://ai.google.dev/).

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YOUR-USERNAME]/creative-of-store.git
    cd creative-of-store
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### API Key Configuration

The application uses Streamlit's `st.secrets` for API key management, which works both locally (via `.streamlit/secrets.toml`) and on the Cloud.

1.  Create a folder named `.streamlit` in the project root.
2.  Inside the folder, create a file named `secrets.toml`.
3.  Add your Gemini API Key to this file:
    ```toml
    # .streamlit/secrets.toml
    [gemini]
    api_key = "YOUR_GEMINI_API_KEY_HERE"
    ```

### Running the Application

Start the Streamlit application from your terminal:

```bash
streamlit run app.py
