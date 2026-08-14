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
│   └── schemas.py
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
| GET    | `/tasks/{task_id}` | Get a task by ID                   |
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

> The current API provides list, create, update, and delete operations for users. A separate `GET /users/{user_id}` endpoint is not implemented.

---

## Projects

| Method | Endpoint                       | Description            |
| ------ | ------------------------------ | ---------------------- |
| POST   | `/projects`                    | Create project         |
| GET    | `/projects`                    | List projects          |
| PUT    | `/projects/{project_id}`       | Update project         |
| DELETE | `/projects/{project_id}`       | Delete project         |
| GET    | `/projects/{project_id}/stats` | Get project statistics |

> The current API provides project statistics by ID. A separate `GET /projects/{project_id}` endpoint is not implemented.

---

## Algorithms

| Method | Endpoint                    | Description                   |
| ------ | --------------------------- | ----------------------------- |
| POST   | `/algorithms/sort`          | Run insertion sort            |
| GET    | `/algorithms/linear-search` | Run linear search             |
| GET    | `/algorithms/binary-search` | Run binary search             |
| POST   | `/algorithms/benchmark`     | Compare algorithm performance |

---

# 📚 Complete API Examples

## 1. Create Task

### Request

```http
POST /tasks
Content-Type: application/json
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

## 2. List Tasks

### Request

```http
GET /tasks
```

### Response

```json
[
  {
    "id": 1,
    "title": "Finish monthly report",
    "priority": "high",
    "due_date": "tomorrow",
    "status": "pending",
    "project_id": 1
  },
  {
    "id": 2,
    "title": "Prepare presentation",
    "priority": "medium",
    "due_date": "friday",
    "status": "pending",
    "project_id": 1
  }
]
```

---

## 3. Get Task By ID

### Request

```http
GET /tasks/1
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

### Not Found Response

```json
{
  "detail": "Task not found"
}
```

Status:

```text
404
```

---

## 4. Update Task

### Request

```http
PUT /tasks/1
Content-Type: application/json
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

### Response

```json
{
  "id": 1,
  "title": "Finish updated monthly report",
  "priority": "medium",
  "due_date": "friday",
  "status": "pending",
  "project_id": 1
}
```

---

## 5. Delete Task

### Request

```http
DELETE /tasks/1
```

### Response

```json
{
  "message": "Task deleted successfully"
}
```

---

# 📊 Task Sorting

TaskFlow supports sorting tasks using the custom **Insertion Sort** implementation.

## Sort By Priority

### Request

```http
GET /tasks?sort=priority
```

### Example Response

```json
[
  {
    "id": 2,
    "title": "Prepare presentation",
    "priority": "medium",
    "due_date": "friday",
    "status": "pending",
    "project_id": 1
  },
  {
    "id": 1,
    "title": "Fix login bug",
    "priority": "high",
    "due_date": "today",
    "status": "pending",
    "project_id": 1
  }
]
```

Priority ranking is:

```text
low < medium < high
```

## Sort By Due Date

### Request

```http
GET /tasks?sort=due_date
```

### Example Response

```json
[
  {
    "id": 1,
    "title": "Fix login bug",
    "priority": "high",
    "due_date": "today",
    "status": "pending",
    "project_id": 1
  },
  {
    "id": 2,
    "title": "Prepare presentation",
    "priority": "medium",
    "due_date": "friday",
    "status": "pending",
    "project_id": 1
  }
]
```

Invalid sorting values return:

```json
{
  "detail": "sort must be 'priority' or 'due_date'"
}
```

Status:

```text
400
```

---

# 🔎 Task Search

TaskFlow supports both **Linear Search** and **Binary Search**.

## Linear Search

### Request

```http
GET /tasks/search?title=Fix%20login%20bug&algo=linear
```

Linear Search checks records sequentially until a matching task is found.

### Example Response

```json
{
  "algorithm": "linear",
  "query": "Fix login bug",
  "found": true,
  "index": 0,
  "comparison_count": 1,
  "task": {
    "id": 1,
    "title": "Fix login bug",
    "priority": "high",
    "due_date": "today",
    "status": "pending",
    "project_id": 1
  }
}
```

## Binary Search

### Request

```http
GET /tasks/search?title=Fix%20login%20bug&algo=binary
```

Binary Search first sorts records by title and then searches the sorted records.

### Example Response

```json
{
  "algorithm": "binary",
  "query": "Fix login bug",
  "found": true,
  "index": 0,
  "comparison_count": 1,
  "task": {
    "id": 1,
    "title": "Fix login bug",
    "priority": "high",
    "due_date": "today",
    "status": "pending",
    "project_id": 1
  }
}
```

## Search Not Found

```json
{
  "algorithm": "linear",
  "query": "Unknown task",
  "found": false,
  "index": -1,
  "comparison_count": 3,
  "task": null
}
```

---

# 🤖 AI-Assisted Quick-Add

TaskFlow provides a natural-language Quick-Add feature.

The user can describe a task using normal language. The parser extracts:

```text
title
priority
due_date_hint
```

The created task also receives:

```text
status = pending
```

### Example

Input:

```text
Finish monthly report tomorrow, urgent
```

Parsed result:

```json
{
  "title": "Finish monthly report",
  "priority": "high",
  "due_date_hint": "tomorrow"
}
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
next monday
next tuesday
next wednesday
next thursday
next friday
next saturday
next sunday
monday
tuesday
wednesday
thursday
friday
saturday
sunday
```

The parser normalizes extra whitespace and removes unwanted punctuation from the beginning and end of the generated title.

---

# 📌 Quick-Add API Example

## Request

```http
POST /tasks/quick-add
Content-Type: application/json
```

```json
{
  "description": "Finish monthly report tomorrow, urgent",
  "project_id": 1
}
```

## Response

```json
{
  "id": 3,
  "title": "Finish monthly report",
  "priority": "high",
  "due_date": "tomorrow",
  "status": "pending",
  "project_id": 1
}
```

---
s
# 🧪 Five Worked Quick-Add Examples

The following examples are based on the actual output of the project's `parse_quick_add()` function.

## Example 1 — High Priority

### Input

```text
Finish monthly report tomorrow, urgent
```

### Actual Parsed Output

```json
{
  "title": "Finish monthly report",
  "priority": "high",
  "due_date_hint": "tomorrow"
}
```

---

## Example 2 — High Priority With ASAP

### Input

```text
Fix login bug today, ASAP
```

### Actual Parsed Output

```json
{
  "title": "Fix login bug",
  "priority": "high",
  "due_date_hint": "today"
}
```

---

## Example 3 — Low Priority

### Input

```text
Update documentation next week, low priority
```

### Actual Parsed Output

```json
{
  "title": "Update documentation",
  "priority": "low",
  "due_date_hint": "next week"
}
```

---

## Example 4 — Medium Priority

### Input

```text
Prepare project presentation tomorrow
```

### Actual Parsed Output

```json
{
  "title": "Prepare project presentation",
  "priority": "medium",
  "due_date_hint": "tomorrow"
}
```

---

## Example 5 — No Matching Keywords

### Input

```text
Review the project documentation
```

### Actual Parsed Output

```json
{
  "title": "Review the project documentation",
  "priority": "medium",
  "due_date_hint": null
}
```

These examples demonstrate:

* high-priority keyword detection
* ASAP detection
* low-priority detection
* date extraction
* medium-priority default behavior
* handling of input with no date or priority keyword
* title cleanup and whitespace normalization

---

# 🧠 Quick-Add Prompt Design

TaskFlow uses a structured prompt for the AI-assisted Quick-Add feature.

The prompt provides the model with:

1. The role of the task parser.
2. The required output concepts.
3. The allowed priority values.
4. The user's natural-language task description.

The structure is:

```text
System:
You are TaskFlow's task parser.
Convert a free-text description into title,
priority and due_date_hint.
Priority must be low, medium, or high.

User:
<task description>
```

This structure is intentionally simple so that the parser has a clear task and a constrained output vocabulary.

---

# 🤖 AI Prompting Techniques

TaskFlow's AI-assisted Quick-Add demonstrates both **Zero-Shot** and **Few-Shot** prompting concepts.

## Zero-Shot Prompting

Zero-shot prompting asks the model to perform a task without providing worked examples beforehand.

For Quick-Add, the model can be instructed to identify:

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

Another example can show low priority:

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

Few-shot prompting can make expected transformations clearer because the model sees the desired input-to-output pattern before processing a new request.

### Prompting Technique Rationale

Zero-shot prompting is useful when the transformation rules are simple and clearly described. It keeps the prompt short, which reduces token usage and generally makes the request cheaper and faster. It is also easier to maintain because there are fewer examples that can become outdated when the application's parsing rules change. For a constrained task such as extracting a title, priority, and due-date hint, explicit instructions about the allowed priority values can provide enough guidance for many inputs.

Few-shot prompting can improve reliability when the input language is ambiguous or when the desired transformation is difficult to express using rules alone. Providing examples demonstrates the exact relationship between natural-language input and structured output. This can reduce interpretation differences and make formatting more consistent. However, every additional example consumes tokens. A large number of examples increases prompt size, increases processing cost, and may leave less context available for the actual user request. Examples can also introduce unintended patterns if they are poorly selected or inconsistent.

For TaskFlow, a small number of carefully selected examples is preferable to a very large prompt. The examples should represent important variations such as high priority, low priority, date extraction, and an input without special keywords. This provides useful guidance without unnecessarily increasing token consumption.

Reliability can also be improved by constraining the output vocabulary. For example, priority is restricted to `low`, `medium`, or `high`. Structured output expectations reduce the chance of receiving unrelated values such as `critical` or `normal`. Validation should still happen before database insertion so that invalid AI-generated values cannot silently enter the database.

The project currently uses a deterministic mock parser for verification. This makes testing repeatable because the same input produces the same result every time. In a future production version, an actual LLM could be used with structured output validation and carefully selected few-shot examples.

---

# 🧮 Algorithm Complexity

TaskFlow implements three main algorithms.

| Algorithm      | Best Case | Average Case | Worst Case | Space |
| -------------- | --------- | ------------ | ---------- | ----- |
| Insertion Sort | O(n)      | O(n²)        | O(n²)      | O(1)  |
| Linear Search  | O(1)      | O(n)         | O(n)       | O(1)  |
| Binary Search  | O(1)      | O(log n)     | O(log n)   | O(1)  |

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

# 👤 User API Examples

## Create User

### Request

```http
POST /users
Content-Type: application/json
```

```json
{
  "name": "Test User",
  "email": "test@example.com"
}
```

### Response

```json
{
  "id": 1,
  "name": "Test User",
  "email": "test@example.com"
}
```

---

## List Users

### Request

```http
GET /users
```

### Response

```json
[
  {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com"
  }
]
```

---

## Update User

### Request

```http
PUT /users/1
Content-Type: application/json
```

```json
{
  "name": "Updated User",
  "email": "updated@example.com"
}
```

### Response

```json
{
  "id": 1,
  "name": "Updated User",
  "email": "updated@example.com"
}
```

---

## Delete User

### Request

```http
DELETE /users/1
```

### Response

```json
{
  "message": "User deleted successfully"
}
```

---

# 📁 Project API Examples

## Create Project

### Request

```http
POST /projects
Content-Type: application/json
```

```json
{
  "name": "TaskFlow Development",
  "owner_id": 1
}
```

### Response

```json
{
  "id": 1,
  "name": "TaskFlow Development",
  "owner_id": 1
}
```

---

## List Projects

### Request

```http
GET /projects
```

### Response

```json
[
  {
    "id": 1,
    "name": "TaskFlow Development",
    "owner_id": 1
  }
]
```

---

## Update Project

### Request

```http
PUT /projects/1
Content-Type: application/json
```

```json
{
  "name": "TaskFlow Production",
  "owner_id": 1
}
```

### Response

```json
{
  "id": 1,
  "name": "TaskFlow Production",
  "owner_id": 1
}
```

---

## Delete Project

### Request

```http
DELETE /projects/1
```

### Response

```json
{
  "message": "Project deleted successfully"
}
```

---

# 📊 Project Statistics

### Request

```http
GET /projects/1/stats
```

### Response

```json
{
  "project_id": 1,
  "total": 2,
  "pending": 0,
  "completed": 2
}
```

The statistics endpoint calculates the number of tasks belonging to a project and separates them into pending and completed tasks.

---

# 🧪 Algorithm API Examples

## Insertion Sort

### Request

```http
POST /algorithms/sort
Content-Type: application/json
```

```json
[
  5,
  1,
  3
]
```

### Response

```json
{
  "algorithm": "insertion_sort",
  "input": [
    5,
    1,
    3
  ],
  "sorted": [
    1,
    3,
    5
  ]
}
```

---

## Linear Search

### Request

```http
GET /algorithms/linear-search?numbers=5,1,3&target=3
```

### Response

```json
{
  "algorithm": "linear_search",
  "numbers": [
    5,
    1,
    3
  ],
  "target": 3,
  "index": 2
}
```

---

## Binary Search

### Request

```http
GET /algorithms/binary-search?numbers=5,1,3&target=3
```

### Response

```json
{
  "algorithm": "binary_search",
  "numbers": [
    1,
    3,
    5
  ],
  "target": 3,
  "index": 1
}
```

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
* **Linear Search** grows approximately linearly with the number of tasks.
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

## Task Not Found

```json
{
  "detail": "Task not found"
}
```

Status:

```text
404
```

## Project Not Found

```json
{
  "detail": "Project not found"
}
```

Status:

```text
404
```

## User Not Found

```json
{
  "detail": "User not found"
}
```

Status:

```text
404
```

## Duplicate User Email

```json
{
  "detail": "Email already exists"
}
```

Status:

```text
422
```

## Invalid Sort Parameter

```json
{
  "detail": "sort must be 'priority' or 'due_date'"
}
```

Status:

```text
400
```

## Invalid Search Algorithm

```json
{
  "detail": "algo must be 'binary' or 'linear'"
}
```

Status:

```text
400
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
* ✅ Quick-Add parser outputs
* ✅ Algorithm verification
* ✅ Algorithm benchmarking
* ✅ Swagger API endpoints
* ✅ Error handling

Algorithm verification result:

```text
RESULT: 13/13 checks passed
ALL ALGORITHM CHECKS PASSED
```

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
```
