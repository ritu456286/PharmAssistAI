#backend: fast api
from fastapi import FastAPI
from sqlalchemy.orm import close_all_sessions
from contextlib import asynccontextmanager
from src.configs.db_con import initialize_db, engine
from src.configs.ai_agent_config import agent
from src.configs.log_config import configure_logging
from src.routers import medicine_routes, chat_pharma_routes, alert_routes, ai_agent_routes, ocr_routes, invoice_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    print("[STARTUP] Initializing the database...")
    initialize_db()
    agent
    try:
        yield  # App runs here
    finally:
        print("[SHUTDOWN] Closing database connections...")
        close_all_sessions()
        engine.dispose()
        print("[SHUTDOWN] Database connections closed successfully.")



app = FastAPI(lifespan=lifespan)

app.include_router(medicine_routes.router, prefix="/api/medicines", tags=["Medicines"])

app.include_router(ai_agent_routes.router, prefix="/api/agent", tags=["Agent"])

app.include_router(alert_routes.router, prefix="/api/alerts", tags=["Alerts"])

app.include_router(invoice_routes.router, prefix="/api/invoice", tags=["Invoice"])

app.include_router(ocr_routes.router, prefix="/api/process-image", tags=["OCR"])

app.include_router(chat_pharma_routes.router, prefix="/api/chat/pharma", tags=["Chatbot"])


@app.get("/")
def home():
    return {"message": "Welcome to DiagnoPharmAI"}


if __name__ == "__main__":
    import uvicorn
    try:
        print("[STARTING] Server is starting...")
        uvicorn.run("main:app", host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("[SHUTDOWN] Server stopped by CTRL+C")