from fastapi import FastAPI
from uvicorn import run

app = FastAPI(title="Тест")


@app.get("/")
def main():
    return "Hello from test-helper!"


if __name__ == "__main__":
    run(app=app)
