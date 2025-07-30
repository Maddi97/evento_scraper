#!/bin/bash
source venv/bin/activate  # Linux/macOS

uvicorn app.main:app --reload
