import streamlit as st
import pandas as pd
import time
from utils.api.invoice_apis  import get_all_invoices, delete_invoice

def app():
    """Streamlit Page to Display and Manage Invoices."""
    st.title("🧾 Invoice Management")

    # Fetch invoice data
    with st.spinner("Fetching invoices..."):
        invoices = get_all_invoices()

    if not invoices:
        st.warning("⚠️ No invoices found!")
        return

    # Convert data into a Pandas DataFrame
    df = pd.DataFrame(invoices)

    # Add Delete Buttons
    col1, col2 = st.columns([4, 1])

    with col1:
        st.subheader("📜 Invoice Records")

    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()

    # Display table with delete buttons
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 2, 2, 1])

        col1.write(row["id"])
        col2.write(row["patient_name"])
        col3.write(row["doctor_name"])
        col4.write(row["clinic_name"])
        col5.write(row["invoice_date"])
        col6.write(f"${row['total_amount']:.2f}")

        # Delete Button
        if col7.button("❌", key=f"delete_{row['id']}"):
            if f"deleted_{row['id']}" not in st.session_state:
                with st.spinner(f"Deleting Invoice {row['id']}..."):
                    success = delete_invoice(row["id"])
                    if success:
                        st.session_state[f"deleted_{row['id']}"] = True  # Mark as deleted
                        st.success(f"✅ Invoice {row['id']} deleted successfully!")
                        time.sleep(1)
                        st.rerun()  # Refresh page
                    else:
                        st.error("❌ Failed to delete invoice!")


    # Styling Table
    st.markdown("""
        <style>
        div[data-testid="column"] {
            text-align: center !important;
        }
        button[kind="primary"] {
            background-color: red !important;
        }
        </style>
    """, unsafe_allow_html=True)
