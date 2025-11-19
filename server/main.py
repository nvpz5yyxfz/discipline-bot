from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from database import init_db, add_answer, get_stats
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="server/templates")

init_db()

@app.post("/answer")
async def answer(data: dict):
    user_id = data["user_id"]
    answer = data["answer"]
    date = datetime.utcnow().strftime("%Y-%m-%d")
    add_answer(user_id, date, answer)
    return {"status": "ok"}

@app.get("/stats", response_class=HTMLResponse)
async def stats(request: Request):
    data = get_stats()
    table = {}
    for user_id, date, answer in data:
        if user_id not in table:
            table[user_id] = {}
        table[user_id][date] = answer
    all_dates = sorted({d for _, d, _ in data})
    return templates.TemplateResponse("stats.html", {"request": request, "table": table, "dates": all_dates})

