# Event RSVP System API

A backend API built with FastAPI that allows users to create events and RSVP to them.
This project demonstrates REST API development, request validation, and project structure using Python and FastAPI.

## Project Overview

The Event RSVP System is a simple event management backend where:

- Users can create events
- Users can view all events
- Users can RSVP to events

This project is designed as a learning project for building APIs with FastAPI and organizing backend code into services, schemas, and storage layers.

## Features

- Create events
- View all events
- RSVP to events
- Upload optional event flyers
- Structured project architecture
- Error handling and validation
- Unit test support

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pytest (for testing)

## Project Structure

event/
│
├── app/
│ ├── api/ # API route handlers
│ ├── schemas/ # Request and response models
│ ├── service/ # Business logic
│ ├── storage/ # In-memory storage
│
├── tests/ # Unit tests
├── uploads/ # Uploaded event flyers
├── main.py # FastAPI application entry point
├── .gitignore
└── README.md

## Installation

Clone the repository:

git clone https://github.com/kenenwa09/event-rsvp-system.git

Move into the project folder:

cd event-rsvp-system

Create a virtual environment:

python -m venv env

Activate the environment:

Windows:

env\Scripts\activate

Install dependencies:

pip install fastapi uvicorn pytest

## ▶ Running the API

Start the FastAPI server:

uvicorn app.main:app --reload

The API will run at:

http://127.0.0.1:8000

## API Documentation

FastAPI automatically generates documentation.

Swagger UI:

http://127.0.0.1:8000/docs

Alternative Docs:

http://127.0.0.1:8000/redoc

## API Endpoints

### Create Event

POST /events/

Form Fields:

- `title`
- `description`
- `date`
- `location`
- `flyer` (optional file)

### Get All Events

GET /events/

Returns a list of all events.

### RSVP to an Event

POST /events/{event_id}/rsvp

Allows a user to RSVP for a specific event.

## Running Tests

Run the tests using:

pytest

Tests are located inside the `tests` folder.

## Future Improvements

- Add database support (PostgreSQL or MongoDB)
- Add authentication
- Add event editing and deletion
- Add RSVP user management

## Author

Kenechukwu Okeke

---

## License

This project is for educational purposes.(Project from ALTSCHOOL)
