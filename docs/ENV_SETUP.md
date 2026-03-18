# Environment Variable Setup Guide

This project has been refactored to load all environment variables from a **single `.env` file** for both Docker and local environments.

## Overview

Previously, environment variables were managed differently for local and Docker environments. Now:

- **Single Source of Truth**: The `.env` file is the only place to configure environment variables
- **Uniform Configuration**: Both local development and Docker use the same `.env` file
- **Simple to Use**: Configure once, run anywhere

## Files Changed

### 1. **`ler_o_brasil/settings/base.py`**
- Loads `.env` file at the very top of the settings module
- All models now use `DATABASE_*` prefixed environment variables for consistency
- Added environment variable support for `WAGTAILADMIN_BASE_URL`

### 2. **`ler_o_brasil/settings/dev.py`**
- Removed redundant `load_dotenv()` call (now handled in base.py)
- Continues to use environment variables for development configuration
- Email backend defaults to console output for development

### 3. **`ler_o_brasil/settings/production.py`**
- Fully populated with environment variable support for all production settings
- Includes validation that required variables are set
- Email, security, and CORS settings all configurable via `.env`

### 4. **`docker-compose.yml`**
- Added `env_file: .env` directive to both `db` and `web` services
- This ensures Docker reads the same `.env` file as local development
- Updated to use `DATABASE_*` prefixed variables instead of `DB_*`

### 5. **`.env`** (Development Configuration)
- Created with sensible development defaults
- Uses `localhost` for database host
- Debug mode enabled
- Console email backend

### 6. **`.envsample`** (Production Template)
- Updated to match new environment variable names
- Serves as a template for production deployments
- Contains all available configuration options with descriptions

## Environment Variables Overview

### Django Core
```
DJANGO_SETTINGS_MODULE     - Settings module to use (dev or production)
DJANGO_SECRET_KEY          - Django secret key
DJANGO_DEBUG               - Debug mode (true/false)
DJANGO_ALLOWED_HOSTS       - Comma-separated list of allowed hosts
```

### Wagtail
```
WAGTAILADMIN_BASE_URL      - Base URL for Wagtail admin backend
```

### Database
```
DATABASE_ENGINE            - Django database backend (default: postgresql)
DATABASE_NAME              - Database name
DATABASE_USER              - Database user
DATABASE_PASSWORD          - Database password
DATABASE_HOST              - Database host (use 'db' for Docker, 'localhost' for local)
DATABASE_PORT              - Database port
```

### Email
```
EMAIL_BACKEND              - Email backend (console for dev, smtp for production)
EMAIL_HOST                 - SMTP host
EMAIL_PORT                 - SMTP port
EMAIL_HOST_USER            - SMTP username
EMAIL_HOST_PASSWORD        - SMTP password
EMAIL_USE_TLS              - Use TLS/SSL
DEFAULT_FROM_EMAIL         - Default sender email
SERVER_EMAIL               - Error notification email
```

### CORS/CSRF
```
DJANGO_CORS_ALLOWED_ORIGINS    - Comma-separated list of allowed origins
DJANGO_CORS_ALLOW_CREDENTIALS  - Allow credentials in CORS requests
DJANGO_CSRF_TRUSTED_ORIGINS    - Comma-separated list of trusted origins
```

### Security (Production)
```
SECURE_SSL_REDIRECT            - Redirect HTTP to HTTPS
SECURE_HSTS_SECONDS            - HSTS max-age
SECURE_HSTS_INCLUDE_SUBDOMAINS - HSTS include subdomains
SECURE_HSTS_PRELOAD            - HSTS preload enabled
SESSION_COOKIE_SECURE          - Secure session cookies
CSRF_COOKIE_SECURE             - Secure CSRF cookies
```

### Static/Media Files
```
STATIC_URL                 - Static files URL
MEDIA_URL                  - Media files URL
```

## Usage

### Local Development

1. **Use the provided `.env` file** (already configured for development):
   ```bash
   # Default configuration is ready to use
   # Database will use localhost:5432
   ```

2. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Run Django management commands**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Docker Development

1. **The `.env` file is automatically used by docker-compose**:
   ```bash
   docker-compose up
   ```

   The `env_file: .env` directive in `docker-compose.yml` ensures all variables are loaded.

2. **For database host**, the `.env` file is configured to use `db` (Docker service name):
   ```
   DATABASE_HOST=db  # Used by Docker
   ```

   To use local development with Docker database, you'd only need to change:
   ```
   DATABASE_HOST=localhost  # For local connections
   ```

### Production Deployment

1. **Copy the template**:
   ```bash
   cp .envsample .env.production
   ```

2. **Configure for production**:
   ```bash
   # Edit .env.production with your production values
   DJANGO_SETTINGS_MODULE=ler_o_brasil.settings.production
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_HOST=your-database-host
   # ... etc
   ```

3. **Use in your deployment**:
   ```bash
   # Load the production environment
   export $(cat .env.production | xargs)
   python manage.py collectstatic
   python manage.py migrate
   gunicorn ler_o_brasil.wsgi:application
   ```

## Multi-Environment Setup

For managing multiple environments with different `.env` files:

```bash
# Development
source venv/bin/activate
# Uses .env by default

# Production (with separate file)
export $(cat .env.production | xargs)
gunicorn ler_o_brasil.wsgi:application

# Staging
export $(cat .env.staging | xargs)
gunicorn ler_o_brasil.wsgi:application
```

## Key Changes Summary

| Item | Before | After |
|------|--------|-------|
| Env var loading | Multiple places | Single location (base.py) |
| Docker compose | Inline environment vars | `env_file: .env` |
| DB variable prefix | `DB_*` | `DATABASE_*` |
| Dev/Docker sync | Manual | Automatic (same `.env` file) |
| Settings module | Hardcoded | `DJANGO_SETTINGS_MODULE` variable |

## Troubleshooting

### Variables not loading in Docker
- Ensure `.env` file exists in project root
- Check that `env_file: .env` is in docker-compose.yml
- Rebuild containers: `docker-compose down && docker-compose up --build`

### Database connection errors when using local environment
- For local development: Set `DATABASE_HOST=localhost`
- For Docker: Set `DATABASE_HOST=db` and run via docker-compose
- Don't mix - use either local OR Docker, not both simultaneously

### Variables not being recognized
- Verify file format: one variable per line, no spaces around `=`
- Ensure no quotes around values unless needed
- Run: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('VARIABLE_NAME'))"`

## Security Notes

⚠️ **Important**: 
- Never commit `.env` files to version control
- `.env` is already in `.gitignore` (if configured)
- Use `.envsample` as a template for new deployments
- Change `DJANGO_SECRET_KEY` for every production deployment
- Never hardcode secrets in settings files

## References

- [python-dotenv documentation](https://github.com/theskumar/python-dotenv)
- [Django settings documentation](https://docs.djangoproject.com/en/5.2/topics/settings/)
- [Docker Compose environment variables](https://docs.docker.com/compose/environment-variables/)
