

# source venv/Scripts/activate

echo "Starting FastAPI Server..."

# Start the server with single process
uvicorn src.main:app --host 127.0.0.1 --port 8000

echo "Server Stopped."