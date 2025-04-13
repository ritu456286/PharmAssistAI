#!/bin/bash

echo "Starting FastAPI Server..."

# Bind to all interfaces so Docker port mapping works
uvicorn src.main:app --host 0.0.0.0 --port 8000

echo "Server Stopped."
