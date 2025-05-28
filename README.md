# Grow AI – Backend Setup (`database/` Folder)

---

## Implemented Features

- [x] **User Avatar System**
  - Upload via `POST /upload_avatar` (`user_id` + `image`)
  - Query avatar via `GET /get_avatar/{user_id}`
- [x] **Unread Dream Notification**
  - `GET /count_unread_dreams/{user_id}` for red-dot frontend hint
- [x] **Achievement System (In Progress)**
  - Auto-check via `GET /check_achievements/{user_id}`
  - View unlocked achievements via `GET /get_achievements/{user_id}`
  - Visual progress bar via `GET /achievement_progress/{user_id}`
  - Lottery draw via `POST /draw_lottery/{user_id}` (≥100 points)
- [x] **MongoDB Cloud Integration**
  - Avatar URLs, user prefs, dream logs, notifications saved to MongoDB Atlas
- [x] **Sensor Endpoint**
  - `POST` + `GET /lux` API for logging light sensor data
- [x] **Render Deployment**
  - Hosted backend: [https://growai-backend.onrender.com](https://growai-backend.onrender.com)

---

## MongoDB Setup

- MongoDB hosted on **MongoDB Atlas**
- Local `.env_user` file stores private credentials (excluded via `.gitignore`)
- Refer to [MongoDB Setup Wiki](https://git.arts.ac.uk/24043715/Grow-AI/wiki/MongoDB-Setup#mongodb-setup-for-grow-ai)

---

## Folder Contents

| File | Description |
|------|-------------|
| `main.py` | FastAPI entrypoint with all routes registered |
| `avatar_uploader.py` | Avatar upload, get avatar URL, unread dream counter |
| `achievement_api.py` | Achievement visual data, progress bar, lottery draw |
| `check_achievements.py` | Backend logic for auto-unlocking achievements |
| `achievement_config.py` | Config for all achievements (name, icon, points) |
| `community_db_manager.py` | Logs plant actions, chats, notifications |
| `user_db_manager.py` | MongoDB handler for user profile and preferences |
| `dream_db_logger.py` | (Optional) For writing dream records to cloud DB |
| `static/avatars/` | Folder for uploaded avatar images |
| `.env_user` | Private MongoDB URI + user config (excluded from Git) |
| `requirements.txt` | Dependencies list for deployment |
| `README.md` | This file |

---


