from fastapi import FastAPI, Request

from app.run import call_agent
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


@app.post("/agent")
async def agent(request: Request):
    data = await request.json()
    user_input = data.get("user_input")
    model = data.get("model", "llama-3.3-70b-versatile")
    host = data.get("host", "cloud groq")
    call_agent(user_input, model, host)
    return {
        "response": "Finished Execution. \nPlease check the database for the result.",
        "url": "http://localhost:8000/ui",
    }
