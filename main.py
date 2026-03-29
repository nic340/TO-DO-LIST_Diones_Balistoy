from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

tasks = []

@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <html>
    <head>
        <title>💖 To-Do List</title>
        <style>
            body {
                font-family: Arial;
                background-color: #ffe6f0;
                text-align: center;
                margin-top: 50px;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 15px;
                width: 300px;
                margin: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input {
                padding: 8px;
                width: 70%;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            button {
                padding: 8px;
                border: none;
                background: #ff69b4;
                color: white;
                border-radius: 8px;
                cursor: pointer;
            }
            button:hover {
                background: #ff1493;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            a {
                color: red;
                text-decoration: none;
                margin-left: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>💖 My To-Do List</h2>

            <form action="/add" method="post">
                <input type="text" name="task" placeholder="Enter task" required>
                <button type="submit">Add</button>
            </form>

            <ul>
    """

    if len(tasks) == 0:
        html += "<p>No tasks yet 😢</p>"
    else:
        for i, task in enumerate(tasks):
            html += f"<li>{i+1}. {task} <a href='/delete/{i}'>❌</a></li>"

    html += """
            </ul>
        </div>
    </body>
    </html>
    """

    return html


@app.post("/add")
async def add_task(task: str = Form(...)):
    if task.strip() != "":
        tasks.append(task)
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{task_id}")
async def delete_task(task_id: int):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return RedirectResponse("/", status_code=303)