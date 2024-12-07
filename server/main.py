from fastapi import FastAPI  # type: ignore


app = FastAPI()


@app.get("/")
async def read_file():
    print("Reading file")
    return "Hello, worldddddd!"
