from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

count = 0

class IngredientPydantic(BaseModel):
    name: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/count")
async def countGet():
    global count
    count += 1
    return count

@app.get("/ingredient")
async def ingredientGet(name):
    sql.run('select * from ingredients where name like ?', name)
    return {"url": "ingredient",
            "ingredients":[
                {"name": name},
                {"name": f"{name} juice"}
            ]
            }


@app.post("/ingredient")
async def ingredientPut(ingredient: IngredientPydantic):
    return {"message": f"added ingredient {ingredient.name}", "name": ingredient.name}



@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

class Sql:
    def run(self, query, *params):
        pass

sql = Sql()

