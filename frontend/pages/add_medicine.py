import streamlit as st
from utils.api.medicine_apis import add_medicine
from datetime import date

def app():
    st.title("➕ Add New Medicine")

    name = st.text_input("Medicine Name")
    dosage = st.text_input("Dosage")
    quantity = st.number_input("Quantity", min_value=1, step=1, help="Enter a valid quantity (minimum 1)")
    price = st.number_input("Price", min_value=0.0, format="%.2f", help="Price cannot be negative")
    expiry_date = st.date_input("Expiry Date", min_value=date.today(), help="Expiry date must be in the future")

    # Validation before submission
    if st.button("Add Medicine"):
        if not name.strip():
            st.error("⚠️ Medicine name cannot be empty!")
        elif not dosage.strip():
            st.error("⚠️ Dosage cannot be empty!")
        elif price is None or price < 0:
            st.error("⚠️ Price must be a positive number!")
        elif expiry_date <= date.today():
            st.error("⚠️ Expiry date must be in the future!")
        else:
            # Call API if all validations pass
            with st.status("Adding medicine...", expanded=True) as status:
                success = add_medicine(name.strip(), dosage.strip(), quantity, price, str(expiry_date))
                
                if success:
                    status.update(label="✅ Medicine added successfully!", state="complete", expanded=False)
                    st.rerun()
                else:
                    status.update(label="❌ Failed to add medicine. Please try again.", state="error", expanded=True)

if __name__ == "__main__":
    app()
