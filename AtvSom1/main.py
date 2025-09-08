import random
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/teste")
async def funcaoteste():
    return {"teste": True, "num_aleatorio": random.randint(0, 1000)}