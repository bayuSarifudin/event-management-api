# Event Management API

A role-based event management API built with Django REST Framework. This system is designed to manage events, tracks, sessions, and participant registrations with a scalable and structured backend architecture.

---

## 🚀 Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Token)
- **Containerization**: Docker & Docker Compose

---

## 📌 Key Features

### 🔹 Authentication & Authorization

- JWT-based authentication
- Role-based access control:
  - **Superadmin**: full system control, manage roles
  - **Admin**: manage events, tracks, sessions
  - **User**: register to events

---

### 🔹 Event Management

- Create, update, delete events (admin & superadmin)
- Event ownership (`created_by`)
- Filter & pagination support

---

### 🔹 Track & Session Management

- Hierarchical structure:

```
Event → Track → Session
```

- Tracks belong to an event
- Sessions belong to a track
- Enables structured scheduling within events

---

### 🔹 Registration System

- Users can register for events
- Track participants per event
- Prevent duplicate registrations (if implemented)

---

### 🔹 API Design

- Standardized response format:

```json
{
  "data": {},
  "message": "",
  "errors": null
}
```

- Pagination response:

```json
{
  "data": [],
  "message": "List of events",
  "errors": null,
  "meta": {
    "count": 100,
    "next": "...",
    "previous": "..."
  }
}
```

---

## 🧠 System Design

### Entity Relationship

- **User**
  - has role: `superadmin | admin | user`

- **Event**
  - created by user (admin/superadmin)

- **Track**
  - belongs to Event

- **Session**
  - belongs to Track

- **Registration**
  - links User ↔ Event

---

## ⚙️ Setup (Local Development)

### 1. Clone Repository

```bash
git clone git@github.com:bayuSarifudin/event-management-api.git
cd event-management-api
```

---

### 2. Setup python environment

**USE PYENV**

```
pyenv install 3.10.20
pyenv local 3.10.20
```

**CReate Virtual env**

```
python -m venv venv
```

**Activate**

```
source venv/bin/activate
```

**Validate**

```
which python
which pip
```

**Installing new additional dependencies**

```
python -m pip install -new library-
```

**freeze to requirement.txt**

```
pip freeze > requirements.txt
```

### 3. Create Environment File

Create `.env` file:

```env
DB_NAME=event_db
DB_USER=event_user
DB_PASSWORD=password123
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True
```

---

### 4. Run with Docker

```bash
docker compose up --build
```

---

### 5. Access API

```
http://localhost:8000
```

---

## 🔑 Default Superadmin

On first setup:

```
username: superadmin
password: P@ssw0rd
```

---

## 📚 [API Endpoints](https://github.com/bayuSarifudin/event-management-api/blob/main/api-contract.md)

### 🔐 Authentication

| Method | Endpoint              | Description       |
| ------ | --------------------- | ----------------- |
| POST   | `/api/auth/register/` | Register user     |
| POST   | `/api/auth/login/`    | Login and get JWT |

---

### 📅 Events

| Method | Endpoint                            | Access           |
| ------ | ----------------------------------- | ---------------- |
| GET    | `/api/events/`                      | All users        |
| POST   | `/api/events/`                      | Admin/Superadmin |
| GET    | `/api/events/{id}/`                 | All users        |
| PUT    | `/api/events/{id}/`                 | Admin/Superadmin |
| PATCH  | `/api/events/{id}/`                 | Admin/Superadmin |
| DELETE | `/api/events/{id}/`                 | Admin/Superadmin |
| GET    | `/api/events/my-events/`            | Admin/Superadmin |
| GET    | `/api/events/{id}/my-event-detail/` | Admin/Superadmin |
| GET    | `/api/events/{id}/registrations/`   | Admin/Superadmin |

---

### 📊 Tracks

| Method | Endpoint            |
| ------ | ------------------- |
| GET    | `/api/tracks/`      |
| POST   | `/api/tracks/`      |
| GET    | `/api/tracks/{id}/` |
| PUT    | `/api/tracks/{id}/` |
| DELETE | `/api/tracks/{id}/` |

---

### 🎤 Sessions

| Method | Endpoint              |
| ------ | --------------------- |
| GET    | `/api/sessions/`      |
| POST   | `/api/sessions/`      |
| GET    | `/api/sessions/{id}/` |
| PUT    | `/api/sessions/{id}/` |
| DELETE | `/api/sessions/{id}/` |

---

### 📝 Registrations

| Method | Endpoint              |
| ------ | --------------------- |
| POST   | `/api/registrations/` |
| GET    | `/api/registrations/` |

---

## 🐳 Docker Setup

### Services

- **web** → Django API
- **db** → PostgreSQL

### Run

```bash
docker compose up --build
```

### Stop

```bash
docker compose down
```

---

## 📈 Scalability Considerations

- Separation of concerns (apps: users, events, registrations)
- PostgreSQL for relational integrity
- Pagination for large datasets
- Docker for environment consistency
