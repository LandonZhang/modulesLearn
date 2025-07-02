from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"greeting": "Nice to meet you! My friend."}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, host="0.0.0.0")
