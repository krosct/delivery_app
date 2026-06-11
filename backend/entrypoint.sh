#!/bin/sh
set -e

echo "Applying SQLAlchemy schema (delivery tables)..."
python -c "from core.database import init_db; init_db(); print('Schema ready.')"

exec uvicorn main:app --host 0.0.0.0 --port 8000
