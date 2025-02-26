import streamlit as st
import requests
import os 
from dotenv import load_dotenv
load_dotenv()

# FastAPI Backend URL
API_URL = os.getenv("BASE_URL") + "api/chat/pharma/"

def app():
    """Pharma Assistant Chatbot Page"""
    st.title("💊 Pharma Assistant Chatbot")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat Interface
    st.write("Ask your health-related queries, and the Pharma Assistant will help you!")

    # User Input
    user_message = st.text_input("You:", key="user_input")

    if st.button("Send"):
        if user_message.strip():
            try:
                with st.spinner("Pharma Bot is thinking... 💭"):
                    # Send request to FastAPI backend
                    response = requests.post(API_URL, json={"message": user_message})

                    if response.status_code == 200:
                        bot_reply = response.json().get("response", "Sorry, I couldn't understand.")
                    else:
                        bot_reply = "Error: Unable to get response from server."

                # Update chat history
                st.session_state.chat_history.append(("You", user_message))
                st.session_state.chat_history.append(("Pharma Bot", bot_reply))

                # Clear user input field
                st.query_params["user_input"] = ""

            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Display Chat History
    for sender, message in st.session_state.chat_history:
        with st.chat_message("assistant" if sender == "Pharma Bot" else "user"):
            st.write(f"**{sender}:** {message}")
