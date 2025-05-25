# database/main.py
from fastapi import FastAPI
from avatar_uploader import upload_avatar, get_avatar, count_unread_dreams

app = FastAPI()

app.post("/upload_avatar")(upload_avatar)
app.get("/get_avatar/{user_id}")(get_avatar)
app.get("/count_unread_dreams/{user_id}")(count_unread_dreams)

@app.get("/")
def root():
    return {"message": "Grow AI backend is running"}
