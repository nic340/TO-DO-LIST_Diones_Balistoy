from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import json, os
from datetime import datetime

app = FastAPI()
FILE = "tasks.json"

# Load tasks
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        tasks = json.load(f)
else:
    tasks = []

def save_tasks():
    with open(FILE, "w") as f:
        json.dump(tasks, f)


@app.get("/", response_class=HTMLResponse)
async def home(search: str = ""):
    filtered = [t for t in tasks if search.lower() in t["text"].lower()]

    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])

    html = f"""
    <html>
    <head>
        <title>💖 Smart To-Do</title>
        <style>
            body {{
                font-family: Arial;
                background: linear-gradient(to right, #ffe6f0, #fff);
                text-align: center;
                margin-top: 40px;
            }}
            .box {{
                background: white;
                padding: 25px;
                border-radius: 20px;
                width: 350px;
                margin: auto;
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
            }}
            input {{
                padding: 8px;
                border-radius: 10px;
                border: 1px solid #ccc;
                margin: 5px;
            }}
            button {{
                padding: 8px 12px;
                border: none;
                border-radius: 10px;
                background: #ff69b4;
                color: white;
                cursor: pointer;
            }}
            button:hover {{
                background: #ff1493;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            li {{
                margin: 10px 0;
                font-size: 14px;
            }}
            .done {{
                text-decoration: line-through;
                color: gray;
            }}
            a {{
                margin-left: 5px;
                text-decoration: none;
            }}
            .stats {{
                font-size: 12px;
                color: gray;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h2>💖 Smart To-Do List</h2>

            <p class="stats">Total: {total} | Done: {done}</p>

            <form method="get">
                <input name="search" placeholder="Search..." value="{search}">
                <button>Search</button>
            </form>

            <form action="/add" method="post">
                <input name="task" placeholder="New task" required>
                <button>Add</button>
            </form>

            <form action="/clear" method="post">
                <button style="background:red;">Clear All 🗑️</button>
            </form>

            <ul>
    """

    if len(filtered) == 0:
        html += "<p>No tasks found 😢</p>"
    else:
        for i, t in enumerate(tasks):
            if search.lower() not in t["text"].lower():
                continue

            style = "class='done'" if t["done"] else ""

            html += f"""
            <li {style}>
                {t['text']} <br>
                <small>{t['time']}</small><br>
                <a href='/toggle/{i}'>✔️</a>
                <a href='/delete/{i}'>❌</a>
                <a href='/edit/{i}'>✏️</a>
            </li>
            """

    html += """
            </ul>
        </div>
    </body>
    </html>
    """
    return html


@app.post("/add")
async def add_task(task: str = Form(...)):
    tasks.append({
        "text": task,
        "done": False,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_tasks()
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{task_id}")
async def delete_task(task_id: int):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks()
    return RedirectResponse("/", status_code=303)


@app.get("/toggle/{task_id}")
async def toggle_task(task_id: int):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
        save_tasks()
    return RedirectResponse("/", status_code=303)


@app.post("/clear")
async def clear_tasks():
    tasks.clear()
    save_tasks()
    return RedirectResponse("/", status_code=303)


@app.get("/edit/{task_id}", response_class=HTMLResponse)
async def edit_page(task_id: int):
    task = tasks[task_id]
    return f"""
    <form action="/edit/{task_id}" method="post">
        <input name="new_task" value="{task['text']}">
        <button>Save</button>
    </form>
    """


@app.post("/edit/{task_id}")
async def edit_task(task_id: int, new_task: str = Form(...)):
    tasks[task_id]["text"] = new_task
    save_tasks()
    return RedirectResponse("/", status_code=303)