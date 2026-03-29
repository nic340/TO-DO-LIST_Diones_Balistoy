from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import json, os
from datetime import datetime

app = FastAPI()
FILE = "tasks.json"

if os.path.exists(FILE):
    with open(FILE, "r") as f:
        tasks = json.load(f)
else:
    tasks = []

def save():
    with open(FILE, "w") as f:
        json.dump(tasks, f)


@app.get("/", response_class=HTMLResponse)
async def home():
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])

    html = f"""
    <html>
    <head>
        <title>TaskFlow</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #f5f7fb;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .app {{
                width: 420px;
                background: white;
                border-radius: 16px;
                padding: 25px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }}

            h1 {{
                margin: 0;
                font-size: 24px;
            }}

            .stats {{
                font-size: 13px;
                color: gray;
                margin-bottom: 15px;
            }}

            input {{
                width: 70%;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #ddd;
            }}

            button {{
                padding: 10px 12px;
                border: none;
                border-radius: 8px;
                background: #4f46e5;
                color: white;
                cursor: pointer;
            }}

            button:hover {{
                background: #4338ca;
            }}

            ul {{
                list-style: none;
                padding: 0;
                margin-top: 20px;
            }}

            li {{
                background: #f9fafb;
                padding: 12px;
                border-radius: 10px;
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            .left {{
                text-align: left;
            }}

            .done {{
                text-decoration: line-through;
                color: gray;
            }}

            .time {{
                font-size: 11px;
                color: gray;
            }}

            .actions a {{
                margin-left: 8px;
                text-decoration: none;
            }}

            .clear {{
                margin-top: 10px;
                background: #ef4444;
            }}
        </style>
    </head>

    <body>
        <div class="app">
            <h1>TaskFlow ✔️</h1>
            <div class="stats">Total: {total} | Completed: {done}</div>

            <form action="/add" method="post">
                <input name="task" placeholder="What needs to be done?" required>
                <button>Add</button>
            </form>

            <form action="/clear" method="post">
                <button class="clear">Clear All</button>
            </form>

            <ul>
    """

    if len(tasks) == 0:
        html += "<p style='color:gray;'>No tasks yet.</p>"
    else:
        for i, t in enumerate(tasks):
            style = "done" if t["done"] else ""

            html += f"""
            <li>
                <div class="left {style}">
                    {t['text']}<br>
                    <span class="time">{t['time']}</span>
                </div>
                <div class="actions">
                    <a href="/toggle/{i}">✔️</a>
                    <a href="/delete/{i}">❌</a>
                </div>
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
async def add(task: str = Form(...)):
    tasks.append({
        "text": task,
        "done": False,
        "time": datetime.now().strftime("%b %d, %H:%M")
    })
    save()
    return RedirectResponse("/", status_code=303)


@app.get("/toggle/{id}")
async def toggle(id: int):
    if 0 <= id < len(tasks):
        tasks[id]["done"] = not tasks[id]["done"]
        save()
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{id}")
async def delete(id: int):
    if 0 <= id < len(tasks):
        tasks.pop(id)
        save()
    return RedirectResponse("/", status_code=303)


@app.post("/clear")
async def clear():
    tasks.clear()
    save()
    return RedirectResponse("/", status_code=303)