import streamlit as st
from utils.api.agent_apis import get_answer_from_agent

def app():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
            body {
                font-family: 'Poppins', sans-serif;
                background-color: #f6f9fc;
            }
            .chat-container {
                padding: 20px;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                margin: 20px 0;
                animation: fadeIn 0.8s ease-in-out;
            }
            .chat-bot {
                color: #4CAF50;
                font-weight: bold;
            }
            .submit-btn {
                background: linear-gradient(135deg, #6dd5fa, #4CAF50);
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 12px;
                text-align: center;
                cursor: pointer;
                transition: background 0.3s ease-in-out;
            }
            .submit-btn:hover {
                background: linear-gradient(135deg, #4CAF50, #45a049);
            }
            @keyframes fadeIn {
                from {opacity: 0;}
                to {opacity: 1;}
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🤖 Inventory Agent Chatbot")
    st.markdown("<h4 style='color: #4CAF50;'>Welcome to the <b>PharmAssistAI</b> AGENT!</h4>", unsafe_allow_html=True)
    st.write("Ask your queries and perform actions on your inventory!")

    user_input = st.text_input("💬 Ask Inventory Agent Question", placeholder="Example: List the cheapest medicine")

    if st.button("🔍 Ask Agent", key="chatbot"):
        if user_input:
            with st.spinner("Asking Inventory Agent..."):
                response = get_answer_from_agent(user_input)

                if response:
                    st.markdown(f"""
                        <div class="chat-container">
                            <span class="chat-bot">🤖 {response['query_result']}</span>
                        </div>
                    """, unsafe_allow_html=True)

        else:
            st.warning("⚠️ Please enter your query first.")
