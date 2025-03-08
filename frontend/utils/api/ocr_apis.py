import requests
import streamlit as st
from utils.api.api_config import OCR_ROUTES as BASE_URL

def process_image(file):
    """
    Sends an image file to the FastAPI OCR endpoint and returns the extracted data.

    Args:
        file: The uploaded image file from Streamlit.

    Returns:
        dict: JSON response containing extracted text or an error message.
    """
    if file is None:
        return {"error": "No file provided"}

    files = {"file": (file.name, file.getvalue(), file.type)}
    try:
        response = requests.post(f"{BASE_URL}/", files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
