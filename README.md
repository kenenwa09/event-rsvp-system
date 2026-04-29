# Event Management API

A RESTful API for creating and managing events and RSVPs, built with **FastAPI**, **SQLAlchemy (async)**, and **PostgreSQL**.

---

## Features

- Create events with optional flyer upload (PNG, JPG, JPEG, PDF)
- List all events
- RSVP to an event by name and email
- Retrieve all RSVPs for an event
- Async database access with SQLAlchemy and asyncpg
- Auto-creates database tables on startup
- Environment-based configuration

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL |
| Driver | asyncpg |
| Validation | Pydantic v2 |
| Settings | pydantic-settings |
| Testing | pytest, pytest-asyncio, httpx |

---

## Project Structure

```
event/
├── app/
│   ├── api/
│   │   ├── deps.py            # Form/file dependency for event creation
│   │   ├── events_api.py      # Event routes
│   │   └── rsvp_api.py        # RSVP routes
│   ├── core/
│   │   ├── config.py          # Settings loaded from .env
│   │   ├── db_async.py        # Async engine, session factory, Base
│   │   ├── db_sync.py         # Sync engine (available for tools/scripts)
│   │   └── deps.py            # get_async_db dependency
│   ├── model/
│   │   ├── event_model.py     # Event ORM model
│   │   └── rsvp_model.py      # Rsvp ORM model
│   ├── schemas/
│   │   ├── errors.py          # Custom exceptions
│   │   ├── event.py           # Event Pydantic schemas
│   │   └── rsvp.py            # RSVP Pydantic schemas
│   ├── service/
│   │   ├── event_service.py   # Event business logic
│   │   └── rsvp_service.py    # RSVP business logic
│   └── main.py                # App entry point, lifespan, routers
├── uploads/                   # Saved flyer files (auto-created)
├── conftest.py                # Pytest fixtures and test DB setup
├── pytest.ini                 # Pytest configuration
├── .env                       # Environment variables (not committed)
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL running locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/event.git
cd event
```

### 2. Create and activate a virtual environment

```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy asyncpg pydantic-settings pytest pytest-asyncio httpx
```

### 4. Create the databases

In your PostgreSQL shell or terminal:

```sql
CREATE DATABASE event;
CREATE DATABASE event_test;
```

### 5. Set up environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:yourpassword@localhost/event
DATABASE_URL_SYNC=postgresql://postgres:yourpassword@localhost/event
ENVIRONMENT=DEBUG
```

> Set `ENVIRONMENT=DEBUG` to see SQL queries printed in the terminal. Remove it or leave it empty in production.

### 6. Run the app

```bash
uvicorn app.main:app --reload
```

On startup, SQLAlchemy automatically creates the `events` and `rsvps` tables if they don't exist.

Visit **http://localhost:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

### Events

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/event` | Create a new event |
| `GET` | `/event/` | List all events |

#### POST `/event`

Accepts `multipart/form-data`:

| Field | Type | Required |
|---|---|---|
| `title` | string | Yes |
| `description` | string | Yes |
| `date` | string | Yes |
| `location` | string | Yes |
| `flyer` | file | No |

Supported flyer formats: `.png`, `.jpg`, `.jpeg`, `.pdf`

**Response `201`:**
```json
{
  "id": 1,
  "title": "Tech Conference",
  "description": "Annual tech event",
  "date": "2026-05-10",
  "location": "Lagos",
  "flyer": "a1b2c3d4-uuid.png"
}
```

---

### RSVPs

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/rsvp/{event_id}` | RSVP to an event |
| `GET` | `/rsvp/{event_id}` | Get all RSVPs for an event |

#### POST `/rsvp/{event_id}`

```json
{
  "name": "Chika Obi",
  "email": "chika@mail.com"
}
```

**Response `201`:**
```json
{
  "rsvps": [
    {
      "event_id": 1,
      "name": "Chika Obi",
      "email": "chika@mail.com"
    }
  ]
}
```

---

## Error Responses

| Status | Meaning |
|---|---|
| `404` | Event not found |
| `415` | Unsupported flyer file type |
| `422` | Validation error (missing fields, bad file) |

---

## Running Tests

Tests run against a separate `event_test` database, which is created and torn down automatically for each test.

```bash
pytest
```

To see detailed output:

```bash
pytest -v
```

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL_ASYNC` | Async PostgreSQL connection string | `postgresql+asyncpg://postgres:pass@localhost/event` |
| `DATABASE_URL_SYNC` | Sync PostgreSQL connection string | `postgresql://postgres:pass@localhost/event` |
| `ENVIRONMENT` | Set to `DEBUG` to enable SQL logging | `DEBUG` |

---

## Notes

- Uploaded flyers are saved to the `uploads/` folder with a UUID filename to avoid collisions.
- The `uploads/` folder is created automatically if it does not exist.
- The `.env` file should never be committed — add it to `.gitignore`.

---

## .gitignore recommendation

```
.env
uploads/
env/
__pycache__/
*.pyc
.pytest_cache/
```


## Acknowledgements

This project was developed as a semester Assement for the **School of Engineering** at [AltSchool Africa](https://altschoolafrica.com).  
It demonstrates backend development concepts including REST API design, async programming, ORM integration, and database management with PostgreSQL.