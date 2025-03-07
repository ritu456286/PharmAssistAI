"""
This file contains the services for the agentic_ai endpoints.
"""

from src.configs.ai_agent_config import agent
from pydantic import BaseModel
from fastapi import HTTPException

class QueryRequest(BaseModel):
    question: str

class AgentResponse(BaseModel):  # Use Pydantic for response
    query_result: str


async def get_answer_from_agent(query: QueryRequest):
    """
    Asynchronously sends a query to the AI agent and returns the response.
    Args:
        query (QueryRequest): An object containing the user's question.
    Returns:
        dict: A dictionary containing the agent's answer with the key "answer".
        str: An error message if an exception occurs.
    Raises:
        Exception: If there is an error invoking the agent.
    """
    
    
    print(f"User Question: {query.question}")
    
    try:
        result = await agent.ainvoke({"question": query.question, "attempts": 0})
        return AgentResponse(query_result=result["query_result"])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))