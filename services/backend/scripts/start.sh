#!/bin/ash

uvicorn src.entrypoint.presentation.main:app --host 0.0.0.0 --port 8000
