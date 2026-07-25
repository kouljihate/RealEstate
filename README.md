# RealEstate - Farm Land eCommerce Platform

A web & mobile Android application for buying and selling farm lands across the country.

## Architecture

```
RealEstate/
├── backend/          # FastAPI REST API
├── web/              # Web frontend (HTML/CSS/JS)
├── mobile/           # Android app (KivyMD)
├── shared/           # Shared constants & enums
├── logs/             # Application logs
├── media/            # Photo & video uploads
├── tests/            # Test suite
└── scripts/          # Deployment utilities
```

## Tech Stack

- **Backend:** Python / FastAPI + Motor (async MongoDB)
- **Database:** MongoDB (users, properties, media metadata)
- **File Storage:** Local filesystem for photos/videos
- **Auth:** JWT tokens with role-based access (admin, customer, guest)
- **Web:** Vanilla HTML/CSS/JS (served by FastAPI)
- **Mobile:** KivyMD (Python cross-platform Android app)
- **Logging:** Rotating file logs + structured JSON logging

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI and secret key

# 4. Run the server
python -m backend.main
```

## API Endpoints (v1)

| Method | Endpoint               | Auth     | Description            |
|--------|------------------------|----------|------------------------|
| POST   | /api/v1/auth/register  | -        | Register customer      |
| POST   | /api/v1/auth/login     | -        | Login (returns JWT)    |
| GET    | /api/v1/auth/me        | Any      | Current user profile   |
| GET    | /api/v1/users          | Admin    | List all users         |
| GET    | /api/v1/users/{id}     | Admin    | Get user by ID         |
| CRUD   | /api/v1/properties/*   | Auth     | Property management    |
| POST   | /api/v1/media/upload   | Auth     | Upload photo/video     |
| GET    | /api/v1/media/{id}     | Any      | Serve media file       |

## Build Log

| Version | Date       | Description                                  |
|---------|------------|----------------------------------------------|
| v1.0.2  | 2026-07-25 | Fix passlib/bcrypt incompat, JSONFormatter fmt |
| v1.0.1  | 2026-07-25 | Fix deps: separate Kivy, loose pins, aiofiles  |
| v1.0.0  | 2026-07-25 | Initial project scaffold                      |
