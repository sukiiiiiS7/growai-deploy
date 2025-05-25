# Grow AI – Backend Setup (`database/` Folder)

---

## Done

- [x] User avatar upload via `/upload_avatar` (upload image + user_id)
- [x] Get avatar by ID using `/get_avatar/{user_id}`
- [x] Red dot system for unread dream notifications via `/count_unread_dreams/{user_id}`
- [x] MongoDB integration for users, logs, dream chats
- [x] Light sensor POST/GET endpoint via `/lux` (real-time testable)

---

## MongoDB Setup

- Hosted on MongoDB Atlas (private)
- `.env_user` stores the connection string (excluded from Git)
- See [MongoDB Setup Wiki](https://git.arts.ac.uk/24043715/Grow-AI/wiki/MongoDB-Setup#mongodb-setup-for-grow-ai)

---

## API Test / Connect Guide

- Use FastAPI endpoints from local or deployed backend
- Sample dataset (`dream_record_log_labeled.json`) available on request
- S7 can assist with API simulation or test case setup

---

## Folder: `database/`

| File | What it does |
|------|---------------|
| `avatar_uploader.py` | Upload avatar, fetch avatar, red-dot logic |
| `user_db_manager.py` | Manage MongoDB user profiles |
| `community_db_manager.py` | Handle dream logs, chat logs, notification flags |
| `dream_db_logger.py` | Upload labeled dream records to MongoDB |
| `main.py` | FastAPI entry point for deployment |
| `requirements.txt` | Dependencies for deployment |
| `.gitignore` | Prevent sensitive files (e.g. `.env_user`) from uploading |
| `static/avatars/` | Local uploaded avatar images |

---

## FastAPI Example (Local)

Start locally with:

```bash
cd database
uvicorn main:app --reload
