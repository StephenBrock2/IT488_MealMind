from fastapi import FastAPI

app = FastAPI()

count = 0

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/count")
async def countGet():
    global count
    count += 1
    return count


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}