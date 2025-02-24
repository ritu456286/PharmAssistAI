#backend: fast api
from src.configs.db_con import initialize_db
from fastapi import FastAPI
from src.routers import medicine_routes
from src.routers import chat_pharma_routes

app = FastAPI()
initialize_db()

app.include_router(medicine_routes.router, prefix="/api/medicine", tags=["Medicine"])
app.include_router(chat_pharma_routes.router, prefix="/api/chat/pharma", tags=["Chatbot"])

@app.get("/")
def home():
    return {"message": "Welcome to DiagnoPharmAI"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)