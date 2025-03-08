import streamlit as st
import pandas as pd
import requests
from utils.api.medicine_apis import get_all_medicines, get_medicines_below_threshold

def app():
    st.title("📊 Medicine Inventory Dashboard")
    st.markdown("---")

    if "skip" not in st.session_state:
        st.session_state.skip = 0  # Start from Page 0
    limit = 10  # Fixed page size

   # Fetch Data
    medicines = get_all_medicines(skip=st.session_state.skip, limit=limit)
    below_threshold_medicines = get_medicines_below_threshold()

    # ====== Key Metrics ======
    total_meds = len(medicines) if medicines else 0
    low_stock_meds = len(below_threshold_medicines) if below_threshold_medicines else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Medicines", value=total_meds, delta=None)
    with col2:
        st.metric(label="Low Stock Medicines", value=low_stock_meds, delta="⚠️ Restock Needed" if low_stock_meds > 0 else "✅ All Good")


    # ====== Warning Section ======
    if below_threshold_medicines:
        with st.expander("⚠️ **Medicines Below Threshold**", expanded=True):
            st.warning("The following medicines are running low on stock. Please restock immediately!")

            # Create 3 column layout
            cols = st.columns(3)
            index = 0  # Initialize index

            threshold = 15  # Threshold value

            for med in below_threshold_medicines:
                progress = int((med["quantity"] / threshold) * 100)
                progress = min(progress, 100)

                # Force all medicines as Moderate or Critical
                if progress <= 40:
                    stock_status = "🔥 Critical Stock"
                    color = "#FF4B4B"  # Red
                else:
                    stock_status = "⚠️ Moderate Stock"
                    color = "#FFA500"  # Orange

                with cols[index % 3]:
                    st.markdown(
                        f"""
                        <div style="border: 2px solid {color}; 
                        border-radius: 12px; 
                        padding: 15px; 
                        margin: 10px 0; 
                        background-color: rgba(255, 75, 75, 0.1);
                        box-shadow: 2px 2px 8px rgba(255, 75, 75, 0.3);">
                        🔍 <strong>Name:</strong> {med['name']}<br>
                        💊 <strong>Dosage:</strong> {med['dosage']}<br>
                        📦 <strong>Quantity:</strong> {med['quantity']}<br>
                        🗓️ <strong>Expiry Date:</strong> {med['expiry_date']}<br>
                        💰 <strong>Price:</strong> {med['price']} INR<br>
                        <small>{stock_status}</small>
                        <div style="height: 10px; width: 100%; background: #ddd; border-radius: 10px; overflow: hidden; margin-top: 10px;">
                            <div style="height: 100%; width: {progress}%; background: {color}; text-align: center; color: white; font-weight: bold;">
                            </div>
                        </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                index += 1




    # ====== Search Section ======
    st.markdown("---")
    search_id = st.text_input("🔍 Search by Medicine ID")
    if search_id and not search_id.isdigit():
        st.warning("⚠️ Please enter a valid integer ID!")
        
    # ====== Table Section ======
    if medicines and isinstance(medicines, list):
        medicines_df = pd.DataFrame(medicines)
        if "id" in medicines_df.columns:
            medicines_df["id"] = medicines_df["id"].astype(int)
            medicines_df = medicines_df.set_index("id")

        if search_id and search_id.isdigit():
            medicines_df = medicines_df.loc[[int(search_id)]] if int(search_id) in medicines_df.index else pd.DataFrame()

        with st.expander("🏥 **Medicine Inventory Table**", expanded=True):
            st.dataframe(medicines_df, use_container_width=True)

            # ===== Pagination Buttons =====
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                if st.button("⬅️ Previous", key="prev_page") and st.session_state.skip > 0:
                    st.session_state.skip -= limit
                    st.rerun()

            with col3:
                if len(medicines) == limit:
                    if st.button("➡️ Next", key="next_page"):
                        st.session_state.skip += limit
                        st.rerun()
        
    else:
        st.warning("⚠️ No medicines found in the inventory!")

    # ====== Navigation Buttons ======
    st.markdown("---")
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    with nav_col1:
        if st.button("➕ Add Medicine"):
            st.switch_page("pages/add_medicine.py")
    with nav_col2:
        if st.button("❌ Delete Medicine"):
            st.switch_page("pages/delete_medicine.py")
    with nav_col3:
        if st.button("✏️ Update Medicine"):
            st.switch_page("pages/update_medicine.py")


if __name__ == "__main__":
    app()
