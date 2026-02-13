from fastapi import FastAPI

from app.ui import run_ui_with

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# Mount NiceGUI at /ui — open /ui in the browser for the classifier agent interface
run_ui_with(app, mount_path="/ui")