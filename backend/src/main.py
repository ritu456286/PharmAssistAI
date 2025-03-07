#backend: fast api
from fastapi import FastAPI
from sqlalchemy.orm import close_all_sessions
from contextlib import asynccontextmanager
from src.configs.db_con import initialize_db, engine
from src.configs.log_config import configure_logging
# from src.configs.scheduler import start_scheduler, stop_scheduler_on_shutdown
from src.routers import medicine_routes, chat_pharma_routes, alert_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    print("[STARTUP] Initializing the database...")
    initialize_db()
    # start_scheduler()  # Start the scheduler automatically

    try:
        yield  # App runs here
    finally:
        print("[SHUTDOWN] Closing database connections...")
        # stop_scheduler_on_shutdown()  
        close_all_sessions()
        engine.dispose()
        print("[SHUTDOWN] Database connections closed successfully.")



app = FastAPI(lifespan=lifespan)

app.include_router(medicine_routes.router, prefix="/api/medicines", tags=["Medicines"])

app.include_router(chat_pharma_routes.router, prefix="/api/chat/pharma", tags=["Chatbot"])

app.include_router(alert_routes.router, prefix="/api/alerts", tags=["Alerts"])

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