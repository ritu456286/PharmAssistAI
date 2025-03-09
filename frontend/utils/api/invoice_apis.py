import requests
from utils.api.api_config import INVOICE_ROUTES as BASE_URL
import streamlit as st

def create_invoice(invoice_data):
    """
    API call to create the invoice
    """
   
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
            
            return response_data
        else:
            error_message = response_data.get("detail", "Unknown error")
            st.error(f"❌ Error: {response.status_code} - {error_message}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Server Connection Error: {e}")
        return None

def get_all_invoices():
    """
    API call to fetch all invoices.
    Returns a list of invoice objects if successful, otherwise None.
    """
    try:
        response = requests.get(f"{BASE_URL}/")

        # Ensure the response is valid JSON
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("❌ Error: Received invalid JSON from the server.")
            return None

        # Handle success
        if response.status_code == 200:
            if isinstance(response_data, list):  # Ensure it's a list of invoices
                
                return response_data
            else:
                st.error("❌ Error: Unexpected response format from the server.")
                return None
        else:
            error_message = response_data.get("detail", "Unknown error")
            st.error(f"❌ Error: {response.status_code} - {error_message}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Server Connection Error: {e}")
        return None
    
def delete_invoice(invoice_id):
    """
    API call to delete an invoice by ID.
    """
    try:
        response = requests.delete(f"{BASE_URL}/{invoice_id}")

        # Handle success
        if response.status_code == 204:  # No Content (successful deletion)
       
            return True
        elif response.status_code == 404:
            st.error(f"❌ Error: Invoice {invoice_id} not found.")
            return False
        else:
            response_data = response.json()
            error_message = response_data.get("detail", "Unknown error")
            st.error(f"❌ Error: {response.status_code} - {error_message}")
            return False

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Server Connection Error: {e}")
        return False