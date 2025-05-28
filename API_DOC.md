# Grow AI – API Documentation

This document outlines all backend API endpoints for the **Achievement**, **Avatar**, and **Notification** systems of the Grow AI project. (Just for now.)

---

## Avatar Endpoints

### `POST /upload_avatar`
**Description:** Upload an avatar image for a user. Automatically triggers achievement check.  
**Input:**  
- Form:
  - `user_id` (string)  
  - `file` (.jpg, .png, .jpeg)  
**Output:**  
- `avatar_url`, success message, or error

### `GET /get_avatar/{user_id}`
**Description:** Retrieve the avatar image URL for a given user.  
**Input:**  
- URL path `user_id`  
**Output:**  
- `avatar_url` or error message

### `GET /count_unread_dreams/{user_id}`
**Description:** Returns the number of unread dream notifications.  
**Input:**  
- URL path `user_id`  
**Output:**  
- Integer (e.g., `2`)

---

## Achievement System Endpoints

### `GET /get_achievements/{user_id}`
**Description:** Return a list of all defined achievements, indicating which ones are unlocked.  
**Input:**  
- URL path `user_id`  
**Output:**  
- `user_id`  
- `total_points`  
- `unlocked_achievements`: list of  
  - `id`, `name`, `description`, `icon`, `points`, `animate`, `unlocked`

### `GET /get_achievement_progress/{user_id}`
**Description:** Returns current achievement points, progress percentage, and eligibility to draw.  
**Input:**  
- URL path `user_id`  
**Output:**  
- `points`, `progress_percent`, `can_draw`

### `GET /check_achievements/{user_id}`
**Description:** Manually run the achievement checker for the user.  
**Input:**  
- URL path `user_id`  
**Output:**  
- Message confirming check was run

### `DELETE /reset_achievements/{user_id}`
**Description:** Reset all user achievements and points (for testing only).  
**Input:**  
- URL path `user_id`  
**Output:**  
- Message confirming reset

---

## Lottery System Endpoints

### `GET /draw_lottery/{user_id}`
**Description:** Draw a reward if the user has at least 100 points. Deducts points.  
**Input:**  
- URL path `user_id`  
**Output:**  
- `reward_id`, `reward_label`, `status`

### `GET /get_lottery_history/{user_id}`
**Description:** Returns history of rewards the user has drawn.  
**Input:**  
- URL path `user_id`  
**Output:**  
- List of `reward_id`, `reward_label`, `timestamp`

---

## Animated Achievement Pop-up

### `GET /latest_animated_achievement/{user_id}`
**Description:** Fetch the most recent animated achievement unlocked (for visual display).  
**Input:**  
- URL path `user_id`  
**Output:**  
- `achievement_id`, `name`, `icon`, `unlocked_at`  
- Or: message if none found

---

## Notification & Dream Chat Endpoints

### `POST /chat/send_dream_chat`
**Description:** Send a dream message from one plant to another. Automatically notifies the target plant's user.  
If no `dream_text` is provided, the system will auto-generate one using poetic logic.  

**Input:** JSON body with:  
- `from_plant_id` (str)  
- `to_plant_id` (str)  
- `dream_text` (str, optional)

**Output:**  
- `status` (str)  
- `chat_id` (str)  
- `used_auto_generated` (bool)  
  - `true`: system auto-generated the `dream_text` (user left it blank)  
  - `false`: user/front-end manually submitted the `dream_text`


### `GET /chat/get_dream_chats/{plant_id}`
**Description:** Retrieve dream chats sent to a specific plant.  
**Input:**  
- URL path `plant_id`  
**Output:** List of dream chat objects

### `GET /chat/count_unread_dreams/{user_id}`
**Description:** Count number of unread "dream" notifications for this user (for red dot display).  
**Input:**  
- URL path `user_id`  
**Output:** Integer

### `GET /chat/get_dream_notifications/{user_id}`
**Description:** Fetch all unread "dream" notifications.  
**Input:**  
- URL path `user_id`  
**Output:** List of notification objects

### `POST /chat/clear_dream_notifications/{user_id}`
**Description:** Mark all unread dream notifications as read. Clears red dot.  
**Input:**  
- URL path `user_id`  
**Output:** Number of notifications cleared

---

## Notes
- All endpoints assume valid MongoDB records exist for the given `user_id`.
- Each reward draw costs **100 achievement points**.
- Animated achievements are defined via `animate: True` in config.
- Notifications are stored in `notification_log` with type `"dream"`.
- If no `dream_text` is provided in `/send_dream_chat`, the backend automatically generates one via `generate_dream_text()`.
  The API response will include `"used_auto_generated": true` to indicate that the content was system-generated.
