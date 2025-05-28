# Grow AI – API Documentation

This document outlines all backend API endpoints for the **Achievement** and **Avatar** systems of the Grow AI project.(Just for now.)

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
- `unread_dreams` (integer)

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

## Notes
- All endpoints assume valid MongoDB records exist for the given `user_id`.
- Each reward draw costs **100 achievement points**.
- Animated achievements are defined via `animate: True` in config.
