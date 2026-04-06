# SSH Auth Log Monitor - API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints except `/auth/login` and `/auth/register` require JWT authentication.

**Header:**
```
Authorization: Bearer {access_token}
```

---

## Authentication Endpoints

### Register User

**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- `400 Bad Request` - User already exists or invalid input
- `500 Internal Server Error` - Server error

---

### Login User

**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials
- `500 Internal Server Error` - Server error

---

## Log Endpoints

### Get Logs

**GET** `/logs`

Retrieve SSH authentication logs with optional filtering and pagination.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number (1-indexed) |
| page_size | integer | 20 | Items per page (1-100) |
| username | string | null | Filter by username (substring match) |
| ip | string | null | Filter by IP address (substring match) |
| status | string | null | Filter by status ('success' or 'failed') |
| from_time | datetime | null | Filter from time (ISO 8601) |
| to_time | datetime | null | Filter to time (ISO 8601) |
| sort_by | string | login_time | Column to sort by |
| sort_order | string | DESC | Sort order ('ASC' or 'DESC') |

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/logs?page=1&page_size=20&status=failed&sort_order=DESC"
```

**Response:** `200 OK`
```json
{
  "total": 150,
  "page": 1,
  "page_size": 20,
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "username": "ubuntu",
      "ip_address": "192.168.1.100",
      "login_time": "2026-04-06T15:30:50Z",
      "status": "success",
      "auth_method": "publickey",
      "ssh_key": null,
      "created_at": "2026-04-06T15:30:51Z"
    },
    {
      "id": "223e4567-e89b-12d3-a456-426614174001",
      "username": "root",
      "ip_address": "10.0.0.5",
      "login_time": "2026-04-06T15:25:30Z",
      "status": "failed",
      "auth_method": "password",
      "ssh_key": null,
      "created_at": "2026-04-06T15:25:31Z"
    }
  ]
}
```

**Error Responses:**

`401 Unauthorized` - Invalid or missing token
```json
{
  "detail": "Invalid or expired token"
}
```

`500 Internal Server Error` - Server error
```json
{
  "detail": "Failed to retrieve logs"
}
```

---

## Data Models

### User

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| username | string | Username (unique) |
| is_active | boolean | User active status |
| created_at | datetime | Creation timestamp |

### SSH Log

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| username | string | SSH username |
| ip_address | string | Source IP address |
| login_time | datetime | Login timestamp |
| status | string | 'success' or 'failed' |
| auth_method | string | 'password', 'publickey', or 'unknown' |
| ssh_key | string | SSH public key (if applicable) |
| created_at | datetime | Record creation time |

### Login Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | User login name |
| password | string | Yes | User password |

### Token Response

| Field | Type | Description |
|-------|------|-------------|
| access_token | string | JWT access token |
| token_type | string | Always "bearer" |

### Log List Response

| Field | Type | Description |
|-------|------|-------------|
| total | integer | Total number of matching logs |
| page | integer | Current page number |
| page_size | integer | Items per page |
| data | array | Log records |

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Status | Meaning | Common Cause |
|--------|---------|--------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input parameters |
| 401 | Unauthorized | Missing/invalid authentication token |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server-side error |

---

## Rate Limiting

Currently no rate limiting is implemented. For production, add rate limiting middleware.

---

## CORS

CORS is enabled for all origins. In production, configure to specific domains:

```python
allow_origins=["https://yourdomain.com"]
```

---

## Pagination Guidelines

- **Maximum page_size:** 100
- **Default page_size:** 20
- **Minimum page:** 1
- Use `total` field to determine total pages: `ceil(total / page_size)`

### Example Pagination

Request page 2 with 50 items per page:
```
GET /api/logs?page=2&page_size=50
```

---

## Filtering Examples

### Filter by failed logins
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/api/logs?status=failed"
```

### Filter by username
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/api/logs?username=ubuntu"
```

### Filter by date range
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/api/logs?from_time=2026-04-01T00:00:00Z&to_time=2026-04-07T00:00:00Z"
```

### Combine filters
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/api/logs?username=admin&status=failed&sort_order=ASC"
```

---

## Interactive Documentation

Once the server is running, access interactive API documentation at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Health Check

**GET** `/health`

Check if the API is running.

**Response:** `200 OK`
```json
{
  "status": "ok"
}
```

---

## Version

- **API Version:** v1
- **Last Updated:** April 6, 2026
