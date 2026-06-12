# ⚠️ Arquivo Movido

Este arquivo foi movido para a pasta de documentação centralizada.

**Consulte**: [docs/DOCKER_SETUP.md](docs/DOCKER_SETUP.md)

---

Para um índice completo e guia de início rápido, veja: [docs/README.md](docs/README.md)


### Prerequisites
- Docker installed
- Docker Compose installed

### Setup Steps

1. **The `.env` file is automatically loaded** by docker-compose:
   ```bash
   # docker-compose.yml has 'env_file: .env' configured
   # Default values for development are already set:
   DATABASE_HOST=db  # Service name for Docker
   DATABASE_PORT=5432
   DATABASE_USER=postgres
   DATABASE_PASSWORD=postgres
   DATABASE_NAME=ler_o_brasil
   ```
   See [ENV_SETUP.md](ENV_SETUP.md) for complete environment variable documentation.

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Run migrations and create the default admin** (handled automatically in container startup):
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py create_default_admin
   ```

4. **Access the application**:
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

The PostgreSQL database is stored in a Docker volume named `postgres_data`. This ensures your data persists even when containers are stopped or removed (unless you use `docker-compose down -v`).

### Environment Variables

The `docker-compose.yml` loads variables from your `.env` file using the `env_file: .env` directive. This ensures both Docker and local development use the same configuration.

**Default admin bootstrap variables**:
- `DJANGO_DEFAULT_ADMIN_USERNAME` - default admin username
- `DJANGO_DEFAULT_ADMIN_EMAIL` - default admin email address
- `DJANGO_DEFAULT_ADMIN_PASSWORD` - default admin password
- `DJANGO_DEFAULT_ADMIN_COUNTRY` - country value required by the custom user model

If these are omitted in development, the startup command falls back to safe local defaults. In production, set them explicitly so the created admin is fully configured.

**Key difference for Docker:**
- Use `DATABASE_HOST=db` (the Docker service name)
- For local development, use `DATABASE_HOST=localhost`

You can override variables by:

1. **Editing `.env` file** (affects both Docker and local)
2. **Using command line**:
   ```bash
   DATABASE_PASSWORD=mypassword docker-compose up
   ```

For detailed environment variable setup and configuration, see [ENV_SETUP.md](ENV_SETUP.md).

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

**Environment variables not being read:**
- Verify `.env` file exists in project root
- Check that variables match the names used in `base.py`
- Rebuild containers: `docker-compose down && docker-compose up --build`

### Production Deployment

For production, see [ENV_SETUP.md - Production Deployment](ENV_SETUP.md#production-deployment) section for:
- How to configure environment variables on your server
- Integration with deployment platforms (AWS, Heroku, etc.)
- Security considerations


