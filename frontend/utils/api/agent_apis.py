import requests
import streamlit as st
from utils.api.api_config import AGENT_ROUTES

def get_answer_from_agent(question):
    """
    API call to fetch the AI agent's response.
    """
    payload = {"question": question}
    try:
        response = requests.post(f"{AGENT_ROUTES}/", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Error: {response.status_code} - {response.json()['detail']}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Server Connection Error: {e}")
        return None
