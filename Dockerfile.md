# Dockerfile Guide

> A comprehensive reference for creating, using, and reasoning about Dockerfiles

---

## What is a Dockerfile?

A Dockerfile is a plain text file containing a series of instructions that Docker reads top-to-bottom to build a **container image**. Think of it as a reproducible recipe: anyone with the file and Docker installed will produce an identical image, regardless of their local machine, OS, or installed software.

The build process works in **layers**. Each instruction creates a new read-only layer stacked on top of the previous one. Docker caches these layers, so if a layer hasn't changed, it doesn't get rebuilt — this makes iterative development fast.

---

## The Mental Model

```
Source Code + Dockerfile  →  docker build  →  Image  →  docker run  →  Container
```

- **Image** — a frozen, immutable snapshot. Like a class definition.
- **Container** — a running instance of an image. Like an object instantiated from a class.
- **Layer** — one instruction's worth of filesystem changes, cached independently.
- **Registry** — remote storage for images (Docker Hub, ACR, GHCR). Like npm for whole environments.

A good Dockerfile should be:

- **Deterministic** — same inputs always produce the same image
- **Minimal** — only what the app needs to run
- **Layered thoughtfully** — things that change less often go earlier (more cacheable)
- **Secure** — no secrets, no root user, no unnecessary attack surface

---

## Dockerfile Instruction Reference

### FROM — Base Image

Every Dockerfile starts with `FROM`. It defines the starting layer your image builds on.

```dockerfile
FROM python:3.11-slim
```

**Variants to know:**

|Tag|What it means|
|---|---|
|`python:3.11`|Full Debian-based image. Largest, most compatible.|
|`python:3.11-slim`|Stripped Debian. Good balance of size and compatibility.|
|`python:3.11-alpine`|Alpine Linux base. Smallest, but musl libc can cause issues.|
|`scratch`|Empty image. Used for statically compiled binaries (Go, Rust).|

```dockerfile
# Always pin to a specific version — never use :latest in production
FROM python:3.11.9-slim

# Multi-stage: name your stages for reference later
FROM python:3.11-slim AS builder
FROM node:20-alpine AS frontend
```

---

### WORKDIR — Set Working Directory

Sets the current directory for all subsequent instructions. Creates it if it doesn't exist.

```dockerfile
WORKDIR /app
```

Always use `WORKDIR` instead of `RUN cd /some/path`. The latter doesn't persist between RUN instructions.

---

### COPY — Copy Files Into the Image

```dockerfile
# Copy a specific file
COPY requirements.txt .

# Copy everything in the current build context
COPY . .

# Copy from a named build stage (multi-stage builds)
COPY --from=builder /app/dist ./dist

# Copy with specific ownership (avoid a separate RUN chown)
COPY --chown=appuser:appuser . .
```

**COPY vs ADD:**

Prefer `COPY` in almost every case. `ADD` has extra magic (auto-extracting tarballs, fetching URLs) that makes behavior less predictable. Only use `ADD` if you specifically need tarball extraction.

---

### RUN — Execute Commands During Build

Each `RUN` creates a new layer. Chain related commands with `&&` to keep layers small and meaningful.

```dockerfile
# Bad — three layers for one logical operation
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good — one layer, clean cache in the same step
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

**Common patterns:**

```dockerfile
# Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Node dependencies
RUN npm ci --only=production

# System packages (Debian/Ubuntu)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
```

---

### ENV — Set Environment Variables

Available during build AND at runtime.

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000
```

Use `ENV` for configuration that the app reads at runtime. Do **not** use it for secrets — environment variables are visible in `docker inspect` and image metadata.

---

### ARG — Build-Time Variables

Only available during `docker build`, not at runtime. Use for build configuration like version pins or feature flags.

```dockerfile
ARG APP_VERSION=1.0.0
ARG BUILD_ENV=production

RUN echo "Building version $APP_VERSION"
```

```bash
docker build --build-arg APP_VERSION=2.1.0 .
```

`ARG` before `FROM` is used to parameterize the base image itself:

```dockerfile
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim
```

---

### EXPOSE — Document Ports

Metadata only — it does not actually publish ports. It tells humans and orchestration tools which port the app listens on.

```dockerfile
EXPOSE 8000
```

The actual port mapping happens at runtime: `docker run -p 8080:8000`

---

### CMD and ENTRYPOINT — Define What Runs

These two work together and are often confused.

**ENTRYPOINT** — the executable. Rarely overridden. **CMD** — default arguments to ENTRYPOINT. Easily overridden.

```dockerfile
# Shell form (runs as /bin/sh -c "..." — no signal forwarding)
CMD python app.py

# Exec form (preferred — runs directly, handles signals correctly)
CMD ["python", "app.py"]

# ENTRYPOINT + CMD pattern (most flexible)
ENTRYPOINT ["python"]
CMD ["app.py"]
```

With the ENTRYPOINT + CMD pattern, you can override just the arguments at runtime:

```bash
docker run myimage app.py          # uses CMD default
docker run myimage other_script.py # overrides CMD
```

**When to use which:**

|Scenario|Use|
|---|---|
|Simple app, one way to run|`CMD ["python", "app.py"]`|
|App with swappable subcommands|`ENTRYPOINT` + `CMD`|
|Wrapper script that sets up env|`ENTRYPOINT ["./entrypoint.sh"]`|

---

### USER — Drop Root Privileges

Containers run as root by default. Always switch to a non-root user before the final `CMD`.

```dockerfile
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

USER appuser
```

---

### VOLUME — Declare Mount Points

Documents that a directory is intended to be a mount point for persistent data or host-mounted directories.

```dockerfile
VOLUME ["/data", "/logs"]
```

Like `EXPOSE`, this is mostly documentation. Actual mounts are specified at `docker run` time.

---

### HEALTHCHECK — Container Self-Reporting

Tells Docker how to test if the container is healthy. Used by orchestrators like Kubernetes and Docker Swarm.

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

---

### LABEL — Image Metadata

Attach metadata for tooling, registries, and documentation.

```dockerfile
LABEL maintainer="albert@archkey.com" \
      version="1.0.0" \
      description="ArchKey internal API service"
```

---

## Layer Caching — The Most Important Concept

Docker checks each instruction against its cache. If the instruction and its inputs haven't changed, Docker reuses the cached layer and skips the build step. **Once a layer is invalidated, all subsequent layers are rebuilt.**

This means **instruction order matters enormously**:

```dockerfile
# BAD — copying all source code before installing dependencies
# Any code change invalidates the pip install layer
COPY . .
RUN pip install -r requirements.txt

# GOOD — install dependencies first, then copy code
# pip install is only re-run when requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

**The golden rule:** Put instructions that change less frequently earlier in the file.

**Cache invalidation triggers:**

- The instruction itself changes
- Files copied with `COPY` or `ADD` change
- An `ARG` value changes
- The cache for a previous layer was invalidated

---

## Multi-Stage Builds

Multi-stage builds let you use one image to build your app and a different (smaller) image to run it. The final image contains only the runtime artifacts — no compilers, build tools, or intermediate files.

### Python Example

```dockerfile
# Stage 1: Build — install everything including dev tools
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages into a prefix directory
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime — only copy what we need to run
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Node.js Example

```dockerfile
# Stage 1: Build frontend assets
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: Build backend dependencies
FROM python:3.11-slim AS backend-builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 3: Final runtime image
FROM python:3.11-slim

WORKDIR /app

COPY --from=backend-builder /install /usr/local
COPY --from=frontend-builder /frontend/dist ./static
COPY backend/ .

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
```

---

## .dockerignore

Like `.gitignore`, but for the Docker build context. Excludes files from being sent to the Docker daemon during build. Critical for performance and security.

```
# Version control
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.egg-info
dist/
build/
.venv/
venv/
env/

# Node
node_modules/
npm-debug.log

# Environment and secrets
.env
.env.*
*.key
*.pem
secrets/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile*
docker-compose*

# Tests and docs (usually not needed at runtime)
tests/
docs/
README.md
```

---

## Complete Examples

### Flask API

```dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### FastAPI / Uvicorn

```dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Node.js Express

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine

ENV NODE_ENV=production \
    PORT=3000

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY . .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s \
    CMD node -e "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "server.js"]
```

### .NET 8 API

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS builder

WORKDIR /src
COPY *.csproj ./
RUN dotnet restore

COPY . .
RUN dotnet publish -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0

WORKDIR /app
COPY --from=builder /app/publish .

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080

ENTRYPOINT ["dotnet", "MyApi.dll"]
```

---

## Security Best Practices

### Never store secrets in images

```dockerfile
# WRONG — secret baked into the image layer forever
ENV DB_PASSWORD=supersecret
RUN curl -H "Authorization: Bearer mytoken" https://api.example.com

# RIGHT — pass secrets at runtime
# docker run -e DB_PASSWORD=$DB_PASSWORD myimage
# Or use Docker secrets / Azure Key Vault / environment injection
```

### Always run as non-root

```dockerfile
# Debian/Ubuntu-based
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --no-create-home appuser
USER appuser

# Alpine-based
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

### Use specific image digests in production

```dockerfile
# Tag-based (tag can be reassigned — less deterministic)
FROM python:3.11-slim

# Digest-based (cryptographically pinned — fully deterministic)
FROM python:3.11-slim@sha256:abc123...
```

### Minimize installed packages

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \   # <-- only what you need
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*                    # <-- always clean up
```

### Scan images for vulnerabilities

```bash
# Docker Scout (built into Docker Desktop)
docker scout cves myimage:latest

# Trivy (open source)
trivy image myimage:latest

# Grype
grype myimage:latest
```

---

## Build Commands Reference

```bash
# Basic build (tags image as myapp:latest)
docker build -t myapp:latest .

# Build with a specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build with build args
docker build --build-arg APP_VERSION=2.0.0 -t myapp:2.0.0 .

# Build targeting a specific stage (useful for testing build stages)
docker build --target builder -t myapp:builder .

# Build with no cache (force full rebuild)
docker build --no-cache -t myapp:latest .

# Build and push to registry in one step (BuildKit)
docker buildx build --platform linux/amd64,linux/arm64 \
    -t myregistry.azurecr.io/myapp:latest --push .

# Build for a different platform (useful on Apple Silicon)
docker buildx build --platform linux/amd64 -t myapp:latest .
```

---

## Running Containers

```bash
# Run interactively (attach terminal)
docker run -it myapp:latest /bin/sh

# Run detached (background)
docker run -d --name myapp myapp:latest

# Map ports (host:container)
docker run -d -p 8080:8000 myapp:latest

# Pass environment variables
docker run -d -e DB_HOST=localhost -e DB_PORT=5432 myapp:latest

# Load env from file
docker run -d --env-file .env myapp:latest

# Mount a volume
docker run -d -v /host/path:/container/path myapp:latest
docker run -d -v myvolume:/data myapp:latest

# Set resource limits
docker run -d --memory="512m" --cpus="1.0" myapp:latest

# Override the CMD
docker run myapp:latest python manage.py migrate

# One-shot command (auto-remove when done)
docker run --rm myapp:latest python -c "import sys; print(sys.version)"
```

---

## Inspecting and Debugging

```bash
# List images
docker images

# Show image layers and history
docker history myapp:latest

# Inspect image metadata (env, entrypoint, labels, etc.)
docker inspect myapp:latest

# Show running containers
docker ps

# Show all containers (including stopped)
docker ps -a

# View logs
docker logs myapp
docker logs -f myapp          # Follow (tail -f equivalent)
docker logs --tail 100 myapp  # Last 100 lines

# Shell into a running container
docker exec -it myapp /bin/sh

# Copy a file from a running container
docker cp myapp:/app/logs/error.log ./error.log

# Check resource usage
docker stats

# Show image size breakdown
docker image inspect myapp:latest --format='{{.Size}}'
```

---

## Common Patterns

### Entrypoint wrapper script

Use a shell script as entrypoint to run initialization before the main process:

```bash
#!/bin/sh
# entrypoint.sh

set -e

# Run database migrations before starting the app
python manage.py migrate --noinput

# Then exec the CMD (replaces shell with app process for proper signal handling)
exec "$@"
```

```dockerfile
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "app:app"]
```

### Development vs production Dockerfiles

```dockerfile
# Dockerfile (production)
FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app"]

# Dockerfile.dev (development — mounts source, hot reload)
FROM python:3.11-slim
WORKDIR /app
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
# Source code is mounted via docker-compose volume, not COPY'd
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
```

### Pinning dependency versions

```dockerfile
# requirements.txt — pin everything for reproducible builds
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
pydantic==2.7.1
```

---

## Docker Compose Integration

Dockerfiles work hand-in-hand with `docker-compose.yml` for local development:

```yaml
version: "3.9"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
      args:
        APP_VERSION: dev
    ports:
      - "8000:8000"
    volumes:
      - .:/app              # Mount source for hot reload
    environment:
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      db:
        condition: service_healthy
    env_file:
      - .env.dev

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: appdb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

```bash
# Build and start all services
docker compose up --build

# Start in background
docker compose up -d --build

# View logs from all services
docker compose logs -f

# Run a one-off command in a service
docker compose run --rm api python manage.py createsuperuser

# Stop and remove containers (keep volumes)
docker compose down

# Stop and remove containers AND volumes
docker compose down -v
```

---

## Azure-Specific Patterns

### Build and push to Azure Container Registry

```bash
# Login to ACR
az acr login --name myregistry

# Build and push
docker build -t myregistry.azurecr.io/myapp:v1.0.0 .
docker push myregistry.azurecr.io/myapp:v1.0.0

# Or use ACR Tasks to build in the cloud (no local Docker needed)
az acr build --registry myregistry --image myapp:v1.0.0 .
```

### Deploy to Azure Container Apps

```bash
az containerapp create \
  --name myapp \
  --resource-group my-rg \
  --environment myenv \
  --image myregistry.azurecr.io/myapp:v1.0.0 \
  --registry-server myregistry.azurecr.io \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 5 \
  --env-vars DB_HOST=secretref:db-host DB_PORT=5432
```

### Deploy to Azure App Service

```bash
az webapp create \
  --name myapp \
  --resource-group my-rg \
  --plan my-plan \
  --deployment-container-image-name myregistry.azurecr.io/myapp:v1.0.0

az webapp config container set \
  --name myapp \
  --resource-group my-rg \
  --docker-custom-image-name myregistry.azurecr.io/myapp:v1.0.0 \
  --docker-registry-server-url https://myregistry.azurecr.io
```

---

## Troubleshooting

|Problem|Likely cause|Fix|
|---|---|---|
|Build is slow every time|`COPY . .` before `RUN pip install`|Move dependency install before copying source|
|Image is huge|No `.dockerignore`, not using multi-stage, full base image|Add `.dockerignore`, use slim/alpine, use multi-stage|
|App can't write to disk|Running as non-root, no write permission|`chown` the target directory to the app user|
|Container exits immediately|CMD process exits, or crashes at start|`docker logs <container>` to see output; use exec form for CMD|
|Port not accessible|EXPOSE doesn't publish ports|Use `-p host:container` at runtime|
|`apt-get` fails mid-build|Stale cache layer has old package lists|`docker build --no-cache` or add `--no-cache` to apt-get|
|Works locally, fails in CI|Build context difference, missing file|Check `.dockerignore`, verify CI build context|
|Secrets exposed in `docker inspect`|Used `ENV` or `ARG` for secrets|Pass secrets at runtime via `-e` or secret management|

---

## Quick Reference Cheat Sheet

```dockerfile
FROM image:tag                          # Base image (always first)
FROM image:tag AS stagename             # Named stage for multi-stage

WORKDIR /app                            # Set working directory

COPY source dest                        # Copy files from build context
COPY --from=stagename /src /dest        # Copy from another stage

RUN command && \                        # Execute during build
    another command                     # Chain with && to minimize layers

ENV KEY=value                           # Runtime environment variable
ARG KEY=default                         # Build-time variable only

EXPOSE 8000                             # Document port (metadata only)

USER appuser                            # Switch to non-root user

LABEL key=value                         # Image metadata

HEALTHCHECK --interval=30s CMD ...      # Health probe

ENTRYPOINT ["executable"]               # Fixed executable
CMD ["arg1", "arg2"]                    # Default args (overridable)

VOLUME ["/data"]                        # Declare mount point
```

---

_Last updated: 2026 | Tags: #docker #containers #devops #azure #az204_