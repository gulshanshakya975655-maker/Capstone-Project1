# 🚀 TaskFlow

TaskFlow is a full-stack task and project management platform built with **FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript**.

It provides task, user, and project management together with algorithm-based searching/sorting, AI-assisted Quick-Add, project statistics, benchmarking, and a responsive web dashboard.

## ✨ Features

* Create, read, update, and delete tasks
* Create, read, update, and delete users
* Create, read, update, and delete projects
* Search tasks using Linear Search or Binary Search
* Sort tasks by priority
* Sort tasks by due date
* Project task statistics
* AI Quick-Add for natural-language task creation
* Insertion Sort implementation
* Comparison counting for algorithms
* Algorithm verification script
* Benchmarking with 10, 500, and 3000 records
* Interactive Swagger API documentation
* SQLite database
* Responsive frontend
* Client-side validation
* LocalStorage caching

## 🛠️ Technologies

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn
* HTML5
* CSS3
* JavaScript

## 📁 Project Structure

```text
taskflow1/
├── backend/
│   ├── main.py
│   ├── algorithms.py
│   ├── check_algorithms.py
│   ├── benchmark.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── taskflow.db
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Setup

### 1. Create and activate virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start the backend

```powershell
cd backend
python -m uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔌 API Endpoints

### Tasks

| Method | Endpoint               | Purpose                              |
| ------ | ---------------------- | ------------------------------------ |
| POST   | `/tasks`               | Create a task                        |
| GET    | `/tasks`               | Get tasks                            |
| GET    | `/tasks?sort=priority` | Sort tasks by priority               |
| GET    | `/tasks?sort=due_date` | Sort tasks by due date               |
| GET    | `/tasks/search`        | Search tasks                         |
| GET    | `/tasks/{task_id}`     | Get one task                         |
| PUT    | `/tasks/{task_id}`     | Update a task                        |
| DELETE | `/tasks/{task_id}`     | Delete a task                        |
| POST   | `/tasks/quick-add`     | Create a task using natural language |

### Users

| Method | Endpoint           | Purpose     |
| ------ | ------------------ | ----------- |
| POST   | `/users`           | Create user |
| GET    | `/users`           | Get users   |
| PUT    | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

### Projects

| Method | Endpoint                       | Purpose                |
| ------ | ------------------------------ | ---------------------- |
| POST   | `/projects`                    | Create project         |
| GET    | `/projects`                    | Get projects           |
| GET    | `/projects/{project_id}/stats` | Get project statistics |
| PUT    | `/projects/{project_id}`       | Update project         |
| DELETE | `/projects/{project_id}`       | Delete project         |

### Algorithms

| Method | Endpoint                    | Purpose                       |
| ------ | --------------------------- | ----------------------------- |
| POST   | `/algorithms/sort`          | Run insertion sort            |
| GET    | `/algorithms/linear-search` | Run linear search             |
| GET    | `/algorithms/binary-search` | Run binary search             |
| POST   | `/algorithms/benchmark`     | Compare algorithm performance |

## 🤖 AI Quick-Add

TaskFlow supports deterministic natural-language Quick-Add.

Example:

```text
Finish report tomorrow, urgent
```

This is converted into a structured task with:

```text
Title: Finish report
Priority: high
Due Date: tomorrow
Status: pending
```

Another example:

```text
Prepare documentation next week
```

The parser extracts the task title and due-date information automatically.

## 🔎 Task Search

TaskFlow supports:

### Linear Search

```text
GET /tasks/search?title=ramesh&algo=linear
```

### Binary Search

```text
GET /tasks/search?title=ramesh&algo=binary
```

The API returns the matching task, index, and comparison count.

## 📊 Algorithm Benchmark

The benchmark script tests the algorithms with:

```text
10 records
500 records
3000 records
```

Run it with:

```powershell
cd backend
python benchmark.py
```

The benchmark reports comparison counts for:

* Insertion Sort
* Linear Search
* Binary Search

## 🧪 Algorithm Verification

Run:

```powershell
cd backend
python check_algorithms.py
```

The verification script checks sorting, searching, comparison counting, and input immutability.

Current verification result:

```text
RESULT: 12/12 checks passed
ALL ALGORITHM CHECKS PASSED
```

## 📈 Project Statistics

Project statistics are available through:

```text
GET /projects/{project_id}/stats
```

Example response:

```json
{
  "project_id": 1,
  "total": 2,
  "pending": 0,
  "completed": 2
}
```

## 🌐 Frontend

The frontend provides:

* Task creation and management
* Task search and filtering
* Priority and status controls
* User management
* Project management
* Statistics dashboard
* Responsive layout
* Client-side validation
* LocalStorage caching

Open the frontend through a local development server such as VS Code Live Server.

## 🧪 Testing Completed

The following functionality has been tested successfully:

* Task CRUD
* User CRUD
* Project CRUD
* Project statistics
* Task search
* Priority sorting
* Due-date sorting
* AI Quick-Add
* Algorithm verification
* Algorithm benchmarking

## 📌 Example Quick-Add

```text
Finish report tomorrow, urgent
```

Expected structured task:

```json
{
  "title": "Finish report",
  "priority": "high",
  "status": "pending"
}
```

## 📄 License

This project was created as a full-stack software engineering project for educational and demonstration purposes.

## Algorithm Benchmark Results

The benchmark was run with 10, 500, and 3000 records.

| Records | Insertion Sort | Linear Search | Binary Search |
|--------:|---------------:|--------------:|--------------:|
| 10 | 9 | 10 | 4 |
| 500 | 499 | 500 | 9 |
| 3000 | 2999 | 3000 | 12 |

The results show that linear search grows directly with the number of records,
while binary search requires far fewer comparisons after sorting. Insertion
sort is more expensive as the dataset grows, but TaskFlow users are expected
to sort their task list repeatedly while adding or renaming tasks less often.
Therefore, paying the sorting cost can be worthwhile when the sorted data is
searched repeatedly.
