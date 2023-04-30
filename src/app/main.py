from collections.abc import AsyncIterator

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index() -> Response:
    async def generator() -> AsyncIterator[str]:
        for i in range(10):
            yield f"Line {i}\n"

    return StreamingResponse(generator())


if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8000, reload=True)
