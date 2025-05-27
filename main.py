from fastapi import FastAPI, File, Form, UploadFile
from avatar_uploader import upload_avatar, get_avatar, count_unread_dreams
from check_achievements import check_achievements
from achievement_api import get_achievements, check_and_draw_lottery
from achievement_api import get_achievement_progress


app = FastAPI()

@app.post("/upload_avatar")
async def upload_avatar_route(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    return await upload_avatar(user_id, file)

@app.get("/get_avatar/{user_id}")
def get_avatar_route(user_id: str):
    return get_avatar(user_id)

@app.get("/count_unread_dreams/{user_id}")
def count_unread_dreams_route(user_id: str):
    return count_unread_dreams(user_id)

@app.get("/check_achievements/{user_id}")
def trigger_achievement_check(user_id: str):
    check_achievements(user_id)
    return {"status": "checked"}

@app.get("/get_achievements/{user_id}")
def get_achievements_api(user_id: str):
    return get_achievements(user_id)

@app.get("/achievement_progress/{user_id}")
def achievement_progress_api(user_id: str):
    return get_achievement_progress(user_id)

@app.post("/draw_lottery/{user_id}")
def draw_lottery_api(user_id: str):
    return check_and_draw_lottery(user_id)

@app.get("/")
def root():
    return {"message": "Grow AI backend is running + achievement route included"}
