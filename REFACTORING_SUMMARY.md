# ⚠️ Arquivo Movido

Este arquivo foi movido para a pasta de documentação centralizada.

**Consulte**: [docs/REFACTORING_SUMMARY.md](docs/REFACTORING_SUMMARY.md)

---

Para um índice completo e guia de início rápido, veja: [docs/README.md](docs/README.md)


### 1. **ler_o_brasil/settings/base.py**
**Status**: ✅ Updated

**Changes**:
- Confirmed `load_dotenv(BASE_DIR / ".env")` at the top of the file (loads once)
- Updated database variables to use `DATABASE_*` prefix instead of `DB_*`:
  - `DB_ENGINE` → `DATABASE_ENGINE`
  - `DB_NAME` → `DATABASE_NAME`
  - `DB_USER` → `DATABASE_USER`
  - `DB_PASSWORD` → `DATABASE_PASSWORD`
  - `DB_HOST` → `DATABASE_HOST`
  - `DB_PORT` → `DATABASE_PORT`
- Added environment variable support for `WAGTAILADMIN_BASE_URL`

**Benefits**:
- Single source of truth for Django configuration
- No redundant `load_dotenv()` calls in child settings
- Consistent variable naming across the project

---

### 2. **ler_o_brasil/settings/dev.py**
**Status**: ✅ Updated

**Changes**:
- Removed redundant `from dotenv import load_dotenv` import
- Removed redundant `load_dotenv()` call (handled in base.py)
- Kept all environment variable configurations
- Email backend defaults to console for development

**Benefits**:
- Cleaner code without duplication
- Single point of environment variable loading

---

### 3. **ler_o_brasil/settings/production.py**
**Status**: ✅ Enhanced

**Changes**:
- Added comprehensive environment variable support
- Added validation for required production variables
- Configured all major settings from environment variables:
  - Email settings (SMTP, sender, etc.)
  - CORS/CSRF origins
  - Security settings (SSL, HSTS, secure cookies)
  - Wagtail admin base URL

**Code Added**:
```python
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is not set")
# ... etc
```

**Benefits**:
- Production settings are now fully configurable via environment
- Explicit validation prevents operating with incomplete configuration
- No hardcoded production credentials

---

### 4. **docker-compose.yml**
**Status**: ✅ Updated

**Changes**:
- Added `env_file: .env` to both `db` and `web` services
- Updated environment variable references from `DB_*` to `DATABASE_*`:
  - `${DB_NAME}` → `${DATABASE_NAME}`
  - `${DB_USER}` → `${DATABASE_USER}`
  - `${DB_PASSWORD}` → `${DATABASE_PASSWORD}`
- Removed hardcoded `DEBUG=True` (controlled by `.env`)

**Before**:
```yaml
environment:
  - DEBUG=True
  - DB_ENGINE=django.db.backends.postgresql
  - DB_NAME=${DB_NAME:-ler_o_brasil}
```

**After**:
```yaml
env_file: .env
environment:
  - DATABASE_ENGINE=django.db.backends.postgresql
  - DATABASE_NAME=${DATABASE_NAME:-ler_o_brasil}
```

**Benefits**:
- Single `.env` file used by both Docker and local environments
- Docker automatically loads all environment variables
- Consistent configuration across all environments

---

### 5. **.env** (Development Configuration)
**Status**: ✅ Updated

**Changes**:
- Updated all `DB_*` variables to `DATABASE_*`
- Set sensible development defaults:
  - `DJANGO_SETTINGS_MODULE=ler_o_brasil.settings.dev`
  - `DEBUG=true`
  - `DATABASE_HOST=db` (for Docker)
  - `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`
  - Security settings disabled for development
- Added comprehensive comments for each section

**Key Values**:
```env
DATABASE_HOST=db                # For Docker (use 'localhost' for local)
DATABASE_PASSWORD=postgres
DJANGO_DEBUG=true
EMAIL_BACKEND=console
SECURE_SSL_REDIRECT=false
```

---

### 6. **.envsample** (Production Template)
**Status**: ✅ Updated

**Changes**:
- Updated all `DB_*` variables to `DATABASE_*`
- Changed `DATABASE_URL` to individual `DATABASE_*` variables
- Updated `DJANGO_SETTINGS_MODULE=ler_o_brasil.settings.production`
- Set production-appropriate defaults:
  - `DEBUG=false`
  - `SECURE_SSL_REDIRECT=true`
  - `EMAIL_BACKEND=smtp`
  - Security headers enabled

**Purpose**:
- Serves as template for production deployments
- Documents all available environment variables
- Clear instructions on what values to change

---

### 7. **DOCKER_SETUP.md**
**Status**: ✅ Updated

**Changes**:
- Updated documentation to reflect new environment variable names
- Removed instructions to manually set `DB_*` variables
- Added reference to ENV_SETUP.md for comprehensive documentation
- Updated troubleshooting section
- Added notes about using `DATABASE_HOST=localhost` for local vs `db` for Docker

---

### 8. **ENV_SETUP.md** (NEW FILE)
**Status**: ✅ Created

**Purpose**: Comprehensive guide for environment variable setup

**Contents**:
- Overview of changes
- Complete environment variables reference
- Usage instructions for:
  - Local development
  - Docker development
  - Production deployment
- Multi-environment setup patterns
- Security notes and best practices
- Troubleshooting guide

---

## Environment Variable Mapping

### Old → New Names
| Old | New |
|-----|-----|
| `DB_ENGINE` | `DATABASE_ENGINE` |
| `DB_NAME` | `DATABASE_NAME` |
| `DB_USER` | `DATABASE_USER` |
| `DB_PASSWORD` | `DATABASE_PASSWORD` |
| `DB_HOST` | `DATABASE_HOST` |
| `DB_PORT` | `DATABASE_PORT` |

### New Variables Added
- `DJANGO_SETTINGS_MODULE`
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_ENGINE` (replaces `DB_ENGINE`)
- `EMAIL_*` (full email configuration suite)
- `SECURE_*` (security settings suite)
- `CORS_*` (CORS configuration)

---

## How It Works Now

```
┌─────────────────────────────────────┐
│         .env File                   │
│  (single source of truth)           │
└────────────┬────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌─────────────┐  ┌──────────────────┐
│   Local     │  │  Docker Compose  │
│   Dev       │  │  (env_file)      │
│             │  │                  │
│ manage.py   │  │ docker-compose   │
│ runserver   │  │ up               │
└─────────────┘  └──────────────────┘
      │             │
      └──────┬──────┘
             │
      ┌──────▼──────────┐
      │ ler_o_brasil/   │
      │ settings/       │
      │ base.py         │
      │ load_dotenv()   │
      └─────────────────┘
```

### Local Development
1. Copy `.env` to your machine
2. Run `python manage.py runserver`
3. Settings module auto-loads from `.env` (via `load_dotenv()`)

### Docker Development
1. `.env` file in project root
2. Run `docker-compose up`
3. Docker automatically loads `.env` via `env_file: .env`

---

## Testing the Setup

### Verify environment variables are loaded:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('DATABASE_NAME'))"
```

### Expected output:
```
ler_o_brasil
```

### Test Docker setup:
```bash
docker-compose config | grep "DATABASE_NAME"
```

---

## Breaking Changes

⚠️ **If updating existing setup:**

1. **Environment Variable Names Changed**
   - Old: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
   - New: `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT`
   - **Action**: Update any `.env` files or environment configurations

2. **Settings Module**
   - Old: Often hardcoded in files
   - New: Must be set via `DJANGO_SETTINGS_MODULE` environment variable
   - **Action**: Add `DJANGO_SETTINGS_MODULE=ler_o_brasil.settings.dev` to your `.env`

3. **Docker Deployment**
   - Old: Inline environment variables
   - New: Uses `env_file: .env`
   - **Action**: Ensure `.env` file exists with correct variables

---

## Files Affected Summary

| File | Change Type | Status |
|------|------------|--------|
| `ler_o_brasil/settings/base.py` | Modified | ✅ |
| `ler_o_brasil/settings/dev.py` | Modified | ✅ |
| `ler_o_brasil/settings/production.py` | Enhanced | ✅ |
| `docker-compose.yml` | Modified | ✅ |
| `.env` | Updated | ✅ |
| `.envsample` | Updated | ✅ |
| `DOCKER_SETUP.md` | Updated | ✅ |
| `ENV_SETUP.md` | Created | ✅ |

---

## Next Steps (Optional)

1. **For existing deployments**: Update your environment configuration to use new variable names
2. **For CI/CD pipelines**: Update environment variables in your CI/CD platform (GitHub Actions, GitLab CI, etc.)
3. **For team members**: Update local `.env` files with new variable names
4. **For production**: Use `.envsample` as template to configure your production environment

---

## References

- See [ENV_SETUP.md](ENV_SETUP.md) for comprehensive setup guide
- See [DOCKER_SETUP.md](DOCKER_SETUP.md) for Docker-specific instructions
- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [Django Settings Documentation](https://docs.djangoproject.com/en/5.2/topics/settings/)
- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/)
