# Cross-Platform Productivity Suite

This repository hosts a set of applications starting with a basic To-Do list backend. The backend is built with [FastAPI](https://fastapi.tiangolo.com/) and provides simple CRUD endpoints for tasks.

## Running the Backend

Install dependencies and run the tests:

```bash
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
pytest
```

Start the development server:

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at `http://localhost:8000`.
