from fastapi import FastAPI

from app.routers import product
from app.routers import movement
from app.routers import stock

app = FastAPI()

@app.get("/")
async def main():
	return {"message": "Hello World"}

app.include_router(product.router)
app.include_router(movement.router)
app.include_router(stock.router)