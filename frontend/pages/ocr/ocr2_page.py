import streamlit as st
from utils.api.ocr_apis import process_image
from utils.api.medicine_apis import check_availabilty
from utils.api.invoice_apis import create_invoice
from utils.generate_pdf import generate_invoice_pdf
import pandas as pd

def app():
    st.title("📄 OCR Prescription Scanner")

    # Initialize session state 
    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = None
    if "medicines" not in st.session_state:
        st.session_state.medicines = []
    if "new_med_input" not in st.session_state:
        st.session_state.new_med_input = "" 
    if "med_availability" not in st.session_state:
        st.session_state.med_availability = None
    if "invoice_medicines" not in st.session_state:
        st.session_state.invoice_medicines = []

    uploaded_file = st.file_uploader("Upload a prescription image", type=["jpg", "jpeg", "png"],
                                     help="Upload an image of a prescription to extract text")

    if uploaded_file:
        st.image(uploaded_file, caption="📷 Uploaded Image", use_container_width=True)

        if st.button("🔍 Extract Text", use_container_width=True):
            with st.spinner("⏳ Processing..."):
                extracted_data = process_image(uploaded_file)

            if "error" in extracted_data:
                st.error(f"❌ Error: {extracted_data['error']}")
            else:
                st.success("✅ Text Extracted Successfully!")
                st.session_state.extracted_data = extracted_data
                st.session_state.medicines = extracted_data.get("Medicines Prescribed", [])

    # Display editable fields only if data is extracted
    if st.session_state.extracted_data:
        st.markdown("### 🏥 Extracted Prescription Details (Editable)")

        # Editable Fields
        patient_name = st.text_input("👤 Patient's Name:", st.session_state.extracted_data.get("Patient's Name", ""))
        doctor_name = st.text_input("👨‍⚕️ Doctor's Name:", st.session_state.extracted_data.get("Doctor's Name", ""))
        clinic_name = st.text_input("🏥 Clinic Name:", st.session_state.extracted_data.get("Clinic Name", ""))
        date = st.text_input("📅 Date:", st.session_state.extracted_data.get("Date", ""))

        # Medicines List - Editable, Add & Remove Option
        st.markdown("**💊 Medicines Prescribed:**")
        updated_medicines = st.session_state.medicines[:] # Create a copy

        for i, med in enumerate(st.session_state.medicines):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                updated_medicines[i] = st.text_input(f"Medicine {i+1}:", med, key=f"med_{i}")
            with col2:
                if st.button("❌", key=f"remove_{i}", help="Remove this medicine"):
                    st.session_state.medicines.pop(i)
                    st.rerun()

        # Add new medicine option
        new_medicine = st.text_input("➕ Add New Medicine:", key="new_med_input", value=st.session_state.new_med_input) # Use value from session state
        if st.button("Add Medicine", key="add_med_button"):
            if new_medicine:
                st.session_state.medicines.append(new_medicine)
                st.rerun() 

        # Updated JSON Object
        updated_data = {
            "Patient's Name": patient_name,
            "Medicines Prescribed": updated_medicines,
            "Doctor's Name": doctor_name,
            "Clinic Name": clinic_name,
            "Date": date
        }

        # Display updated JSON object
        st.markdown("### 📝 Updated Data Preview")
        st.json(updated_data)

        # Check availability button
        if st.button("🔍 Check Availability", use_container_width=True):

            with st.spinner("⏳ Checking Inventory..."):
                med_availability_data = check_availabilty(list(set(updated_medicines)))
                st.session_state.med_availability = med_availability_data
                if med_availability_data:
                    st.success("✅ Medicine availability checked successfully.")
                    print("Response from Backend:", st.json(med_availability_data))
                    
        # If Medicine Availability Data is Available
        if st.session_state.med_availability:
            med_availability = st.session_state.med_availability

            st.markdown("### 📋 Medicine Availability")
            available_meds = med_availability.get("available", [])
            unavailable_meds = med_availability.get("unavailable", [])
            alternatives = med_availability.get("alternatives", [])

            # Show Available Medicines
            if available_meds:
                st.markdown("**✅ Available Medicines:**")
                for med in available_meds:
                    st.write(f"- {med['name']} ({med['dosage']}), Price: {med['price']}, Expiry: {med['expiry_date']}")

            # Show Unavailable Medicines
            if unavailable_meds:
                st.markdown("**❌ Unavailable Medicines:**")
                st.write(", ".join(unavailable_meds))

            # Show Alternative Medicines
            if alternatives:
                st.markdown("**🔄 Alternative Medicines:**")
                for alt in alternatives:
                    st.write(f"- {alt['name']} ({alt['dosage']}) as an alternative for {alt['for_medicine']}")

            # Generate Invoice Buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🧾 Generate Invoice (Include Alternatives)"):
                    st.session_state.invoice_medicines = available_meds + alternatives
                    st.rerun()
            with col2:
                if st.button("🧾 Generate Invoice (No Alternatives)"):
                    st.session_state.invoice_medicines = available_meds
                    st.rerun()

        # If Invoice Medicines Selected
        if st.session_state.invoice_medicines:
            st.markdown("### 📝 Enter Quantity for Each Medicine")

            invoice_items = []
            unique_key = 1
            for idx, med in enumerate(st.session_state.invoice_medicines):  # Use index for uniqueness
                available_stock = med.get("quantity", 0)  # Get available stock
                unique_key += 1
                col1, col2, col3 = st.columns([0.5, 0.3, 0.2])  # Three-column layout
                with col1:
                    st.write(f"**{med['name']} ({med['dosage']})** - ₹{med['price']} | Exp: {med['expiry_date']}")
                with col2:
                    st.write(f"🗃️ Available: **{available_stock}** units")  # Display available quantity
                with col3:
                    qty = st.number_input(
                        f"Quantity ({med['name']})",
                        min_value=0,
                        max_value=available_stock,  # Prevent exceeding available stock
                        value=0,
                        key=unique_key  # Use unique key
                    )
                    invoice_items.append({
                        "id": med.get("id"),
                        "name": med["name"],
                        "dosage": med["dosage"],
                        "quantity": qty,
                        "price": med["price"],
                        "total_price": med["price"] * qty
                    })

            if st.button("✅ Confirm Invoice"):
            # Prepare data for API
                filtered_medicines = {item["id"]: item["quantity"] for item in invoice_items if item["quantity"] > 0}
                total_amount = sum(item["total_price"] for item in invoice_items if item["quantity"] > 0)

                invoice_data = {
                    "patient_name": st.session_state.extracted_data.get("Patient's Name", ""),
                    "doctor_name": st.session_state.extracted_data.get("Doctor's Name", ""),
                    "clinic_name": st.session_state.extracted_data.get("Clinic Name", ""),
                    "invoice_date": st.session_state.extracted_data.get("Date", ""),
                    "medicines": filtered_medicines,
                    "total_amount": total_amount
                }

                # Send data to backend
                response = create_invoice(invoice_data)

                if response:
                    st.session_state.invoice_response = response  # Store response
                    st.session_state.invoice_items = invoice_items  # Store invoice items
                    st.success("🧾 Invoice Successfully Created!")
                    st.rerun()
                else:
                    st.error("❌ Error creating invoice. Please try again.")

    # If invoice is successfully created, show invoice box
    if "invoice_response" in st.session_state and st.session_state.invoice_response:
        invoice_data = st.session_state.invoice_response

        st.markdown("## 📜 Invoice Details")
        st.markdown(f"**🆔 Invoice ID:** {invoice_data['id']}")
        st.markdown(f"**📅 Date:** {invoice_data['invoice_date']}")
        st.markdown(f"**👤 Patient:** {invoice_data['patient_name']}")
        st.markdown(f"**👨‍⚕️ Doctor:** {invoice_data['doctor_name']}")
        st.markdown(f"**🏥 Clinic:** {invoice_data['clinic_name']}")

        st.markdown("### 💊 Medicines Bought")

        # Define column names
        columns = ["Medicine ID", "Medicine Name", "Dosage", "Quantity", "Price per Unit (₹)", "Total Price (₹)"]

        # Create table data
        medicine_table = []
        for med in st.session_state.invoice_items:
            if med["quantity"] > 0:
                medicine_table.append([
                    med["id"], med["name"], med.get("dosage", "N/A"),
                    med["quantity"], med["price"], med["total_price"]
                ])

        # Convert to DataFrame and display
        df = pd.DataFrame(medicine_table, columns=columns)
        st.table(df)

        st.markdown(f"## 🏷️ **Total Amount:** ₹{invoice_data['total_amount']}")

        # Generate and Provide PDF Download Button
        pdf_buffer = generate_invoice_pdf(invoice_data, st.session_state.invoice_items)
        st.download_button(
            label="📥 Download Invoice as PDF",
            data=pdf_buffer,
            file_name=f"Invoice_{invoice_data['id']}.pdf",
            mime="application/pdf"
)


