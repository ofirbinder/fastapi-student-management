# 🎓 Scholar System: Personal Deep-Dive Project

## A Robust Student Management System built with FastAPI & Docker

This is a personal project designed to master **FastAPI**, **Pydantic v2**, and **Dockerized Environments**. Beyond simple CRUD operations, this system explores advanced concepts in Python 3.12, clean architecture, and professional deployment strategies using Docker Compose.

---

## 🌟 The "Special Sauce" (Key Architectural Features)

### 1. Standardized Communication (`APIResponse`)

All API responses follow a strict, predictable JSON structure:

- **Consistency:** Every response includes `status_code`, `data`, and optional `meta`.
- **Frontend Friendly:** Simplifies integration for UI consumers by providing a reliable interface.

### 2. Smart Exception Handling (`AppError` Framework)

A centralized, hierarchical error management system:

- **Domain-Driven Errors:** Custom exceptions like `DuplicateEntryError` or `InvalidAPIFeaturesParams`.
- **Global Middleware:** Automatically catches internal errors and translates them into clean, standardized API responses.

### 3. Sophisticated Data Modeling (Two-Layer Strategy)

Using the latest **Pydantic v2** features:

- **`StudentSchema` vs `StudentInDB`**: Clear separation between user input and internal database records (adding IDs, timestamps, and active status).
- **CamelCase Bridge**: Automatic alias generation allows the API to speak "JavaScript" (camelCase) while the backend stays "Pythonic" (snake_case).

### 4. `APIFeatures`: Dynamic Sorting & Pagination

A custom-built engine that handles logic-based slicing and sorting (e.g., `-created_at`) directly on the validated data sets.

---

## 🎨 Built-in Dashboard (UI)

The project includes a responsive dashboard built with **Tailwind CSS**, served directly by FastAPI. It allows for real-time testing of all CRUD operations with visual feedback and error notifications.

---

## 🛠 Tech Stack

- **Language**: Python 3.12-slim
- **Backend**: FastAPI
- **Validation**: Pydantic v2
- **Storage**: Thread-safe JSON DB with `Portalocker` (File Locking)
- **Containerization**: Docker & Docker Compose
- **Frontend**: HTML5 & Tailwind CSS

---

## 🚀 How to Run

### 1. Using Docker Compose

The project uses a single `docker-compose.yml` to manage both environments.

- **Development (Port 8000):** Includes hot-reload and maps the entire local directory to the container.

  ```bash
  docker-compose up api-dev
  ```

- **Production (Port 8080):** Optimized for stability. Only the data directory is persisted via volumes.

  ```bash
  docker-compose up api-prod
  ```

### 2. Local Debugging (VS Code)

The project includes a pre-configured `launch.json` for easy debugging.

1. **Install Dependencies:** `pip install -r requirements.txt`
2. **Run via Debugger:**
   - Go to the **"Run and Debug"** tab (Ctrl+Shift+D).
   - Choose either **"FastAPI: Development"** or **"FastAPI: Production"**.
   - This will trigger the entry point via `run.py` with the appropriate `APP_ENV` variables.

Access the UI at: `http://localhost:8000/static/index.html` (Dev) or `http://localhost:8080/static/index.html` (Prod).

---

## 📂 Project Structure

```text
├── app
│   ├── core         # Global Exception handling, APIFeatures, DB config
│   ├── models       # Smart Pydantic models (Input vs DB entities)
│   ├── routers      # Clean API Endpoints
│   ├── services     # Business logic (The "Brain" of the app)
│   └── db           # Local persistent storage
├── static           # Tailwind-based UI dashboard
├── Dockerfile       # Python 3.12-slim image definition
├── docker-compose.yml
├── run.py           # Entry point for local execution
└── main.py          # Application factory & Middleware configuration
```

---

**Developed with ❤️ by Ofir Binder**
_Deep-diving into automation, clean code, and modern API design._

---
