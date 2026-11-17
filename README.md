# PeerBoard – Academic Questions and Answers API

PeerBoard is a database-backed REST API built with **Python, FastAPI, SQLModel, and PostgreSQL**. It provides a platform for students to create academic questions, browse discussions, and manage question-related information.

This project was developed as part of **SWE 4538 – Server Programming Lab 02**.

## Technologies Used

- **Python 3.10+** – Backend programming language
- **FastAPI** – REST API framework
- **SQLModel** – Database models and ORM
- **PostgreSQL** – Relational database
- **Docker & Docker Compose** – Database containerization
- **Uvicorn** – ASGI server
- **python-dotenv** – Environment variable management

## Project Features

- Create and manage student users.
- Create academic questions.
- Retrieve all available questions.
- Retrieve a specific question by ID.
- Update existing questions.
- Delete questions.
- Store question tags as JSON data.
- Maintain relationships between users, questions, and answers.
- Persist data using PostgreSQL.

## Project Structure

```text
PeerBoard/
│
├── main.py              # FastAPI application and API endpoints
├── models.py            # Database models (User, Question, Answer)
├── database.py          # Database connection and session management
├── docker-compose.yml   # PostgreSQL Docker configuration
├── .env                 # Environment variables (not committed)
├── .env.example         # Example environment configuration
├── .gitignore           # Files excluded from Git
└── README.md            # Project documentation
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Atik-Shahriar007/PeerBoard.git
cd PeerBoard
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install fastapi sqlmodel "psycopg[binary]" python-dotenv uvicorn
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_DB=peerboard
DATABASE_URL=postgresql+psycopg://your_database_user:your_database_password@localhost:5433/peerboard
```

Replace the placeholder credentials with your own values.

### 5. Start PostgreSQL Using Docker

Make sure Docker Desktop is running, then execute:

```bash
docker compose up -d
```

Check whether the database container is running:

```bash
docker compose ps
```

### 6. Run the FastAPI Application

```bash
fastapi dev main.py
```

Alternatively:

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides interactive API documentation through Swagger UI.

After starting the server, visit:

**http://127.0.0.1:8000/docs**

You can explore and test the available API endpoints directly from your browser.

## Core API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Create a new user |
| POST | `/questions` | Create a new question |
| GET | `/questions` | Retrieve all questions |
| GET | `/questions/{question_id}` | Retrieve a specific question |
| PUT | `/questions/{question_id}` | Update a question |
| DELETE | `/questions/{question_id}` | Delete a question |

## Database Models

PeerBoard uses three main database models:

**1. User**
- `id`
- `name`
- `email`
- `role`

**2. Question**
- `id`
- `title`
- `body`
- `course_code`
- `tags`
- `author_id`
- `accepted_answer_id`
- `created_at`
- `updated_at`

**3. Answer**
- `id`
- `question_id`
- `author_id`
- `body`
- `created_at`
- `updated_at`

These models establish relationships between users, academic questions, and their answers.

## Database Persistence

PostgreSQL runs inside a Docker container with a named volume to preserve database records.

Data remains available even after restarting the FastAPI application or stopping and restarting the database container.

## Author

**Atik Shahriar**

Department of Computer Science and Engineering  
Islamic University of Technology (IUT)

GitHub: [@Atik-Shahriar007](https://github.com/Atik-Shahriar007)

---

*Developed for SWE 4538 – Server Programming Lab 02.*
