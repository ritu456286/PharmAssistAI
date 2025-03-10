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
    if "medicines" not in st.session_state or st.session_state.medicines is None:
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
        st.image(uploaded_file, caption="📷 Uploaded Image", use_container_width=True, output_format="PNG",  # Added output_format
                 )

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
        with st.container():
            st.markdown("<h3 class='section-title'>🏥 Extracted Prescription Details (Editable)</h3>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                patient_name = st.text_input("👤 Patient's Name:", st.session_state.extracted_data.get("Patient's Name") or "N/A")
                clinic_name = st.text_input("🏥 Clinic Name:", st.session_state.extracted_data.get("Clinic Name") or "N/A")
            with col2:
                doctor_name = st.text_input("👨‍⚕️ Doctor's Name:", st.session_state.extracted_data.get("Doctor's Name") or "N/A")
                date = st.text_input("📅 Date:", st.session_state.extracted_data.get("Date") or "3023-12-12")

        with st.container():
            st.markdown("<h4 class='section-title'>💊 Medicines Prescribed:</h4>", unsafe_allow_html=True)
            updated_medicines = st.session_state.medicines.copy() if st.session_state.medicines else []
 # Create a copy

            for i, med in enumerate(st.session_state.medicines or []): 
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    updated_medicines[i] = st.text_input(f"Medicine {i+1}:", med, key=f"med_{i}")
                with col2:
                    if st.button("❌", key=f"remove_{i}", help="Remove this medicine"):
                        st.session_state.medicines.pop(i)
                        st.rerun()

            new_medicine = st.text_input("➕ Add New Medicine:", key="new_med_input", value=st.session_state.new_med_input)
            if st.button("Add Medicine", key="add_med_button"):
                if new_medicine:
                    st.session_state.medicines.append(new_medicine)
                    st.rerun()

        # Updated Data Preview as Table
        if updated_data := {
            "Patient's Name": patient_name,
            "Medicines Prescribed": updated_medicines,
            "Doctor's Name": doctor_name,
            "Clinic Name": clinic_name,
            "Date": date
        }:
            with st.container():
                st.markdown("<h3 class='section-title'>📝 Updated Data Preview</h3>", unsafe_allow_html=True)
                df_preview = pd.DataFrame.from_dict(updated_data, orient='index', columns=['Value']).T

                # Apply custom column configuration for 'Medicines Prescribed'
                column_config = {
                    "Medicines Prescribed": st.column_config.Column(width="large") # You can also try 'auto' or a specific pixel width
                }
                st.dataframe(df_preview, column_config=column_config)


        if st.button("🔍 Check Availability", use_container_width=True):
            with st.spinner("⏳ Checking Inventory..."):
                med_availability_data = check_availabilty(list(set(updated_medicines)))
                st.session_state.med_availability = med_availability_data
                if med_availability_data:
                    st.success("✅ Medicine availability checked successfully.")
                    # print("Response from Backend:", st.json(med_availability_data))

        # Medicine Availability Section
        if st.session_state.med_availability:
            med_availability = st.session_state.med_availability

            with st.container():
                st.markdown("<h3 class='section-title'>📋 Medicine Availability</h3>", unsafe_allow_html=True)

                if med_availability:
                    with st.expander("✅ Available Medicines", expanded=bool(med_availability.get("available"))):
                        available_meds = med_availability.get("available", [])
                        if available_meds:
                            for med in available_meds:
                                st.markdown(f"""
                                    <div class='availability-box'>
                                        <p class='availability-title'>✅ Available: {med['name']} ({med['dosage']})</p>
                                        <p>Price: ₹{med['price']}</p>
                                        <p>Expiry: {med['expiry_date']}</p>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No medicines are available from the prescription.")

                    with st.expander("❌ Unavailable Medicines", expanded=bool(med_availability.get("unavailable"))):
                        unavailable_meds = med_availability.get("unavailable", [])
                        if unavailable_meds:
                    
                            st.write(", ".join(unavailable_meds))
                        else:
                            st.success("All prescribed medicines are available!")

                    with st.expander("🔄 Alternative Medicines", expanded=bool(med_availability.get("alternatives"))):
                        alternatives = med_availability.get("alternatives", [])
                        if alternatives:
                           
                            for alt in alternatives:
                                st.markdown(f"""
                                    <div class='availability-box'>
                                        <p class='availability-title'>🔄 Alternative for {alt['for_medicine']}: {alt['name']} ({alt['dosage']})</p>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.success("No alternatives available for unavailable medicines.")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🧾 Generate Invoice (Include Alternatives)", use_container_width=True):
                            st.session_state.invoice_medicines = available_meds + alternatives
                            st.rerun()
                    with col2:
                        if st.button("🧾 Generate Invoice (No Alternatives)", use_container_width=True):
                            st.session_state.invoice_medicines = available_meds
                            st.rerun()

        # Invoice Items Section
        if st.session_state.invoice_medicines:
            with st.container():
                st.markdown("<h3 class='section-title'>📝 Enter Quantity for Each Medicine</h3>", unsafe_allow_html=True)

                invoice_items = []
                unique_key = 1
                for idx, med in enumerate(st.session_state.invoice_medicines):
                    available_stock = med.get("quantity", 0)
                    unique_key += 1
                    col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
                    with col1:
                        st.write(f"**{med['name']} ({med['dosage']})** - ₹{med['price']} | Exp: {med['expiry_date']}")
                    with col2:
                        st.write(f"🗃️ Available: **{available_stock}** units")
                    with col3:
                        qty = st.number_input(
                            f"Quantity ({med['name']})",
                            min_value=0,
                            max_value=available_stock,
                            value=0,
                            key=unique_key
                        )
                        invoice_items.append({
                            "id": med.get("id"),
                            "name": med["name"],
                            "dosage": med["dosage"],
                            "quantity": qty,
                            "price": med["price"],
                            "total_price": med["price"] * qty
                        })

                if st.button("✅ Confirm Invoice", use_container_width=True):
                    filtered_medicines = {item["id"]: item["quantity"] for item in invoice_items if item["quantity"] > 0}
                    total_amount = sum(item["total_price"] for item in invoice_items if item["quantity"] > 0)

                    invoice_data = {
                        "patient_name": st.session_state.extracted_data.get("Patient's Name") or "N/A",
                        "doctor_name": st.session_state.extracted_data.get("Doctor's Name") or "N/A",
                        "clinic_name": st.session_state.extracted_data.get("Clinic Name") or "N/A",
                        "invoice_date": st.session_state.extracted_data.get("Date") or "3024-12-12",
                        "medicines": filtered_medicines,
                        "total_amount": total_amount
                    }
            
                    response = create_invoice(invoice_data)

                    if response:
                        st.session_state.invoice_response = response
                        st.session_state.invoice_items = invoice_items
                        st.success("🧾 Invoice Successfully Created!")
                        st.rerun()
                    else:
                        st.error("❌ Error creating invoice. Please try again.")

        # Invoice Details Section
        if "invoice_response" in st.session_state and st.session_state.invoice_response:
            invoice_data = st.session_state.invoice_response

            with st.container():
                st.markdown("<h2 class='invoice-title'>📜 Invoice Details</h2>", unsafe_allow_html=True)
                st.markdown(f"**🆔 Invoice ID:** {invoice_data['id']}")
                st.markdown(f"**📅 Date:** {invoice_data['invoice_date']}")
                st.markdown(f"**👤 Patient:** {invoice_data['patient_name']}")
                st.markdown(f"**👨‍⚕️ Doctor:** {invoice_data['doctor_name']}")
                st.markdown(f"**🏥 Clinic:** {invoice_data['clinic_name']}")

            with st.container():
                st.markdown("<h4 class='section-title'>💊 Medicines Bought</h4>", unsafe_allow_html=True)

                columns = ["Medicine ID", "Medicine Name", "Dosage", "Quantity", "Price per Unit (₹)", "Total Price (₹)"]
                medicine_table = []
                for med in st.session_state.invoice_items:
                    if med["quantity"] > 0:
                        medicine_table.append([
                            med["id"], med["name"], med.get("dosage", "N/A"),
                            med["quantity"], med["price"], med["total_price"]
                        ])

                df = pd.DataFrame(medicine_table, columns=columns)
                st.dataframe(df)

                st.markdown(f"<h3 style='color: #28a745;'>🏷️ **Total Amount:** ₹{invoice_data['total_amount']}</h3>", unsafe_allow_html=True)

                pdf_buffer = generate_invoice_pdf(invoice_data, st.session_state.invoice_items)
                st.download_button(
                    label="📥 Download Invoice as PDF",
                    data=pdf_buffer,
                    file_name=f"Invoice_{invoice_data['id']}.pdf",
                    mime="application/pdf"
        )

