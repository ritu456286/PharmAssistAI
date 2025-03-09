from  utils.api.alert_apis import get_all_alerts
import streamlit as st
import pandas as pd
from utils.api.medicine_apis import get_all_medicines, get_medicines_below_threshold
import plotly.express as px

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

    # ====== Table Data Preparation ======
    if medicines and isinstance(medicines, list):
        medicines_df = pd.DataFrame(medicines)
        
        if "id" in medicines_df.columns:
            medicines_df["id"] = medicines_df["id"].astype(int)
            medicines_df = medicines_df.set_index("id")

        # Reorder columns
        column_order = ["name", "dosage", "quantity", "price", "expiry_date"]
        medicines_df = medicines_df[column_order]
    else:
        st.warning("⚠️ No medicines found in the inventory!")
        medicines_df = pd.DataFrame()  
    
    # ====== Search Section with Refresh Button (Aligned Properly) ======
    st.markdown("---")
    col_search, col_refresh = st.columns([5, 1])  # Adjust width ratio

    with col_search:
        search_query = st.text_input("🔍 Search Medicines by ID, Name, Price, Quantity, etc.")

    with col_refresh:
        st.write("") 
        if st.button("🔄 Refresh", help="Click to refresh data", use_container_width=True):
            st.rerun()  

    if search_query:
        # Convert all values to string for search compatibility
        search_query = search_query.strip().lower()
        
        # Filter the DataFrame based on search query
        filtered_df = medicines_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False, na=False)).any(axis=1)
        
        medicines_df = medicines_df[filtered_df]
        
   # ====== Table Display ======
    with st.expander("🏥 **Medicine Inventory Table**", expanded=True):
        if not medicines_df.empty:
            st.dataframe(medicines_df, use_container_width=True)
        else:
            st.warning("⚠️ No medicines found in the inventory!")

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
        
    
   # ====== 📊 Charts Section ======
    if not medicines_df.empty:
        st.markdown("## 📈 Inventory Insights")
        # Fetch Alerts from Backend
        alerts = get_all_alerts()

        df_alerts = pd.DataFrame(alerts["alerts"])
        df_alerts.rename(columns={"medicine_id": "Medicine ID", "alert_quantity": "Threshold Quantity"}, inplace=True)
        medicines_df = medicines_df.merge(df_alerts, left_on="id", right_on="Medicine ID", how="left")

        # 📊 1. Bar Chart: Medicine Stock Levels with Alert Thresholds
        fig_stock = px.bar(medicines_df, x="name", y="quantity", 
                        title="📦 Medicine Stock Levels vs. Alert Thresholds", 
                        labels={"name": "Medicine Name", "quantity": "Stock Quantity"},
                        color="quantity", color_continuous_scale="viridis")

        # Add threshold lines as a scatter plot overlay
        fig_stock.add_trace(
            px.scatter(medicines_df, x="name", y="Threshold Quantity").data[0].update(marker=dict(color="red", size=8))
        )

        # Customize layout (tilt x-axis labels for readability)
        fig_stock.update_layout(
            xaxis_tickangle=-45,  # Rotate x-axis labels
            xaxis_title="Medicine Name",
            yaxis_title="Quantity",
            height=500
        )

        st.plotly_chart(fig_stock, use_container_width=True)


        # 🥧 3. Pie Chart: Medicine Stock Distribution
        if medicines_df["quantity"].sum() > 0:
            fig_pie = px.pie(medicines_df, names="name", values="quantity", 
                            title="📊 Medicine Stock Distribution", 
                            hole=0.4, 
                            labels={"name": "Medicine Name", "quantity": "Quantity"},
                            color_discrete_sequence=px.colors.qualitative.Set3)  # Colorful theme

            # Customize layout (Show names & percentages on chart)
            fig_pie.update_traces(textinfo="percent+label")

         

            st.plotly_chart(fig_pie, use_container_width=True)
