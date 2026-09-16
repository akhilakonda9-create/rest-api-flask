# Task 3 - REST API Development

## Objective
Develop a RESTful API using Flask with proper route design, JSON input/output, validation, error handling, SQLite database integration, and CRUD operations.

## Project Structure
```text
task3_rest_api_flask/
├── instance/
├── app.py
├── requirements.txt
└── README.md
```

## Setup
1. Install Python 3.
2. Open terminal in this folder.
3. Optional: create a virtual environment:
   `python -m venv venv`
4. Activate it:
   Windows: `venv\Scripts\activate`
   Linux/Mac: `source venv/bin/activate`
5. Install Flask:
   `pip install -r requirements.txt`
6. Start the API:
   `python app.py`

The API runs at `http://127.0.0.1:5000`.

## CRUD Endpoints

### 1. Create
POST `/tasks`

JSON:
```json
{
  "title": "Learn Flask",
  "description": "Complete REST API task",
  "completed": false
}
```

### 2. Read all
GET `/tasks`

### 3. Read one
GET `/tasks/1`

### 4. Update
PUT `/tasks/1`

JSON:
```json
{
  "title": "Learn Flask REST API",
  "description": "Task completed",
  "completed": true
}
```

### 5. Delete
DELETE `/tasks/1`

## Testing
Use Postman, Thunder Client in VS Code, or curl.

Example:
```bash
curl -X POST http://127.0.0.1:5000/tasks ^
-H "Content-Type: application/json" ^
-d "{"title":"Learn Flask","description":"Practice API","completed":false}"
```

Then:
```bash
curl http://127.0.0.1:5000/tasks
```

## Validation and Error Handling
- Invalid JSON -> HTTP 400
- Missing/empty title -> HTTP 400
- Wrong data types -> HTTP 400
- Missing task -> HTTP 404
- Successful create -> HTTP 201
- Successful read/update/delete -> HTTP 200

## Database
SQLite is used, so PostgreSQL is not required for this task. The database file is automatically created in `instance/tasks.db`.

## Submission
Upload this complete folder to a GitHub repository and submit:
1. GitHub repository URL
2. API documentation (this README)
3. Source code
