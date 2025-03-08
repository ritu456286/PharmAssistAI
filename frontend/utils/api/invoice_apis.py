import requests
from utils.api.api_config import INVOICE_ROUTES as BASE_URL
import streamlit as st

def create_invoice(invoice_data):
    """
    API call to create the invoice
    """
    print("🔄 Sending Invoice Data to Backend: ", invoice_data)

    try:
        response = requests.post(f"{BASE_URL}/", json=invoice_data)

        # Ensure the response is valid JSON
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("❌ Error: Received invalid JSON from the server.")
            return None

        # Handle success
        if response.status_code == 200:
            print("✅ Invoice Created Successfully:", response_data)
            return response_data
        else:
            error_message = response_data.get("detail", "Unknown error")
            st.error(f"❌ Error: {response.status_code} - {error_message}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Server Connection Error: {e}")
        return None
