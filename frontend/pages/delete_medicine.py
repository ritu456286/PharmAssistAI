import streamlit as st
import requests
from utils.api.medicine_apis import delete_medicine

def app():
    st.title("❌ Delete Medicine")

    medicine_id = st.number_input("Enter Medicine ID to Delete", min_value=1, step=1)

    if st.button("Delete Medicine"):
        if medicine_id:
            with st.status(f"Deleting medicine ID {medicine_id}...", expanded=True) as status:
                success = delete_medicine(medicine_id)

                if success:
                    status.update(label=f"✅ Medicine ID {medicine_id} deleted successfully!", state="complete", expanded=False)
                    st.rerun()
                else:
                    status.update(label="❌ Failed to delete medicine. Please try again.", state="error", expanded=True)
        else:
            st.warning("⚠️ Please enter a valid Medicine ID.")

if __name__ == "__main__":
    app()
