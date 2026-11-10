```markdown
# KanMind Backend

A robust RESTful API backend built with **Django** and **Django REST Framework (DRF)** for the KanMind Kanban application.

---

## Features

- **Token Authentication**: Secure user authentication via DRF Auth tokens.
- **Board Management**: Create, read, update, and delete project boards.
- **Task Management**: Full task tracking including status choices (`to-do`, `in-progress`, `review`, `done`), priorities, due dates, and assignments.
- **Contacts**: Contact management with automatic initials generation for frontend UI rendering.
- **Comments**: Interactive comments linked to tasks with automated timestamps and author resolution.

---

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtualenv (recommended)

---

## Getting Started

Follow these steps to set up and run the project locally:

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd project.KanMind-main

```

2. **Create and activate a virtual environment:**
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Apply database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate

```


5. **Create a superuser (for Django Admin access):**
```bash
python manage.py createsuperuser

```


6. **Run the development server:**
```bash
python manage.py runserver

```



The API will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints

* **Authentication**: `/api-token-auth/` (POST to get token)
* **Boards**: `/api/boards/`
* **Contacts**: `/api/contacts/`
* **Tasks**: `/api/tasks/`
* **Comments**: `/api/comments/`

---

## License

This project is developed as part of the Developer Akademie training curriculum.

```

```