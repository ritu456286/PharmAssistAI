"""
This file contains the routers for the agentic_ai endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.ai_agent_service import get_answer_from_agent, QueryRequest, AgentResponse

router = APIRouter()



@router.post("/", response_model=AgentResponse)
async def ask_agent(query: QueryRequest):
    """
    Asynchronously sends a query to the AI agent and returns the response.
    """

    print(f"User Question: {query.question}")
    
    try:
        return await get_answer_from_agent(query)
    
    except HTTPException as e:
        raise e  # Re-raise HTTPException for FastAPI to handle
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))