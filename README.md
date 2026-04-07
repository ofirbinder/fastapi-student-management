# Scholar-FastAPI (Robust Student Management API)

A modern, high-performance Student Management API built with **FastAPI**. This project focuses on clean architecture, strict data validation, and a sophisticated error-handling system.

## 🚀 Key Features

- **Clean Architecture**: Separation of concerns between Routes, Services, Models, and Core logic.
- **Robust Error Handling**: Centralized exception management using custom `AppError` handlers.
- **Advanced Validation**: Detailed request validation with Pydantic, including custom handling for malformed JSON.
- **File-Based Persistence**: Thread-safe JSON database operations using `portalocker` for file locking.
- **Production Ready**: Struc tured to be easily extended to a real database (PostgreSQL/MongoDB).

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Concurrency & Locking**: [Portalocker](https://portalocker.readthedocs.io/)
- **Environment Management**: Python-dotenv
- **Linter**: Ruff

## 📂 Project Structure

```text
├── app
│   ├── core         # Core logic (Database, Exception Handlers, Config)
│   ├── models       # Pydantic Schemas & Domain Models
│   ├── routers      # API Endpoints (Student Router, etc.)
│   ├── services     # Business Logic
│   └── db           # Local JSON Storage
├── main.py          # Application Entry Point
└── .env             # Environment Variables
```

## 🚥 Global Exception Handling (The "Special Sauce")

This project implements a unique error-handling flow that distinguishes between:

1. **Client Errors (400/422)**: Distinguishes between bad JSON syntax (400) and failed business logic validation (422).
2. **Server Errors (500)**: Catches database corruption, file lock issues, and permission errors.
3. **Domain Errors**: Custom exceptions like `DuplicateEntryError` for business rules.

## 💻 Getting Started

### Prerequisites

- Python 3.10+
- Virtualenv

### Installation

1. **Clone the repository**:

   ```bash
   git clone [https://github.com/your-username/scholar-fastapi.git](https://github.com/your-username/scholar-fastapi.git)
   cd scholar-fastapi
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`
Interactive docs: `http://127.0.0.1:8000/docs`

## 📝 Roadmap

- [x] Basic CRUD for Students
- [x] Advanced Error Handling
- [x] File Locking Mechanism
- [ ] Authentication & JWT
- [ ] Integration with PostgreSQL
- [ ] Unit Tests with Pytest
