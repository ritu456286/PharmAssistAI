import streamlit as st
from pages.dashboard import dashboard


st.set_page_config(page_title="Streamlit Dashboard", layout="wide")

def main():
    st.sidebar.title("🔄 Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Add Medicine", "Delete Medicine", "Update Medicine", "OCR Scanner", "Alert Management", "Chatbot"])

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
    elif page == "Alert Management":
        from pages.alert import alert
        alert.app()
    elif page == "OCR Scanner":
        from pages.ocr import ocr_page
        ocr_page.app()
    elif page == "Chatbot":
        from pages.chatbot import chat_pharma
        chat_pharma.app()
if __name__ == "__main__":
    main()