from backend.src.configs.gemini_chat_config import get_gemini_model

class PharmaChatService:
    def __init__(self):
        self.model = get_gemini_model()
        self.chat_session = self.model.start_chat(history=[])

    def chat_with_pharma_assistant(self, user_input: str):
        """Sends a message to the chatbot and returns the response."""
        try:
            response = self.chat_session.send_message(user_input)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

# Singleton instance (to persist chat sessions)
pharma_chat_service = PharmaChatService()