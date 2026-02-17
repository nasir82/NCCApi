# Management System API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Version](https://img.shields.io/badge/version-1.0.1-blue?style=for-the-badge)
![OAS](https://img.shields.io/badge/OAS-3.1-green?style=for-the-badge)

A professional-grade backend service built with **FastAPI** to handle the internal operations of the NCC. This system manages student data, attendance tracking, payment records, and resource distribution.

---

## 🚀 Key Features

- **Attendance Tracking** — Automated logs for students organized by academic level and year.
- **Payment Management** — Secure tracking of student fees and transaction records using JSON-structured data.
- **Official Persons Directory** — Role-based management for administration, teachers, and office staff.
- **Exam & Resource Portal** — Distribution of study materials and examination metadata.
- **UUID Strategy** — Implements `UUID4` for all primary keys to ensure global uniqueness and prevent data scraping.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (Asynchronous Python) |
| ORM | SQLAlchemy 2.0 with `from_attributes=True` mapping |
| Migrations | Alembic for version-controlled schema updates |
| Database | PostgreSQL |
| Documentation | Swagger / OpenAPI with custom Markdown descriptions |
| Containerization | Docker & Docker Compose |

---

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL (Local or Docker-based)
- Docker Desktop *(Optional, for containerized deployment)*

---

## 🔧 Installation & Setup

### 1. Clone and Navigate

```bash
git clone https://github.com/nasir82/NCCApi.git
cd ncc-api
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ncc_db
SECRET_KEY=your_generated_secret_key
```

### 3. Setup Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Start the Server

```bash
uvicorn main:app --reload
```

| Interface | URL |
|-----------|-----|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
| OpenAPI JSON | `http://localhost:8000/openapi.json` |

### 🐳 Docker Setup (Alternative)

```bash
docker-compose up --build
```

---

## 📡 API Endpoints & Schemas

### 🖼️ Banners
**Table:** `banners`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/banner/` | Get all banners | `200` |
| `POST` | `/banner/` | Create a banner | `201` |
| `GET` | `/banner/{ref}` | Get a banner by ref | `200` |
| `PATCH` | `/banner/{ref}` | Update a banner | `200` |
| `DELETE` | `/banner/{ref}` | Delete a banner | `204` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `ref` | `str` | `String(36)` | PK · UUID4 · Unique · Index |
| `title` | `str` | `String` | Required |
| `image_url` | `str` | `String` | Required |

---

### 🎓 Students
**Table:** `students`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/students/students` | Get all students | `200` |
| `POST` | `/students/students` | Create a student | `201` |
| `GET` | `/students/students/{student_id}` | Get a student by ID | `200` |
| `DELETE` | `/students/students/{student_id}` | Delete a student | `204` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `id` | `str` | `String(36)` | PK · UUID4 · Index |
| `name` | `str` | `String` | Required |
| `mobile` | `str` | `String` | Required |
| `level` | `str` | `String` | Required |
| `year` | `str` | `String` | Required |
| `school` | `str` | `String` | Required |
| `address` | `str` | `String` | Required |
| `guardian_phone` | `str` | `String` | Required |
| `profile_image_url` | `str \| None` | `String` | Optional · Nullable |

---

### 👤 Users
**Table:** `users`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/users/users` | Get all users | `200` |
| `POST` | `/users/users` | Create a user | `201` |
| `GET` | `/users/users/{user_id}` | Get a user by ID | `200` |
| `DELETE` | `/users/users/{user_id}` | Delete a user | `204` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `id` | `str` | `String(36)` | PK · UUID4 · Index |
| `name` | `str` | `String` | Required |
| `rule` | `str` | `String` | Required |

---

### 🏛️ Administration
**Table:** `official_persons`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/administration/` | Get all officials | `200` |
| `POST` | `/administration/` | Create an official | `201` |
| `PATCH` | `/administration/{ref}` | Update an official | `200` |
| `DELETE` | `/administration/{ref}` | Delete an official | `200` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `ref` | `str` | `String(36)` | PK · UUID4 · Index |
| `name` | `str` | `String` | Required |
| `phone` | `str` | `String` | Required |
| `email` | `str` | `String` | Required · Unique |
| `designation` | `AdministrationDesignationType` | `Enum` | Default: `NONE` |
| `profile_link` | `str` | `String` | Required |
| `join_date` | `str` | `String` | Required |
| `end_date` | `str` | `String` | Required |

> `AdministrationDesignationType` is a custom Enum — see [`app/utils/utility.py`](app/utils/utility.py) for values.

---

### 📅 Attendance Tracking
**Table:** `attendance_tracking`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/attendance-tracking/` | Get all tracking records | `200` |
| `POST` | `/attendance-tracking/` | Create a tracking record | `201` |
| `GET` | `/attendance-tracking/{id}` | Get one tracking record | `200` |
| `PATCH` | `/attendance-tracking/{id}` | Add an attendance record | `200` |
| `DELETE` | `/attendance-tracking/{id}` | Delete a tracking record | `204` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `id` | `str` | `String(36)` | PK · UUID4 · Index |
| `level` | `str` | `String` | Required |
| `year` | `str` | `String(4)` | Required |
| `students` | `List[dict]` | `JSON` | Default: `[]` |
| `attendance_records` | `List[AttendanceModelSchema]` | `JSON` | Default: `[]` |

**`AttendanceModelSchema`** — nested object inside `attendance_records`:

| Field | Type | Constraints |
|-------|------|-------------|
| `date` | `datetime` | Required |
| `subject` | `str` | Required |
| `teacherName` | `str` | Required |
| `attendanceByStudentId` | `Dict[str, bool]` | Required · `studentId → isPresent` |

---

### 📣 Events
**Table:** `events`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/events/` | Get all events | `200` |
| `POST` | `/events/` | Create an event | `201` |
| `GET` | `/events/{id}` | Get an event by ID | `200` |
| `DELETE` | `/events/{id}` | Delete an event | `200` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `id` | `str` | `String(36)` | PK · UUID4 · Index |
| `title` | `str` | `String` | Required |
| `type` | `EventType` | `Enum` | Default: `text` |
| `content` | `str` | `String` | Required |
| `published` | `datetime` | `DateTime` | Required |
| `status` | `EventStatus` | `Enum` | Default: `upcoming` |

> **`EventType`** values: `text`, `image` &nbsp;|&nbsp; **`EventStatus`** values: `upcoming`, *(see `app/models/event_status.py`)*

---

### 📝 Exams
**Table:** `exams`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/exams/` | Get all exams | `200` |
| `POST` | `/exams/` | Create an exam | `201` |
| `GET` | `/exams/{ref}` | Get an exam by ref | `200` |
| `PATCH` | `/exams/{ref}` | Update an exam | `200` |
| `DELETE` | `/exams/{ref}` | Delete an exam | `200` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `ref` | `str` | `String(36)` | PK · UUID4 · Index |
| `examTitle` | `str` | `String` | Required |
| `subject` | `str` | `String` | Required |
| `examTopics` | `List[str]` | `JSON` | Required |
| `examDate` | `datetime` | `DateTime` | Required |
| `totalTime` | `int` | `Integer` | Required · Minutes |
| `questions` | `List[QuestionSchema]` | `JSON` | Required |
| `level` | `str` | `String` | Required |
| `isAttended` | `bool` | `Boolean` | Default: `False` |
| `gainedNumber` | `int` | `Integer` | Default: `0` |

**`QuestionSchema`** — nested object inside `questions`:

| Field | Type | Constraints |
|-------|------|-------------|
| `question` | `str` | Required |
| `options` | `List[str]` | Required |
| `selection` | `str` | Default: `""` |
| `correctAns` | `str` | Required |
| `mark` | `int` | Default: `-1` |
| `explanation` | `str` | Default: `""` |

---

### 💳 Payments
**Table:** `payment_tracking`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/payments/` | Get all payment records | `200` |
| `POST` | `/payments/` | Create a payment tracking record | `201` |
| `PUT` | `/payments/{id}` | Update a payment tracking record | `200` |
| `DELETE` | `/payments/{id}` | Delete a payment tracking record | `200` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `id` | `str` | `String(36)` | PK · UUID4 · Index |
| `level` | `str` | `String` | Required |
| `year` | `str` | `String(4)` | Required |
| `students` | `List[dict]` | `JSON` | Default: `[]` |
| `payment_status_records` | `List[PaymentModelSchema]` | `JSON` | Default: `[]` |

**`PaymentModelSchema`** — nested object inside `payment_status_records`:

| Field | Type | Constraints |
|-------|------|-------------|
| `monthName` | `str` | Required |
| `paymentStatus` | `Dict[str, bool]` | Required · `studentId → isPaid` |

---

### 📚 Resources
**Table:** `resources`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/resources/` | Get all resources | `200` |
| `POST` | `/resources/` | Create a resource | `201` |
| `GET` | `/resources/{id}` | Get a resource by ID | `200` |
| `PATCH` | `/resources/{id}` | Update a resource | `200` |
| `DELETE` | `/resources/{id}` | Delete a resource | `200` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `id` | `str` | `String(36)` | PK · UUID4 · Index |
| `title` | `str` | `String` | Required |
| `type` | `ResourceType` | `Enum` | Required · e.g. `books` |
| `link` | `str` | `String` | Required |
| `level` | `str` | `String` | Default: `""` |
| `dateOfUpload` | `datetime` | `DateTime` | Required |

---

### 🏢 Office Staff
**Table:** `office_staff`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/office/` | Get all staff | `200` |
| `POST` | `/office/` | Create a staff member | `201` |
| `GET` | `/office/{ref}` | Get staff by ref | `200` |
| `PATCH` | `/office/{ref}` | Update a staff member | `200` |
| `DELETE` | `/office/{ref}` | Delete a staff member | `200` |

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `ref` | `str` | `String(36)` | PK · UUID4 · Index |
| `name` | `str` | `String` | Required |
| `designation` | `AssistantsDesignation` | `Enum` | Required |
| `phone` | `str` | `String` | Required |
| `email` | `str` | `String` | Required |
| `image` | `str` | `String` | Required |
| `from` *(alias: `from_date`)* | `str` | `String` | Required |
| `to` *(alias: `to_date`)* | `str` | `String` | Default: `""` |

> Field uses Pydantic `alias` — send `"from"` and `"to"` in JSON; stored as `from_date` / `to_date` in DB.

---

### 👩‍🏫 Teachers
**Table:** `teachers`

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/teachers/` | Get all teachers | `200` |
| `POST` | `/teachers/` | Register a new teacher | `201` |
| `GET` | `/teachers/{id}` | Get a teacher by ID | `200` |
| `PATCH` | `/teachers/{id}` | Update a teacher | `200` |
| `DELETE` | `/teachers/{id}` | Delete a teacher | `200` |

> ⚠️ **Note:** `email` must be **unique** across the entire system.

| Field | Type | DB Column | Constraints |
|-------|------|-----------|-------------|
| `id` | `str` | `String(36)` | PK · UUID4 · Index |
| `name` | `str` | `String` | Required |
| `mobile` | `str` | `String` | Required |
| `email` | `EmailStr` | `String` | Required · Unique |
| `background` | `str` | `String` | Required |
| `profileImageUrl` | `str` | `String` | Required |
| `subjects` | `List[str]` | `JSON` | Default: `[]` |

---

## ⚠️ Error Handling

All endpoints return `422 Unprocessable Entity` for invalid input:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 🗂️ Enum Types Reference

| Enum | Location | Used In |
|------|----------|---------|
| `AdministrationDesignationType` | `app/utils/utility.py` | `OfficialPerson` |
| `AssistantsDesignation` | `app/models/designations.py` | `OfficePerson` |
| `EventType` | `app/models/types.py` | `Event` |
| `EventStatus` | `app/models/event_status.py` | `Event` |
| `ResourceType` | `app/models/types.py` | `Resource` |

---

## 📬 Contact

For support, contact **nasirpks36@gmail.com**.
