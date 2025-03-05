#backend: fast api
from fastapi import FastAPI
from sqlalchemy.orm import close_all_sessions
from contextlib import asynccontextmanager
from src.configs.db_con import initialize_db, engine
from src.configs.log_config import configure_logging
from src.configs.scheduler import start_scheduler, stop_scheduler_on_shutdown
from src.routers import medicine_routes
from src.routers import chat_pharma_routes

# app = FastAPI()
# initialize_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()  # Initialize logging
    # Startup: Initialize the database
    print("[STARTUP] Initializing the database...")
    initialize_db()

    # Start the Cleanup Scheduler Automatically
    start_scheduler()
    print("[STARTUP] Background Cleanup Scheduler Started...")
    yield
    # Shutdown: Close all database sessions and dispose of the engine
    print("[SHUTDOWN] Closing database connections...")
    await stop_scheduler_on_shutdown()
    close_all_sessions()
    engine.dispose()
    print("[SHUTDOWN] Database connections closed successfully.")

app = FastAPI(lifespan=lifespan)

app.include_router(medicine_routes.router, prefix="/api/medicines", tags=["Medicines"])
app.include_router(chat_pharma_routes.router, prefix="/api/chat/pharma", tags=["Chatbot"])

@app.get("/")
def home():
    return {"message": "Welcome to DiagnoPharmAI"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)