# KanMind Backend

REST API for **KanMind**, a Kanban board application, built with **Django** and **Django REST Framework**.
This repository contains the backend only. The frontend is provided separately.

## Features

- Registration and login with email and password (token authentication)
- Boards with an owner and members
- Tasks with status, priority, due date, assignee and reviewer
- Comments on tasks
- Lists of tasks assigned to me or waiting for my review
- Email lookup to add existing users to a board

## Requirements

- Python 3.12 or higher
- pip

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AnnesMuhamed/KanMind.git
   cd KanMind
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   ```
   Windows:
   ```bash
   .venv\Scripts\activate
   ```
   macOS / Linux:
   ```bash
   source .venv/bin/activate
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the database**
   ```bash
   python manage.py migrate
   ```

5. **Create an admin user (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the server**
   ```bash
   python manage.py runserver
   ```

The API is now available at `http://127.0.0.1:8000/api/`.
The admin panel is available at `http://127.0.0.1:8000/admin/`.

## Connecting the frontend

The frontend must run on `http://127.0.0.1:5500` or `http://localhost:5500`,
for example with the VS Code extension **Live Server**.
Only these two addresses are allowed in `CORS_ALLOWED_ORIGINS` in `core/settings.py`.

## Authentication

All endpoints except registration and login require a token.
Send it in the header of every request:

```
Authorization: Token <your_token>
```

You receive the token in the response of `registration/` and `login/`.

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Log in with email and password |
| GET | `/api/boards/` | List all boards the user owns or is a member of |
| POST | `/api/boards/` | Create a board |
| GET | `/api/boards/{board_id}/` | Get a board with its members and tasks |
| PATCH | `/api/boards/{board_id}/` | Update the title and members of a board |
| DELETE | `/api/boards/{board_id}/` | Delete a board (owner only) |
| GET | `/api/email-check/?email=<email>` | Find a user by email |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/assigned-to-me/` | List tasks assigned to the user |
| GET | `/api/tasks/reviewing/` | List tasks the user has to review |
| PATCH | `/api/tasks/{task_id}/` | Update a task |
| DELETE | `/api/tasks/{task_id}/` | Delete a task (creator or board owner only) |
| GET | `/api/tasks/{task_id}/comments/` | List the comments of a task |
| POST | `/api/tasks/{task_id}/comments/` | Add a comment to a task |
| DELETE | `/api/tasks/{task_id}/comments/{comment_id}/` | Delete a comment (author only) |

## Permissions

- **Boards:** the owner and members can view and edit a board. Only the owner can delete it.
- **Tasks:** board members can create and edit tasks. Only the creator or the board owner can delete a task.
  Assignee and reviewer must be members of the board.
- **Comments:** board members can read and write comments. Only the author can delete a comment.

## Notes

- The email address is stored as the username, so users log in with their email.
- The database (`db.sqlite3`) is not part of the repository. Run `migrate` after cloning.

## License

This project was developed as part of the Developer Akademie training program.