# FastAPI Test Project

A RESTful API application built with FastAPI for managing customers, items, and orders. This project includes JWT authentication, role-based access control (admin), and database transaction management.

## Features

- **Customer Management**: Full CRUD operations for customer accounts
- **Item Management**: Create, read, update, and delete items with inventory tracking
- **Order Management**: Create orders with automatic inventory validation and quantity updates
- **Authentication**: JWT-based authentication for customers and admin users
- **Authorization**: Role-based access control with admin-only endpoints
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Database Migrations**: Alembic for schema versioning

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL 17
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: passlib
- **Migrations**: Alembic
- **Containerization**: Docker & Docker Compose

## Project Structure

```
fastapi-test/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for request/response validation
│   ├── service.py           # Business logic layer
│   ├── dependencies.py      # Dependency injection functions
│   ├── exceptions.py        # Custom exception classes
│   ├── database.py          # Database configuration and session management
│   ├── jwt.py               # JWT token creation and validation
│   ├── config.py            # Application configuration
│   └── utils.py             # Utility functions
├── alembic/                 # Database migration scripts
├── docker/
│   └── compose.pg.yml       # Docker Compose configuration
├── pyproject.toml           # Project dependencies
└── README.md
```

## Prerequisites

- Python 3.12+
- Docker & Docker Compose 

## Installation


1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-test
```

2. Start the database and Adminer:
```bash
docker-compose -f docker/compose.pg.yml up -d
```

3. Install dependencies (using uv or pip):
```bash
# Using uv (recommended)
uv sync
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the FastAPI server:
```bash
# Using uv
uv run uvicorn app.main:app --reload --port 8080
```

### Manual Setup

1. Create a PostgreSQL database:
```bash
createdb fastapi_test_db
```

2. Update database connection in `app/database.py`:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/fastapi_test_db"
```

3. Install dependencies and run migrations as above.

## API Endpoints

### Authentication

#### Customer Login
```http
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "id": "uuid",
  "customer_name": "John Doe",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "created_at": "2024-01-01 12:00:00",
  "updated_at": "2024-01-01 12:00:00"
}
```

#### Admin Login
```http
POST /admin/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "88888888"
}
```

**Response:**
```json
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Customers

#### Create Customer
```http
POST /customers
Content-Type: application/json

{
  "customer_name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

#### Get All Customers
```http
GET /customers/all
```

#### Get Current Customer
```http
GET /customers/me
Authorization: Bearer <token>
```

#### Update Customer
```http
PATCH /customers/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "customer_name": "Jane Doe",
  "email": "jane@example.com",
  "password": "newpassword123"
}
```

#### Delete Customer
```http
DELETE /customers/{id}
Authorization: Bearer <token>
```

### Items

#### Create Item
```http
POST /items
Content-Type: application/json

{
  "item_name": "Product Name",
  "price": 29.99,
  "quantity": 100
}
```

#### Get All Items
```http
GET /items
```

#### Update Item
```http
PATCH /items?id={item_id}
Content-Type: application/json

{
  "item_name": "Updated Name",
  "price": 39.99,
  "quantity": 150
}
```

#### Delete Item
```http
DELETE /items?id={item_id}
```

#### Get Admin Items (Admin Only)
```http
GET /admin/items
Authorization: Bearer <admin_token>
```

### Orders

#### Create Order
```http
POST /orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "item_id": "uuid",
  "quantity": 2
}
```

**Note:** This endpoint automatically:
- Validates item exists
- Checks inventory availability
- Uses row-level locking to prevent race conditions
- Updates item quantity atomically

## Configuration

Edit `app/config.py` to customize:

- `SECRET_KEY`: JWT signing key (change in production!)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `ADMIN_EMAIL`: Admin login email
- `ADMIN_PASSWORD`: Admin login password

## Database Schema

The application uses three main models:
- **Customer**: User accounts with authentication
- **Item**: Products with inventory tracking
- **Order**: Customer orders linked to items

![ERD](ERD.png)
See `ERD.png` for the entity relationship diagram.

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Login via `/login` or `/admin/login` to receive a token
2. Include the token in the `Authorization` header:
   ```
   Authorization: Bearer <token>
   ```
3. Tokens expire after 30 minutes (configurable)

## Error Handling

The API uses custom exception classes for consistent error responses:

- `400 Bad Request`: Validation errors, duplicate resources
- `401 Unauthorized`: Authentication/authorization failures
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server errors

## Development

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```


### Running Tests

```python
TODO: pytest
```


## Docker Services

The Docker Compose setup includes:

- **PostgreSQL 17**: Database server on port 5432
- **Adminer**: Database management UI on port 8081

Access Adminer at: http://localhost:8081

## Security Notes

⚠️ **Important**: Before deploying to production:

1. Change the `SECRET_KEY` in `app/config.py`
2. Use environment variables for sensitive configuration
3. Update database credentials
4. Enable HTTPS
5. Implement rate limiting
6. Add input validation and sanitization
7. Review and update password requirements

## References

This project follows best practices and conventions inspired by:

- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) - Opinionated list of best practices and conventions for FastAPI development
- [iThome FastAPI Article](https://ithelp.ithome.com.tw/m/articles/10321483) - FastAPI development guide and best practices
