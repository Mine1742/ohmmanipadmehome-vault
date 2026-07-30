# 🐳 Docker Cheat Sheet

Quick reference for managing containers, images, networks, and Compose setups.

---

## ⚙️ SETUP & INFORMATION

```bash
docker --version
docker info
docker system df                # Show disk usage
docker system prune -a          # Clean up unused data
```

---

## 📦 IMAGES

```bash
docker images                   # List local images
docker pull nginx:latest        # Download image
docker rmi nginx:latest         # Remove image
docker build -t myapp:1.0 .     # Build image from Dockerfile
docker tag myapp:1.0 myrepo/myapp:latest
docker push myrepo/myapp:latest # Push to registry
```

### **Inspect Images**
```bash
docker inspect myapp:1.0
```

---

## 🧱 CONTAINERS

```bash
docker ps                       # Running containers
docker ps -a                    # All containers
docker run -d -p 8080:80 nginx  # Detached container
docker exec -it nginx bash      # Interactive shell
docker logs -f nginx            # Follow logs
docker stop nginx               # Stop container
docker rm nginx                 # Remove container
```

### **Create with Environment Variables**
```bash
docker run -d -e ENV=prod --name web nginx
```

---

## 📂 VOLUMES & PERSISTENCE

```bash
docker volume create appdata
docker volume ls
docker run -v appdata:/var/lib/mysql mysql:latest
docker inspect appdata
```

---

## 🌐 NETWORKING

```bash
docker network ls
docker network create mynet
docker run -d --name web --network=mynet nginx
docker inspect mynet
```

---

## 🧩 DOCKERFILE EXAMPLE

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
```

### **Build & Run**
```bash
docker build -t myflaskapp .
docker run -d -p 8080:8080 myflaskapp
```

---

## 🧰 DOCKER COMPOSE

### **docker-compose.yml**
```yaml
version: '3.9'
services:
  web:
    build: .
    ports:
      - "8080:80"
    volumes:
      - .:/code
    environment:
      - DEBUG=1
  db:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_USER: admin
      POSTGRES_DB: dao_of_life
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

### **Commands**
```bash
docker compose up -d
docker compose ps
docker compose down
docker compose logs -f
```

---

## 🧾 INSPECTING & DEBUGGING

```bash
docker inspect container_name
docker logs container_name
docker top container_name
docker exec -it container_name /bin/bash
docker events --since 1h
```

---

## 🔐 PRIVATE REGISTRIES

```bash
docker login myregistry.io
docker tag myapp myregistry.io/myapp:v1
docker push myregistry.io/myapp:v1
docker pull myregistry.io/myapp:v1
```

---

## 🪄 QUICK REFERENCE SUMMARY

| Task | Command |
|------|----------|
| List containers | `docker ps -a` |
| Run a container | `docker run -d -p 8080:80 nginx` |
| Build image | `docker build -t myapp .` |
| Stop all containers | `docker stop $(docker ps -q)` |
| Remove all containers | `docker rm $(docker ps -aq)` |
| Prune everything | `docker system prune -a` |
| Use Compose | `docker compose up -d` |

---

## 💡 TIPS

- Use `--rm` to auto-remove containers after exit.  
- Use `.dockerignore` to speed up builds.  
- Combine with Terraform or Ansible for full deployments.  
- Prefer `docker compose` over legacy `docker-compose`.  
- Tag consistently: `app:env-version` (e.g., `web:prod-1.2`).

---

**Created for:** containerized app development and DevOps workflows  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #docker #containers #devops #compose #automation
