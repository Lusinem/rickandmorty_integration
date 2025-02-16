#!/bin/bash
echo "Starting FastAPI server..."
uvicorn sample_app.ram_api:app --reload
