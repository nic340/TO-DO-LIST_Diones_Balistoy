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
        <title>🌷 Task Studio</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #ffe4ec, #e0f7fa);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .container {{
                width: 450px;
                background: white;
                border-radius: 20px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            }}

            h1 {{
                margin: 0;
                font-size: 24px;
            }}

            .top {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}

            .badge {{
                background: #ffe0f0;
                padding: 5px 10px;
                border-radius: 999px;
                font-size: 12px;
            }}

            .input-group {{
                display: flex;
                gap: 10px;
            }}

            input {{
                flex: 1;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ddd;
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
                margin-top: 20px;
            }}

            li {{
                background: #f9fafb;
                padding: 12px;
                border-radius: 12px;
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: 0.2s;
            }}

            li:hover {{
                transform: scale(1.02);
            }}

            .text {{
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
                font-size: 16px;
            }}

            .footer {{
                margin-top: 10px;
                text-align: right;
            }}

            .clear {{
                background: #ff4d6d;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <div class="top">
                <h1>🌷 Task Studio</h1>
                <div class="badge">{done}/{total} done</div>
            </div>

            <form action="/add" method="post" class="input-group">
                <input name="task" placeholder="Write something productive..." required>
                <button>＋</button>
            </form>

            <ul>
    """

    if len(tasks) == 0:
        html += "<p style='color:gray;'>No tasks yet ✨</p>"
    else:
        for i, t in enumerate(tasks):
            style = "done" if t["done"] else ""

            html += f"""
            <li>
                <div class="text {style}">
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

            <div class="footer">
                <form action="/clear" method="post">
                    <button class="clear">Clear All</button>
                </form>
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