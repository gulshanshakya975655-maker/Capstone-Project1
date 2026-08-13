# 🚀 TaskFlow

TaskFlow is a full-stack task and project management platform built with **FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript**.

It combines task, user, and project management with algorithm-based searching and sorting, AI-assisted Quick-Add, project statistics, algorithm verification, benchmarking, and a responsive web dashboard.

---

## ✨ Features

* ✅ Task CRUD operations
* ✅ Get individual task by ID
* ✅ User CRUD operations
* ✅ Project CRUD operations
* ✅ Search tasks using Linear Search
* ✅ Search tasks using Binary Search
* ✅ Sort tasks by priority
* ✅ Sort tasks by due date
* ✅ Project task statistics
* ✅ AI-assisted Quick-Add
* ✅ Insertion Sort implementation
* ✅ Comparison counting
* ✅ Algorithm verification
* ✅ Algorithm benchmarking
* ✅ Swagger API documentation
* ✅ SQLite database
* ✅ Responsive frontend
* ✅ Client-side validation
* ✅ LocalStorage caching
* ✅ API request timing middleware

---

## 🛠️ Tech Stack

| Technology | Purpose                |
| ---------- | ---------------------- |
| Python     | Backend programming    |
| FastAPI    | REST API framework     |
| SQLAlchemy | Database ORM           |
| SQLite     | Database               |
| Pydantic   | Data validation        |
| Uvicorn    | ASGI server            |
| HTML5      | Frontend structure     |
| CSS3       | Frontend styling       |
| JavaScript | Frontend functionality |

---

## 📁 Project Structure

```text
taskflow1/
│
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

---

# 🚀 Installation & Setup

## 1. Clone or open the project

Open PowerShell in the project directory:

```powershell
cd C:\Users\gulsh\Desktop\taskflow1
```

## 2. Create virtual environment

```powershell
python -m venv venv
```

## 3. Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## 5. Start the backend

Run this command from the **project root**:

```powershell
python -m uvicorn backend.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🔌 API Endpoints

## Tasks

| Method | Endpoint           | Description                        |
| ------ | ------------------ | ---------------------------------- |
| POST   | `/tasks`           | Create a task                      |
| GET    | `/tasks`           | List tasks                         |
| GET    | `/tasks/{task_id}` | Get a task                         |
| PUT    | `/tasks/{task_id}` | Update a task                      |
| DELETE | `/tasks/{task_id}` | Delete a task                      |
| GET    | `/tasks/search`    | Search tasks                       |
| POST   | `/tasks/quick-add` | Create task using natural language |

### Task Sorting

```text
GET /tasks?sort=priority
```

```text
GET /tasks?sort=due_date
```

---

## Users

| Method | Endpoint           | Description |
| ------ | ------------------ | ----------- |
| POST   | `/users`           | Create user |
| GET    | `/users`           | List users  |
| PUT    | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

---

## Projects

| Method | Endpoint                       | Description            |
| ------ | ------------------------------ | ---------------------- |
| POST   | `/projects`                    | Create project         |
| GET    | `/projects`                    | List projects          |
| PUT    | `/projects/{project_id}`       | Update project         |
| DELETE | `/projects/{project_id}`       | Delete project         |
| GET    | `/projects/{project_id}/stats` | Get project statistics |

---

## Algorithms

| Method | Endpoint                    | Description                   |
| ------ | --------------------------- | ----------------------------- |
| POST   | `/algorithms/sort`          | Run insertion sort            |
| GET    | `/algorithms/linear-search` | Run linear search             |
| GET    | `/algorithms/binary-search` | Run binary search             |
| POST   | `/algorithms/benchmark`     | Compare algorithm performance |

---

# 📚 API Examples

## Create Task

### Request

```http
POST /tasks
```

```json
{
  "title": "Finish monthly report",
  "priority": "high",
  "due_date": "tomorrow",
  "status": "pending",
  "project_id": 1
}
```

### Response

```json
{
  "id": 1,
  "title": "Finish monthly report",
  "priority": "high",
  "due_date": "tomorrow",
  "status": "pending",
  "project_id": 1
}
```

---

## Get Task

```http
GET /tasks/1
```

Example response:

```json
{
  "id": 1,
  "title": "Finish monthly report",
  "priority": "high",
  "due_date": "tomorrow",
  "status": "pending",
  "project_id": 1
}
```

---

## Update Task

```http
PUT /tasks/1
```

```json
{
  "title": "Finish updated monthly report",
  "priority": "medium",
  "due_date": "friday",
  "status": "pending",
  "project_id": 1
}
```

---

## Delete Task

```http
DELETE /tasks/1
```

Example response:

```json
{
  "message": "Task deleted successfully"
}
```

---

# 👤 User Example

Create a user:

```http
POST /users
```

```json
{
  "name": "Test User",
  "email": "test@example.com"
}
```

Update a user:

```http
PUT /users/1
```

```json
{
  "name": "Updated User",
  "email": "updated@example.com"
}
```

Delete a user:

```http
DELETE /users/1
```

---

# 📁 Project Example

Create a project:

```http
POST /projects
```

```json
{
  "name": "TaskFlow Development",
  "owner_id": 1
}
```

Project statistics:

```http
GET /projects/1/stats
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

---

# 🤖 AI-Assisted Quick-Add

TaskFlow provides a natural-language Quick-Add feature.

Example input:

```text
Finish monthly report tomorrow, urgent
```

The parser extracts:

```text
Title: Finish monthly report
Priority: high
Due Date: tomorrow
Status: pending
```

### Supported Priority Keywords

| Input               | Priority |
| ------------------- | -------- |
| `urgent`            | high     |
| `ASAP`              | high     |
| `low priority`      | low      |
| `whenever`          | low      |
| No priority keyword | medium   |

### Supported Date Examples

```text
today
tomorrow
next week
```

The parser also normalizes extra spaces after removing keywords.

---

# 📌 Quick-Add Examples

### High Priority

Input:

```text
Fix login bug today, ASAP
```

Result:

```json
{
  "title": "Fix login bug",
  "priority": "high",
  "due_date_hint": "today"
}
```

### Low Priority

Input:

```text
Update documentation next week, low priority
```

Result:

```json
{
  "title": "Update documentation",
  "priority": "low",
  "due_date_hint": "next week"
}
```

### Normal Priority

Input:

```text
Prepare project presentation tomorrow
```

Result:

```json
{
  "title": "Prepare project presentation",
  "priority": "medium",
  "due_date_hint": "tomorrow"
}
```

---

# 🔎 Task Search

TaskFlow supports both **Linear Search** and **Binary Search**.

## Linear Search

```http
GET /tasks/search?title=Fix%20login%20bug&algo=linear
```

Linear Search checks records sequentially until a matching task is found.

## Binary Search

```http
GET /tasks/search?title=Fix%20login%20bug&algo=binary
```

Binary Search first sorts the records by title and then searches the sorted records.

Example response structure:

```json
{
  "algorithm": "binary",
  "query": "Fix login bug",
  "found": true,
  "index": 0,
  "comparison_count": 1
}
```

---

# 🧮 Algorithm Complexity

TaskFlow implements three main algorithms.

| Algorithm      | Best Case | Average Case | Worst Case | Space |
| -------------- | --------: | -----------: | ---------: | ----: |
| Insertion Sort |      O(n) |        O(n²) |      O(n²) |  O(1) |
| Linear Search  |      O(1) |         O(n) |       O(n) |  O(1) |
| Binary Search  |      O(1) |     O(log n) |   O(log n) |  O(1) |

## Insertion Sort

Insertion Sort is used for task sorting.

It performs well when data is already sorted or nearly sorted.

* Best case: `O(n)`
* Average case: `O(n²)`
* Worst case: `O(n²)`
* Space: `O(1)`

## Linear Search

Linear Search checks records one by one.

* Best case: `O(1)`
* Average case: `O(n)`
* Worst case: `O(n)`
* Space: `O(1)`

## Binary Search

Binary Search repeatedly divides the search range in half.

It requires sorted data.

* Best case: `O(1)`
* Average case: `O(log n)`
* Worst case: `O(log n)`
* Space: `O(1)`

---

# 📊 Algorithm Benchmark

TaskFlow includes a benchmark script for comparing algorithmic work at different dataset sizes.

Run:

```powershell
cd backend
python benchmark.py
```

The benchmark uses:

```text
10 records
500 records
3000 records
```

## Actual Benchmark Results

| Records | Insertion Sort | Linear Search | Binary Search |
| ------: | -------------: | ------------: | ------------: |
|      10 |             17 |            10 |             2 |
|     500 |         31,312 |           500 |             8 |
|    3000 |      1,820,783 |         3,000 |             7 |

### Interpretation

The benchmark demonstrates the expected difference between the algorithms:

* **Insertion Sort** requires substantially more comparisons as the dataset grows.
* **Linear Search** grows approximately linearly with the number of records.
* **Binary Search** requires significantly fewer comparisons after the data is sorted.

This demonstrates why algorithm selection becomes important as the number of tasks increases.

---

# 🧪 Algorithm Verification

TaskFlow includes an automated verification script.

Run:

```powershell
cd backend
python check_algorithms.py
```

The verification checks:

* Insertion Sort correctness
* Binary Search correctness
* Linear Search correctness
* Comparison counting
* Input immutability
* Algorithm behavior

Successful verification:

```text
RESULT: 13/13 checks passed
ALL ALGORITHM CHECKS PASSED
```

---

# 🤖 AI Prompting Techniques

TaskFlow's AI-assisted Quick-Add uses structured prompting concepts.

## Zero-Shot Prompting

Zero-shot prompting asks the model to perform a task without providing worked examples beforehand.

The Quick-Add instruction can request:

```text
title
priority
due_date_hint
```

while restricting priority values to:

```text
low
medium
high
```

Example:

```text
Convert this task description into a task title,
priority, and due_date_hint.

Priority must be low, medium, or high.

Input:
Finish the monthly report tomorrow, urgent
```

Expected interpretation:

```json
{
  "title": "Finish the monthly report",
  "priority": "high",
  "due_date_hint": "tomorrow"
}
```

## Few-Shot Prompting

Few-shot prompting provides examples before processing a new input.

For example:

```text
Input:
Fix the login bug today, urgent

Output:
{
  "title": "Fix the login bug",
  "priority": "high",
  "due_date_hint": "today"
}
```

and:

```text
Input:
Update documentation next week, low priority

Output:
{
  "title": "Update documentation",
  "priority": "low",
  "due_date_hint": "next week"
}
```

Few-shot prompting can make expected transformations clearer, while using more tokens than zero-shot prompting.

---

# 🌐 Frontend

The frontend is built using standard HTML, CSS, and JavaScript.

It provides:

* Task creation
* Task editing
* Task deletion
* Task search
* Task filtering
* Priority controls
* Status controls
* User management
* Project management
* Project statistics
* Responsive layout
* Client-side validation
* LocalStorage caching

The frontend can be opened using a local development server such as **VS Code Live Server**.

---

# ⚡ Performance Monitoring

TaskFlow includes request timing middleware.

API responses include:

```text
X-Process-Time-Ms
```

The backend can also log:

```text
GET /tasks - 200 - 3.21 ms
```

This provides a simple way to monitor API processing time during development and testing.

---

# 🔍 Error Handling

TaskFlow handles common API errors.

### Task Not Found

```json
{
  "detail": "Task not found"
}
```

Status:

```text
404
```

### Project Not Found

```json
{
  "detail": "Project not found"
}
```

Status:

```text
404
```

### Duplicate User Email

```json
{
  "detail": "Email already exists"
}
```

Status:

```text
422
```

---

# 🧪 Testing Completed

The following functionality has been tested:

* ✅ Task CRUD
* ✅ Get task by ID
* ✅ User CRUD
* ✅ Project CRUD
* ✅ Project statistics
* ✅ Task search
* ✅ Linear Search
* ✅ Binary Search
* ✅ Priority sorting
* ✅ Due-date sorting
* ✅ AI Quick-Add
* ✅ Algorithm verification
* ✅ Algorithm benchmarking
* ✅ Swagger API endpoints
* ✅ Error handling

---

# 🏗️ Design Decisions

### FastAPI

FastAPI provides:

* Typed API endpoints
* Request validation
* Automatic Swagger documentation
* High-performance API development

### SQLAlchemy

SQLAlchemy provides structured database interaction through Python models.

### SQLite

SQLite is lightweight and suitable for a small educational and demonstration project.

### Vanilla JavaScript

The frontend uses standard JavaScript to keep the application lightweight and easy to understand.

### Custom Algorithms

Insertion Sort, Linear Search, and Binary Search are implemented explicitly instead of relying entirely on built-in sorting/searching functions. This makes their behavior and comparison counts easier to demonstrate and verify.

---

# 📈 Project Highlights

TaskFlow demonstrates several important software-engineering concepts in one application:

```text
Frontend
   ↓
REST API
   ↓
FastAPI
   ↓
SQLAlchemy
   ↓
SQLite
```

Alongside the application layer, TaskFlow demonstrates:

```text
Task Management
      +
User Management
      +
Project Management
      +
Algorithm Design
      +
AI-Assisted Input
      +
Performance Benchmarking
      +
Automated Verification
```

---

# 📋 Running the Complete Project

From the project root:

```powershell
cd C:\Users\gulsh\Desktop\taskflow1
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Start the backend:

```powershell
python -m uvicorn backend.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

For algorithm verification, open another PowerShell terminal:

```powershell
cd C:\Users\gulsh\Desktop\taskflow1\backend
```

Run:

```powershell
python check_algorithms.py
```

Run benchmark:

```powershell
python benchmark.py
```

---

# 📄 License

This project was created as a full-stack software engineering project for educational and demonstration purposes.

---

## 👨‍💻 Project

**TaskFlow — Full-Stack, AI-Assisted Task Management Platform**

Built using:

```text
Python
FastAPI
SQLAlchemy
SQLite
HTML
CSS
JavaScript
Algorithms
AI-Assisted Quick-Add

