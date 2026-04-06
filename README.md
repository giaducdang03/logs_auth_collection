# SSH Auth Log Monitoring System

A full-stack web application for monitoring and analyzing SSH authentication logs on Ubuntu/Linux systems.

## Features

- **Real-time SSH Log Collection** - Automatically reads and parses `/var/log/auth.log`
- **User Authentication** - JWT-based authentication with bcrypt password hashing
- **Advanced Search & Filtering** - Search by username, IP address, status, and date range
- **Pagination** - Efficient log viewing with configurable page sizes
- **RESTful API** - Comprehensive API with Swagger documentation
- **Modern UI** - React + TypeScript frontend with responsive design
- **Database** - PostgreSQL with optimized indexes for fast queries

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **APScheduler** - Background task scheduling
- **Pydantic** - Data validation
- **Python-Jose** - JWT token handling

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Axios** - HTTP client
- **React Router** - Routing

### DevOps
- **Docker** - Container platform
- **Docker Compose** - Multi-container orchestration

## Project Structure

```
ubuntu_auth_log/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── repositories/   # Database access
│   │   ├── tasks/          # Background jobs
│   │   ├── utils/          # Utilities
│   │   ├── middleware/     # Authentication middleware
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # DB setup
│   │   └── main.py         # FastAPI app
│   ├── scripts/
│   │   └── seed_data.py   # Database seed script
│   ├── tests/              # Unit tests
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Docker build
│   └── .env.example        # Environment template
│
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # React hooks
│   │   ├── api/            # API client
│   │   ├── types/          # TypeScript types
│   │   ├── utils/          # Utilities
│   │   ├── App.tsx         # Main app
│   │   └── main.tsx        # Entry point
│   ├── public/             # Static files
│   ├── package.json        # npm dependencies
│   ├── vite.config.ts      # Vite configuration
│   ├── tsconfig.json       # TypeScript config
│   ├── Dockerfile          # Docker build
│   ├── .env.example        # Environment template
│   └── index.html          # HTML template
│
├── docker-compose.yml      # Multi-container setup
├── README.md               # This file
└── docs/
    └── API.md              # API documentation
```

## Quick Start

### Prerequisites

- Docker & Docker Compose (recommended)
- OR: Python 3.11+, Node 18+, PostgreSQL 15+

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone and navigate to project
cd ubuntu_auth_log

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Build and start all services
docker-compose up -d

# Seed database with test data
docker exec ssh_log_backend python -m scripts.seed_data

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env

# Update .env with your database credentials
# DB_HOST=localhost
# JWT_SECRET=your-secret-key-here

# Initialize database
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Seed test data
python -m scripts.seed_data

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment
cp .env.example .env

# Start dev server
npm run dev
```

## Usage

### Test Credentials

After seeding, use these credentials to login:

- **Username:** `admin`
- **Password:** `admin123`

Or register a new account in the login form.

### API Endpoints

#### Authentication

- `POST /api/auth/login` - Login user
- `POST /api/auth/register` - Register new user

#### Logs

- `GET /api/logs` - Get SSH logs with filters

Query parameters:
- `page` (int, default=1) - Page number
- `page_size` (int, default=20) - Items per page
- `username` (string) - Filter by username
- `ip` (string) - Filter by IP address
- `status` (string) - Filter by status ('success'/'failed')
- `from_time` (datetime) - Start time filter
- `to_time` (datetime) - End time filter
- `sort_by` (string, default='login_time') - Sort column
- `sort_order` (string, default='DESC') - Sort order ('ASC'/'DESC')

Example request:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/logs?page=1&page_size=20&status=failed"
```

### Interactive API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

### Environment Variables

#### Backend (.env)

```
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=ubuntu_auth_log

# JWT
JWT_SECRET=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Log Reader
LOG_FILE_PATH=/var/log/auth.log
LOG_READER_INTERVAL_MINUTES=10

# API
API_PREFIX=/api
ENVIRONMENT=production
DEBUG=false
```

#### Frontend (.env)

```
VITE_API_URL=http://localhost:8000/api
```

## Database Schema

### Users Table

Stores system user accounts for accessing the dashboard.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| username | TEXT | Username (unique) |
| password_hash | TEXT | Bcrypt hashed password |
| is_active | BOOLEAN | User status |
| created_at | TIMESTAMP | Creation date |

### SSH Logs Table

Stores parsed SSH authentication logs.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| username | TEXT | SSH user |
| ip_address | INET | Remote IP address |
| login_time | TIMESTAMP | Login timestamp |
| status | TEXT | 'success' or 'failed' |
| auth_method | TEXT | 'password', 'publickey', 'unknown' |
| ssh_key | TEXT | SSH key (if applicable) |
| raw_log | TEXT | Original log line |
| created_at | TIMESTAMP | Insert time |

### User Sessions Table

Tracks web portal login sessions.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | FK to users table |
| login_time | TIMESTAMP | Session start |
| ip_address | INET | Client IP |
| user_agent | TEXT | Browser info |

## Development

### Backend Testing

```bash
cd backend

# Run tests
pytest tests/ -v

# Coverage report
pytest tests/ --cov=app --cov-report=html
```

### Frontend Testing

```bash
cd frontend

# Run tests
npm test
```

### Building

```bash
# Backend
cd backend
python -m py_compile app/**/*.py

# Frontend
cd frontend
npm run build

# Docker images
docker-compose build
```

## Troubleshooting

### Database Connection Error

```
Error: could not connect to server: Connection refused
```

**Solution:** Ensure PostgreSQL is running and credentials are correct in .env

### Permission Denied on /var/log/auth.log

```
Error: Permission denied: '/var/log/auth.log'
```

**Solution:** The application needs root/sudo to read auth.log. In Docker, ensure the container has appropriate permissions or run with `--privileged` flag.

### JWT Token Expired

**Solution:** Clear localStorage and login again. Adjust `JWT_EXPIRATION_HOURS` in .env if needed.

## Performance Optimization

### Database Indexes

The `ssh_logs` table includes optimized indexes for:
- Username searches
- IP address filtering
- Login time range queries
- Status filtering
- Combined queries for dashboard

### API Response Caching

For future enhancements, consider:
- Redis caching for dashboard statistics
- Query result caching
- Frontend response caching

## Security Considerations

1. **JWT Secret** - Change `JWT_SECRET` in production
2. **HTTPS** - Use HTTPS in production (with reverse proxy like Nginx)
3. **CORS** - Configure CORS origins appropriately
4. **Rate Limiting** - Add rate limiting middleware
5. **Input Validation** - All inputs are validated with Pydantic
6. **Password Hashing** - bcrypt with salt rounds
7. **Database** - Use connection encryption, regular backups

## Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Email alerts for suspicious activity
- [ ] GeoIP mapping for login origins
- [ ] Brute-force attack detection
- [ ] Dashboard statistics (phase 2)
- [ ] Role-based access control (RBAC)
- [ ] Export logs to CSV/PDF
- [ ] Multi-factor authentication
- [ ] Audit logging
- [ ] Performance metrics

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Setup Date:** April 6, 2026
**Version:** 1.0.0 MVP
