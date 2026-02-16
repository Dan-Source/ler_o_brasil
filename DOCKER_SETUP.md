# Docker Compose Setup Guide

## Quick Start with Docker Compose

### Prerequisites
- Docker installed
- Docker Compose installed

### Setup Steps

1. **Update `.env` file for Docker** (if using local development):
   ```bash
   # For docker-compose, you can use the default values:
   DB_HOST=db  # Changed from localhost to db (service name)
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=ler_o_brasil
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Run migrations** (if not already done in the web container):
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create a superuser** (optional):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**:
   - Django app: http://localhost:8000
   - Wagtail admin: http://localhost:8000/admin

### Useful Commands

#### View logs:
```bash
docker-compose logs -f web      # Django app logs
docker-compose logs -f db       # PostgreSQL logs
docker-compose logs -f          # All logs
```

#### Stop services:
```bash
docker-compose down
```

#### Stop and remove volumes (careful - loses database data):
```bash
docker-compose down -v
```

#### Access database directly:
```bash
docker-compose exec db psql -U postgres -d ler_o_brasil
```

#### Rebuild containers:
```bash
docker-compose up -d --build
```

#### Run Django management commands:
```bash
docker-compose exec web python manage.py [command]
```

### Database Persistence

The PostgreSQL database is stored in a Docker volume named `ler_o_brasil_postgres_data`. This ensures your data persists even when containers are stopped or removed (unless you use `docker-compose down -v`).

### Environment Variables

The docker-compose.yml reads from your `.env` file. You can override any variable by:

1. **Editing `.env` file** (for local development)
2. **Using command line**:
   ```bash
   DB_PASSWORD=mypassword docker-compose up
   ```
3. **Creating a `.env.docker` file** with different values for container environment

### Troubleshooting

**Connection refused to db:**
- Ensure the `db` service is healthy: `docker-compose ps`
- Wait a few seconds for the database to be ready
- Check database logs: `docker-compose logs db`

**Port already in use:**
```bash
# Change the port in docker-compose.yml
# Or kill existing containers:
docker-compose down
```

**Need to reset everything:**
```bash
# Stop all services and remove volumes
docker-compose down -v
# Rebuild and restart
docker-compose up -d --build
```

### Production Deployment

For production, use environment variables set on your server/container platform (AWS, Heroku, etc.) instead of `.env` file:
- Set DB_HOST, DB_USER, DB_PASSWORD directly in your deployment platform
- The Django settings will read via `os.getenv()` from system environment variables
