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
        <title>🌸 Task Dashboard</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #ffe4ec, #e0f7fa);
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .layout {{
                display: grid;
                grid-template-columns: 200px 1fr;
                width: 900px;
                gap: 15px;
            }}

            .sidebar {{
                background: white;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            }}

            .main {{
                display: flex;
                flex-direction: column;
                gap: 15px;
            }}

            .card {{
                background: white;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            }}

            h2 {{
                margin-top: 0;
            }}

            input {{
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ddd;
                width: 70%;
            }}

            button {{
                padding: 10px;
                border: none;
                border-radius: 10px;
                background: #ff8fab;
                color: white;
                cursor: pointer;
            }}

            button:hover {{
                background: #ff6f91;
            }}

            ul {{
                list-style: none;
                padding: 0;
            }}

            li {{
                background: #f9fafb;
                padding: 10px;
                border-radius: 12px;
                margin-bottom: 8px;
                display: flex;
                justify-content: space-between;
            }}

            .done {{
                text-decoration: line-through;
                color: gray;
            }}

            .time {{
                font-size: 10px;
                color: gray;
            }}

            .actions a {{
                margin-left: 5px;
                text-decoration: none;
            }}

            .stat {{
                font-size: 18px;
                margin: 10px 0;
            }}

        </style>
    </head>

    <body>

        <div class="layout">

            <!-- SIDEBAR -->
            <div class="sidebar">
                <h3>🌸 Planner</h3>
                <p style="font-size:12px;color:gray;">
                Stay productive ✨<br><br>
                • Plan your day<br>
                • Track progress<br>
                • Keep it cute 💖
                </p>
            </div>

            <!-- MAIN -->
            <div class="main">

                <!-- STATS -->
                <div class="card">
                    <h2>📊 Overview</h2>
                    <div class="stat">Total Tasks: {total}</div>
                    <div class="stat">Completed: {done}</div>
                </div>

                <!-- TO DO -->
                <div class="card">
                    <h2>📝 To-Do List</h2>

                    <form action="/add" method="post">
                        <input name="task" placeholder="Add task..." required>
                        <button>Add</button>
                    </form>

                    <ul>
    """

    if len(tasks) == 0:
        html += "<p>No tasks yet ✨</p>"
    else:
        for i, t in enumerate(tasks):
            style = "done" if t["done"] else ""

            html += f"""
            <li>
                <div class="{style}">
                    {t['text']}<br>
                    <span class="time">{t['time']}</span>
                </div>
                <div class="actions">
                    <a href="/toggle/{i}">✔️</a>
                    <a href="/delete/{i}">🗑️</a>
                </div>
            </li>
            """

    html += """
                    </ul>

                    <form action="/clear" method="post">
                        <button style="background:#ff4d6d;">Clear All</button>
                    </form>

                </div>

            </div>
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
        "time": datetime.now().strftime("%b %d • %H:%M")
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