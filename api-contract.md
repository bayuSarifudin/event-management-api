# API Contract - Event Management System

## Base URL

```
{{ baseUrl }}/api/
```

---

## Authentication

### Register

- **POST** `/auth/register/`

**Body:**

```json
{
  "username": "john",
  "email": "john@mail.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "data": {
    "id": 1,
    "username": "john"
  },
  "message": "User registered",
  "errors": null
}
```

---

### Login

- **POST** `/auth/login/`

**Body:**

```json
{
  "username": "john",
  "password": "password123"
}
```

**Response:**

```json
{
  "data": {
    "access": "jwt_token",
    "refresh": "refresh_token"
  },
  "message": "Login success",
  "errors": null
}
```

---

### Refresh Token

- **POST** `/auth/refresh/`

**Body**

```json
{
  "refresh": "refresh_token"
}
```

**Response**

```json
{
  "access": "access_token"
}
```

---

### Promote user to admin

- **POST** `/users/promote/`

**Body**

```json
{
  "user_id": 1
}
```

**Response**

```json
{
  "message": "User promoted to admin"
}
```

### Get List User

- **GET** `/users/`

**Response**

```json
{
  "success": true,
  "message": "List of users",
  "data": [
    {
      "id": 1,
      "username": "superadmin",
      "email": "",
      "role": "superadmin"
    }
  ],
  "errors": null,
  "meta": {
    "count": 1,
    "next": null,
    "previous": null
  }
}
```

---

## Events

### Get All Events

- **GET** `/events/`

**Query Params:**

- page
- page_size

**Response:**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Tech Conference",
      "capacity": 100,
      "available_seats": 95
    }
  ],
  "message": "List of events",
  "errors": null,
  "meta": {
    "count": 1,
    "next": null,
    "previous": null
  }
}
```

---

### Create Event (Admin Only)

- **POST** `/events/`

**Body:**

```json
{
  "name": "Tech Conference",
  "description": "Event desc",
  "start_date": "2026-05-01T09:00:00Z",
  "end_date": "2026-05-02T17:00:00Z",
  "venue": "Jakarta",
  "capacity": 100
}
```

---

### Event Detail

- **GET** `/events/{id}/`

**Response:**

```json
{
  "data": {
    "id": 1,
    "name": "Tech Conference",
    "available_seats": 95,
    "tracks": [
      {
        "id": 1,
        "name": "Frontend",
        "sessions": [
          {
            "id": 1,
            "title": "React Deep Dive"
          }
        ]
      }
    ]
  }
}
```

---

### Update Event (Full)

- **PUT** `/events/{id}/`

**Body:**

```json
{
  "name": "Updated Event",
  "description": "Updated desc",
  "start_date": "2026-05-01T09:00:00Z",
  "end_date": "2026-05-02T17:00:00Z",
  "venue": "Bandung",
  "capacity": 150
}
```

**Response:**

```json
{
  "data": {
    "id": 1,
    "name": "Updated Event",
    "capacity": 150
  },
  "message": "Event updated",
  "errors": null
}
```

---

### Partial Update Event

- **PATCH** `/events/{id}/`

**Body:**

```json
{
  "capacity": 200
}
```

**Response:**

```json
{
  "data": {
    "id": 1,
    "capacity": 200
  },
  "message": "Event partially updated",
  "errors": null
}
```

---

### Delete Event

- **DELETE** `/events/{id}/`

**Response:**

```json
{
  "message": "Event deleted",
  "errors": null
}
```

---

### My Events (Admin)

- **GET** `/events/my-events/`

---

### My Event Detail

- **GET** `/events/{id}/my-event-detail/`

---

### Registered user

- **GET** `/events/1/registrations/`

**Response**

```json
{
  "success": true,
  "message": "Event registrations",
  "data": [
    {
      "id": 1,
      "event": 1,
      "user": {
        "id": 1,
        "username": "superadmin"
      },
      "registered_at": "2026-04-12T10:02:42.405025Z"
    }
  ],
  "errors": null,
  "meta": {
    "count": 1,
    "next": null,
    "previous": null
  }
}
```

---

## Tracks

### Create Track

- **POST** `/tracks/`

**Body:**

```json
{
  "name": "Frontend",
  "event": 1
}
```

---

### Track Detail

- **GET** `/tracks/{id}/`

**Response:**

```json
{
  "data": {
    "id": 1,
    "name": "Frontend",
    "event": 1
  },
  "message": "Track detail",
  "errors": null
}
```

---

### Update Track

- **PUT** `/tracks/{id}/`

**Body:**

```json
{
  "name": "Backend",
  "event": 1
}
```

---

### Partial Update Track

- **PATCH** `/tracks/{id}/`

**Body:**

```json
{
  "name": "DevOps"
}
```

---

### Delete Track

- **DELETE** `/tracks/{id}/`

**Response:**

```json
{
  "message": "Track deleted"
}
```

---

## Sessions

### Create Session

- **POST** `/sessions/`

**Body:**

```json
{
  "title": "React Deep Dive",
  "track": 1,
  "start_time": "2026-05-01T10:00:00Z",
  "end_time": "2026-05-01T12:00:00Z"
}
```

---

### Get All Sessions

- **GET** `/sessions/`

**Response:**

```json
{
  "data": [
    {
      "id": 1,
      "title": "React Deep Dive",
      "track": 1
    }
  ],
  "message": "List of sessions",
  "errors": null
}
```

---

### Session Detail

- **GET** `/sessions/{id}/`

**Response:**

```json
{
  "data": {
    "id": 1,
    "title": "React Deep Dive",
    "track": 1,
    "start_time": "2026-05-01T10:00:00Z",
    "end_time": "2026-05-01T12:00:00Z"
  }
}
```

---

### Update Session

- **PUT** `/sessions/{id}/`

**Body:**

```json
{
  "title": "Advanced React",
  "track": 1,
  "start_time": "2026-05-01T13:00:00Z",
  "end_time": "2026-05-01T15:00:00Z"
}
```

---

### Partial Update Session

- **PATCH** `/sessions/{id}/`

**Body:**

```json
{
  "title": "React Performance"
}
```

---

### Delete Session

- **DELETE** `/sessions/{id}/`

**Response:**

```json
{
  "message": "Session deleted"
}
```

---

## Registration

### Register Event

- **POST** `/registrations/`

**Body:**

```json
{
  "event": 1
}
```

---

### Get All Registrations

- **GET** `/registrations/`

**Response:**

```json
{
  "data": [
    {
      "id": 1,
      "user": 1,
      "event": 1
    }
  ],
  "message": "List of registrations",
  "errors": null
}
```

---

### Registration Detail

- **GET** `/registrations/{id}/`

**Response:**

```json
{
  "data": {
    "id": 1,
    "user": 1,
    "event": 1
  }
}
```

---

### Update Registration

- **PUT** `/registrations/{id}/`

**Body:**

```json
{
  "event": 2
}
```

---

### Partial Update Registration

- **PATCH** `/registrations/{id}/`

**Body:**

```json
{
  "event": 3
}
```

---

### Delete Registration

- **DELETE** `/registrations/{id}/`

**Response:**

```json
{
  "message": "Registration deleted"
}
```

---

## Constraints

- User cannot register twice
- Event cannot exceed capacity
- Session cannot overlap
- Only admin can manage events

---

# 📚 API Documentation

### Swagger Docs

- **GET** `/api/docs/`

---

### OpenAPI Schema

- **GET** `/api/schema/`

---
