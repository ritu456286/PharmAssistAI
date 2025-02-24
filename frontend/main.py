import streamlit as st
from pages.dashboard import dashboard


st.set_page_config(page_title="Streamlit Dashboard", layout="wide")

def main():
    st.sidebar.title("🔄 Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Add Medicine", "Delete Medicine", "Update Medicine"])

    if page == "Dashboard":
        dashboard.app()
    elif page == "Add Medicine":
        from pages import add_medicine
        add_medicine.app()
    elif page == "Delete Medicine":
        from pages import delete_medicine
        delete_medicine.app()
    elif page == "Update Medicine":
        from pages import update_medicine
        update_medicine.app()

if __name__ == "__main__":
    main()