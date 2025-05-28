from fastapi import FastAPI, Body
from community_db_manager import add_dream_chat, chat_col, add_notification, get_plant_owner
from community_db_manager import count_unread_dreams, get_notifications, mark_notifications_read
import random

app = FastAPI()

def generate_dream_text():
    return random.choice([
        "In the silence between watering, I dreamed of rain that never ends.",
        "I saw roots entwined like forgotten stories beneath the earth.",
        "The stars whispered names I no longer remember, yet still grow toward.",
        "In my sleep, I turned light into longing.",
        "A bee visited me in a dream, humming truths I cannot speak.",
        "I dreamed I was a forest, not a single stem.",
        "I heard the footsteps of time in the falling of old petals.",
        "The wind carried a lullaby from a tree I’ve never met.",
        "In the dark, I bloomed with questions.",
        "I touched the shadow of the sun and it felt like home."
    ])

@app.post("/send_dream_chat")
def send_dream_chat(
    from_plant_id: str = Body(...),
    to_plant_id: str = Body(...),
    dream_text: str = Body(default=None) #Allow users not to pass.
):
    used_auto_generated = False

    if not dream_text or dream_text.strip() == "":
        dream_text = generate_dream_text()
        used_auto_generated = True
    chat_id = add_dream_chat(from_plant_id, to_plant_id, dream_text)
    #Notify the owners of the plants.
    to_user_id = get_plant_owner(to_plant_id)
    if to_user_id:
        add_notification(
            user_id=to_user_id,
            message=f"Your plant '{to_plant_id}' received a new dream.",
            notif_type="dream"
        )

    return {
        "status": "success",
        "chat_id": str(chat_id),
        "used_auto_generated": used_auto_generated # True = system generated the dream_text (user did NOT provide it)
                                                # False = user/front-end provided the dream_text manually
    }

@app.get("/get_dream_chats/{plant_id}")
def get_dream_chats(plant_id: str):
    chats = list(chat_col.find({"to_plant_id": plant_id}, {"_id": 0}))
    return {
        "to_plant_id": plant_id,
        "received_chats": chats
    }

@app.get("/count_unread_dreams/{user_id}")
def count_unread_dreams_route(user_id: str):
    return count_unread_dreams(user_id)

@app.get("/get_dream_notifications/{user_id}")
def get_dream_notifications(user_id: str):
    return get_notifications(user_id)

@app.post("/clear_dream_notifications/{user_id}")
def clear_dream_notifications(user_id: str):
    return {"cleared": mark_notifications_read(user_id)}