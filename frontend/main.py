import streamlit as st


st.set_page_config(page_title="Streamlit Dashboard", layout="wide")

def main():
    st.sidebar.title("🔄 Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Ask Agent", "OCR Scanner", "Chatbot", "Alert Management", "Invoice Management"])

    if page == "Dashboard":
        from pages.dashboard import dashboard
        dashboard.app()
    elif page == "Ask Agent":
        from pages.chatbot import inventory_agent
        inventory_agent.app()
    elif page == "Alert Management":
        from pages.alert import alert
        alert.app()
    elif page == "OCR Scanner":
        from pages.ocr import ocr2_page
        ocr2_page.app()
    elif page == "Chatbot":
        from pages.chatbot import chat_pharma
        chat_pharma.app()
    elif page == "Invoice Management":
        from pages.invoice import invoice
        invoice.app()
if __name__ == "__main__":
    main()