import streamlit as st
import pandas as pd
from utils.api.alert_apis import get_all_alerts, update_alert

def app():
    st.title("🚨 Stock Alerts Management")
    st.write("Manage and update threshold values of medicines to receive alerts when stock is low.")

    # Custom CSS
    st.markdown("""
    <style>
    .search-input {
        padding: 10px;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        width: 100%;
        margin-bottom: 20px;
    }
    .stDataFrame {
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    # Fetch Alerts from Backend
    alerts = get_all_alerts()

    if not alerts:
        st.warning("⚠️ No active alerts found!")
        st.stop()

    # Convert JSON to DataFrame
    df = pd.DataFrame(alerts["alerts"])
    df.rename(columns={"medicine_id": "Medicine ID", "alert_quantity": "Alert Quantity", "status": "Alert Status"}, inplace=True)

    # Search Box
    search_query = st.text_input("🔍 Search by Medicine Name or Medicine ID", placeholder="Type here...", key="search", help="Search by Medicine Name or ID")

    # Filter Table
    if search_query:
        if search_query.isdigit():
            df = df[df["Medicine ID"] == int(search_query)]
        else:
            df = df[df["medicine_name"].str.contains(search_query, case=False, na=False)]

    # Editable Table
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        column_config={
            "Medicine ID": st.column_config.NumberColumn(disabled=True),
            "medicine_name": st.column_config.TextColumn(disabled=True),
            "Alert Quantity": st.column_config.NumberColumn(label="Threshold Quantity"),
            "Alert Status": st.column_config.TextColumn(disabled=True),
        },
        hide_index=True,
        height=500,
    )

    # Save Changes Button
    if st.button("💾 Save Changes"):
        updated = False
        for index, row in edited_df.iterrows():
            original_row = df.iloc[index]
            if row["Alert Quantity"] != original_row["Alert Quantity"]:
                success = update_alert(row["Medicine ID"], row["Alert Quantity"])
                if success:
                    updated = True
                    st.success(f"✅ Alert updated for Medicine ID {row['Medicine ID']}")
                else:
                    st.error(f"❌ Failed to update alert for Medicine ID {row['Medicine ID']}")

        if updated:
            st.rerun()
        else:
            st.info("ℹ️ No changes detected.")
