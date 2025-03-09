import streamlit as st
from utils.api.agent_apis import get_answer_from_agent

def app():
    # Initialize chat history in session state
    if "agent_history" not in st.session_state:
        st.session_state.agent_history = []


    # Custom Styling for chat display
    st.markdown("""
        <style>
            
            .chat-container {
                padding: 10px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 12px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
                margin: 10px 0;
                animation: fadeIn 0.5s ease-in-out;
            }
            .chat-bot {
                color: #4CAF50;
                font-weight: bold;
            }
            .chat-user {
                color: #1E88E5;
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
    st.markdown("<h4>Welcome to <b>PharmAssistAI</b> AGENT!</h4>", unsafe_allow_html=True)
    st.write("Ask your queries and perform actions on your inventory!")

    # Chat Input
    user_input = st.text_input("💬 Ask Inventory Agent Question", placeholder="Example: List the cheapest medicine")

    if st.button("🔍 Ask Agent", key="chatbot"):
        if user_input:
            with st.spinner("Asking Inventory Agent..."):
                try:
                    response = get_answer_from_agent(user_input)

                    if response and "query_result" in response:
                        # Append user input & bot response to chat history
                        st.session_state.agent_history.append(("You", user_input))
                        st.session_state.agent_history.append(("Agent 🤖", response["query_result"]))
                    else:
                        st.session_state.agent_history.append(("You", user_input))
                        st.session_state.agent_history.append(("Agent 🤖", "Hi, the query is not understood."))

                except Exception as e:
                    st.session_state.agent_history.append(("You", user_input))
                    st.session_state.agent_history.append(("Agent 🤖", "Hi, the query is not understood."))  


    # Display Chat History
    st.subheader("📜 Chat History")
    chat_placeholder = st.container()

    with chat_placeholder:
        # Ensure user message is displayed first, then bot response
        history_pairs = list(zip(st.session_state.agent_history[::2], st.session_state.agent_history[1::2]))

        for (user_msg, bot_msg) in reversed(history_pairs):  # Reverse to show latest chats first
            st.markdown(f"""
                <div class="chat-container">
                    <span class="chat-user">{user_msg[0]}: {user_msg[1]}</span>
                </div>
                <div class="chat-container">
                    <span class="chat-bot">{bot_msg[0]}: {bot_msg[1]}</span>
                </div>
            """, unsafe_allow_html=True)


    # Button to Clear Chat History
    if st.button("🗑️ Clear Chat History"):
        st.session_state.agent_history = []
        st.rerun()  # Refresh UI to clear history
