import requests
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

BASE_URL = os.getenv("BASE_URL") + "api/medicine" # Adjust if running on a different port

def add_medicine(name: str, dosage: str, quantity: int, price: float, expiry_date: str):
    """
    Sends a POST request to add a new medicine.
    """
    data = {
        "name": name,
        "dosage": dosage,
        "quantity": quantity,
        "price": price,
        "expiry_date": expiry_date,
    }
    
    try:
        response = requests.post(BASE_URL, json=data)
        if response.status_code == 200 or response.status_code == 201:
            return True
        else:
            st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Server Connection Error: {e}")
        return False


def get_all_medicines():
    """
    Fetches all medicines from the backend.
    """
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching medicines: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Server Connection Error: {e}")
        return []


def delete_medicine(medicine_id: int):
    """
    Sends a DELETE request to remove a medicine by ID.
    """
    try:
        response = requests.delete(f"{BASE_URL}/{medicine_id}")
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            st.warning("Medicine not found.")
            return False
        else:
            st.error(f"Failed to delete medicine: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Server Connection Error: {e}")
        return False


def update_medicine(medicine_id: int, updated_data: dict):
    """
    Sends a PATCH request to update medicine details.
    """
    try:
        print("updated data in frontend", updated_data)
        response = requests.patch(f"{BASE_URL}/{medicine_id}", json=updated_data)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            st.warning("Medicine not found.")
            return False
        else:
            st.error(f"Failed to update medicine: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Server Connection Error: {e}")
        return False
