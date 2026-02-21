# MealMind

MealMind is a full-stack web application built with React (Vite) on the frontend and FastAPI (Python) on the backend. The backend can serve both the API and the built React frontend.

The project supports:
- Development Mode (separate frontend and backend servers)
- Single-Server Mode (everything served from port 8000)

---

## Project Structure

IT488_MealMind/
├── frontend/        # React (Vite)
├── backend_api/     # FastAPI backend
└── README.md

---

## Prerequisites

- Node.js (LTS recommended)
- Python 3.x
- pip
- (Windows users may use `py` launcher)

---

## Development Mode (Recommended)

In development mode:
- React runs on port 5173
- FastAPI runs on port 8000
- React connects to backend via `/api/*`

### Start Backend

Navigate to backend_api/

Create virtual environment (first time only):

Windows:
py -m venv venv
venv\Scripts\activate

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install fastapi uvicorn
pip install bcrypt

Navigate to backend_api/ and run:
uvicorn main:app --reload

Backend available at:
http://127.0.0.1:8000

Swagger docs:
http://127.0.0.1:8000/docs

---

### Start Frontend

Navigate to frontend/

Install dependencies:
npm install

Run dev server:
npm run dev

Frontend available at:
http://localhost:5173

---

## Single-Server Mode (Serve Everything from Port 8000)

Used for demo or deployment-style testing.

### 1. Build Frontend

From frontend/ run:
npm run build

This generates:
frontend/dist/

### 2. Copy Build to Backend

Copy frontend/dist into:
backend_api/frontend_dist

Windows example:
rmdir /S /Q backend_api\frontend_dist
xcopy /E /I /Y frontend\dist backend_api\frontend_dist

### 3. Ensure FastAPI Serves the Frontend

In backend_api/main.py ensure:

from fastapi.staticfiles import StaticFiles
from pathlib import Path

DIST_DIR = Path(__file__).parent / "frontend_dist"
app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="frontend")

All API routes should be defined under `/api/*`.

Example:
@app.get("/api/health")
def health():
    return {"ok": True}

### 4. Run Backend

uvicorn main:app --reload

Now everything runs from:
React UI: http://localhost:8000/
API: http://localhost:8000/api/health
Swagger Docs: http://localhost:8000/docs

---

## Current API Endpoints

GET /api/health – Health check  
GET /api/count – Incrementing counter  
GET /api/ingredient  
POST /api/ingredient  

---

## Notes

- Use Development Mode for daily coding.
- Use Single-Server Mode for demo.
- Rebuild frontend after modifying public assets.

---

## Tech Stack

- React
- Vite
- Material UI
- FastAPI
- Uvicorn
