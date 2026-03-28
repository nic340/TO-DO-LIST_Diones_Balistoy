from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

tasks = []

@app.get("/")
def read_tasks(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/add")
def add_task(request: Request, task: str = Form(...)):
    tasks.append(task)
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete/{task_id}")
def delete_task(task_id: int):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return RedirectResponse(url="/", status_code=303)