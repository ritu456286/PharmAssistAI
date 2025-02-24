import datetime
import streamlit as st
from utils.api.medicine_apis import update_medicine

def app():
    st.title("✏️ Update Medicine")

    medicine_id = st.number_input("Enter Medicine ID to Update", min_value=1, step=1)

    name = st.text_input("New Name (leave blank to keep current)")
    dosage = st.text_input("New Dosage (leave blank to keep current)")
    quantity = st.number_input("New Quantity (leave blank to keep current)", min_value=0, step=1)
    price = st.number_input("New Price (leave blank to keep current)", min_value=0.0, format="%.2f")
    expiry_date = st.date_input("New Expiry Date (leave blank to keep current)", value=datetime.date.today())



    if st.button("Update Medicine"):
        if medicine_id:
            # Prepare data, excluding fields with None values
            data = {}
            if name.strip():
                data["name"] = name.strip()
            if dosage.strip():
                data["dosage"] = dosage.strip()
            if quantity > 0:
                data["quantity"] = quantity
            if price > 0:
                data["price"] = price
            if expiry_date > datetime.date.today():
                data["expiry_date"] = str(expiry_date)

            if not data:
                st.warning("⚠️ No changes detected. Please update at least one field.")
                return

            with st.status(f"Updating medicine ID {medicine_id}...", expanded=True) as status:
                success = update_medicine(medicine_id, data)

                if success:
                    status.update(label=f"✅ Medicine ID {medicine_id} updated successfully!", state="complete", expanded=False)
                    st.rerun()
                else:
                    status.update(label="❌ Failed to update medicine. Please try again.", state="error", expanded=True)


if __name__ == "__main__":
    app()
