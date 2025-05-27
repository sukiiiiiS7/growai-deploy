from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime
from achievement_config import ACHIEVEMENTS

env_path = Path(__file__).parent / ".env_user"
load_dotenv(dotenv_path=env_path)
MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)

db = client["user_data"]
achievement_log = db["achievement_log"]
users = db["users"]
lottery_log = db["lottery_log"]

def get_achievements(user_id: str):
    unlocked = list(achievement_log.find({"user_id": user_id}))
    unlocked_ids = [u["achievement_id"] for u in unlocked]

    enriched = []
    for ach in ACHIEVEMENTS:
        if ach["id"] in unlocked_ids:
            enriched.append({
                "id": ach["id"],
                "name": ach["name"],
                "description": ach["description"],
                "icon": ach["icon"],
                "points": ach["points"],
                "animate": ach.get("animate", False),
                "unlocked": True
            })

    user = users.find_one({"user_id": user_id}) or {}
    total_points = user.get("achievement_points", 0)

    return {
        "user_id": user_id,
        "total_points": total_points,
        "unlocked_achievements": enriched
    }

# Run lottery if user has 100+ points; result is weighted
def check_and_draw_lottery(user_id: str):
    user = users.find_one({"user_id": user_id})
    if not user:
        return {"error": "user not found"}

    points = user.get("achievement_points", 0)
    if points < 100:
        return {"status": "not enough points"}

    import random

    # Reward pool and probability weights
    prize_ids = [
        "digital_stamp_A",
        "digital_stamp_B",
        "full_physical_set",
        "full_physical_set_seed"
    ]
    weights = [0.5, 0.3, 0.15, 0.05]  # Most common → rarest

    # Labels shown to user
    PRIZE_INFO = {
        "digital_stamp_A": "Hidden Digital Stamp A",
        "digital_stamp_B": "Hidden Digital Stamp B",
        "full_physical_set": "Full Physical Stamp Set",
        "full_physical_set_seed": "Full Set + Dream Seed Bottle"
    }

    # Choose one reward
    chosen_id = random.choices(prize_ids, weights=weights, k=1)[0]
    reward_label = PRIZE_INFO[chosen_id]

    # Log the result
    lottery_log.insert_one({
        "user_id": user_id,
        "reward_id": chosen_id,
        "reward_label": reward_label,
        "timestamp": datetime.utcnow()
    })

    # Deduct points
    users.update_one({"user_id": user_id}, {"$inc": {"achievement_points": -100}})

    return {
        "user_id": user_id,
        "reward": reward_label,
        "reward_id": chosen_id,
        "status": "lottery triggered"
    }
def get_achievement_progress(user_id: str):
    user = users.find_one({"user_id": user_id})
    if not user:
        return {"error": "user not found"}

    points = user.get("achievement_points", 0)
    percent = min(100, int((points / 100) * 100))
    can_draw = points >= 100

    return {
        "user_id": user_id,
        "points": points,
        "progress_percent": percent,
        "can_draw": can_draw
    }
