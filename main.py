from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

tasks = []

@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <html>
    <head>
        <title>To-Do List</title>
    </head>
    <body>
        <h1>💖</h1>

        <form action="/add" method="post">
            <input type="text" name="task" placeholder="Enter task" required>
            <button type="submit">Add</button>
        </form>

        <ul>
    """

    for i, task in enumerate(tasks):
        html += f"<li>{task} <a href='/delete/{i}'>❌</a></li>"

    html += """
        </ul>
    </body>
    </html>
    """

    return html


@app.post("/add")
async def add_task(task: str = Form(...)):
    tasks.append(task)
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{task_id}")
async def delete_task(task_id: int):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return RedirectResponse("/", status_code=303)