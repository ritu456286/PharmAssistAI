from fastapi import APIRouter, HTTPException
from src.services.chat_pharma_service import pharma_chat_service

router = APIRouter()

@router.post("/")
async def chat_with_pharma(user_input: dict):
    """Handles chatbot API requests for Pharma Assistant."""
    try:
        user_message = user_input.get("message", "")
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required.")

        response = pharma_chat_service.chat_with_pharma_assistant(user_message)
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))