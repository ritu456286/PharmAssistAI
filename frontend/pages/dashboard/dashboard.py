import streamlit as st
import pandas as pd
import requests
from utils.api.medicine_apis import get_all_medicines

def app():
    st.title("📊 Medicine Inventory Dashboard")

    # Fetch medicines (expecting a list of dictionaries)
    medicines = get_all_medicines()

    # Convert list to DataFrame
    if medicines and isinstance(medicines, list):  
        medicines_df = pd.DataFrame(medicines)
    else:
        medicines_df = pd.DataFrame()  # Empty DataFrame if no data

    # Ensure 'id' exists before operations
    if "id" in medicines_df.columns:
        medicines_df["id"] = medicines_df["id"].astype(int)  # Ensure ID is int
        medicines_df = medicines_df.set_index("id")  # Set 'id' as index

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Add Medicine"):
            st.switch_page("pages/add_medicine.py")
    with col2:
        if st.button("❌ Delete Medicine"):
            st.switch_page("pages/delete_medicine.py")
    with col3:
        if st.button("✏️ Update Medicine"):
            st.switch_page("pages/update_medicine.py")

    # Search by ID
    search_id = st.text_input("🔍 Search by Medicine ID", "")

    # Display table only if DataFrame is not empty
    if not medicines_df.empty:
        if search_id and search_id.isdigit():
            medicines_df = medicines_df.loc[[int(search_id)]] if int(search_id) in medicines_df.index else pd.DataFrame()

        st.write("### 🏥 Medicine Inventory")
        st.dataframe(medicines_df, use_container_width=True)  # Hide index
    else:
        st.warning("⚠️ No medicines found in the inventory!")

if __name__ == "__main__":
    app()
