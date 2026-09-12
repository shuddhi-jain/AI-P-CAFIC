# AI-P-CAFIC Backend

FastAPI backend for an AI-powered regulatory compliance and claims management system. The service handles user authentication, policy management, claims workflow, and document upload integration with Amazon S3.

## Overview

This project provides a REST API for:

- User registration and authentication
- JWT-based protected routes
- Policy creation and retrieval
- Claim creation and retrieval
- Document storage via AWS S3

## Tech Stack

- Python 3.14+
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT authentication with python-jose
- AWS S3 via boto3
- Pydantic settings for environment configuration

## Project Structure

```text
backend/
├── app/
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── jwt.py
│   │   ├── login.py
│   │   └── securirty.py
│   ├── claims/
│   │   └── router.py
│   ├── documents/
│   │   └── router.py
│   ├── models/
│   │   ├── claim.py
│   │   ├── claim_document.py
│   │   ├── policy.py
│   │   └── user.py
│   ├── policies/
│   │   └── router.py
│   ├── schema/
│   │   ├── claim_document_schema.py
│   │   ├── claim_schema.py
│   │   ├── policy_schema.py
│   │   └── user.py
│   ├── storage/
│   │   └── s3.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── .env
├── pyproject.toml
├── README.md
└── uv.lock
```

## Prerequisites

Before starting, make sure you have:

- Python 3.14 or newer
- PostgreSQL installed and running
- An AWS account with an S3 bucket configured
- A package manager for Python dependencies (`uv` is recommended)

Install `uv` if it is not already available:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Environment Configuration

Create a `.env` file in the project root with the following values:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ai_pcafic
JWT_SECRET_KEY=your_super_secret_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your_s3_bucket_name
```

Notes:

- `DATABASE_URL` should point to your PostgreSQL database.
- `JWT_SECRET_KEY` is used for access and refresh token signing.
- AWS values are required for S3 document uploads.
- The app loads these variables from `.env` automatically via `pydantic-settings`.

## Database Setup

1. Start PostgreSQL locally.
2. Create a database (for example `ai_pcafic`).

Example:

```bash
createdb ai_pcafic
```

or with psql:

```bash
psql -U postgres
CREATE DATABASE ai_pcafic;
```

The application automatically creates database tables on startup through SQLAlchemy metadata creation.

## Installation

From the project root:

```bash
cd backend
uv sync
```

This installs the dependencies listed in `pyproject.toml`.

If you prefer a standard virtual environment instead of `uv`, you can use:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Running the Application

Start the API in development mode:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You can also run it with FastAPI directly:

```bash
uv run fastapi dev app/main.py
```

The app will start at:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Health Check

Check whether the API is running:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "healthy"}
```

## Main API Endpoints

### Authentication

- `POST /auth/login`
- `POST /auth/logout`
- `POST /auth/refresh`

### Users

- `POST /register`
- `GET /protected` (requires authentication)

### Policies

- `POST /policy/`
- `GET /policy/`
- `GET /policy/{policy_id}`

### Claims

- `POST /claims/`
- `GET /claims/`
- `GET /claims/{claim_id}`

### Documents

- Document routes are mounted from the `app.documents.router` module and are intended for claim document storage and retrieval.

## Authentication Flow

1. Register a user via `POST /register`.
2. Log in via `POST /auth/login`.
3. The server sets HTTP-only cookies for the access and refresh tokens.
4. Protected endpoints require a valid access token.

## Notes

- The application creates all database tables at startup using `Base.metadata.create_all(bind=engine)`.
- JWT tokens are signed using the `JWT_SECRET_KEY` environment variable.
- Protected routes rely on the authentication dependency logic under `app/auth/dependencies.py`.

## Troubleshooting

### Import errors

Make sure the virtual environment is activated and dependencies are installed:

```bash
uv sync
```

### Database connection errors

Verify:

- PostgreSQL is running
- The database name in `DATABASE_URL` exists
- The username/password are correct

### AWS or S3 errors

Verify that:

- AWS credentials are valid
- The bucket exists
- The region matches the bucket configuration

## License

This project is currently intended for internal project use and is not yet published with a formal license.
