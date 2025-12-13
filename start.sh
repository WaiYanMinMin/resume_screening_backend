#!/bin/bash
# Start script for Railway deployment
PORT=${PORT:-8000}
uvicorn main:app --host 0.0.0.0 --port $PORT

