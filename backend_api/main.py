from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel

app = FastAPI()

count = 0

class IngredientPydantic(BaseModel):
    name: str

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/count")
def count_get():
    global count
    count += 1
    return {"count": count}

@app.get("/api/ingredient")
def ingredient_get(name: str):
    return {"ingredients": [{"name": name}, {"name": f"{name} juice"}]}

@app.post("/api/ingredient")
def ingredient_put(ingredient: IngredientPydantic):
    return {"message": f"added ingredient {ingredient.name}"}

DIST_DIR = Path(__file__).parent / "frontend_dist"
app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="frontend")
