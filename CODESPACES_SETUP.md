# GitHub Codespaces Setup Guide

This project is configured to automatically build and start when creating a new GitHub Codespace.

## What Happens Automatically

1. **Codespace Creation**: When you create a new Codespace, the `.devcontainer/devcontainer.json` configuration is used
2. **Auto-Build**: Docker Compose automatically builds all services (database, backend, frontend)
3. **Auto-Start**: All services start automatically via `postCreateCommand`
4. **Port Forwarding**: Ports 8080 (backend) and 3000 (frontend) are automatically forwarded

## Manual Commands (if needed)

If you need to manually control the services:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Accessing the Application

- **Frontend**: http://localhost:3000 (or use Codespace port forwarding)
- **Backend API**: http://localhost:8080/api/health
- **WebSocket**: ws://localhost:8080/ws/medications or ws://localhost:8080/ws/vitals

## Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your configuration (if needed)

**Note**: `.env` is gitignored and will not be committed to version control.
