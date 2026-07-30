#docker #webapp 
Below is a step‐by‐step guide on creating a Dockerfile for your Flask application.

---

### 1. Create a File Named `Dockerfile` (No Extension)

In the root of your project folder, create a file named **Dockerfile** (with no extension).

---

### 2. Write the Dockerfile

Here’s an example Dockerfile for a Flask app:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . /app

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set environment variables (optional, you can also use a .env file)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Start the Flask app. 
# The "--host=0.0.0.0" flag ensures the app is accessible from outside the container.
CMD ["flask", "run", "--host=0.0.0.0"]
```

**Notes:**

- **FROM python:3.10-slim**  
    This uses a lightweight Python 3.10 image. You can adjust the version as needed.
    
- **WORKDIR /app**  
    This sets the working directory inside the container to `/app`.
    
- **COPY requirements.txt /app/**  
    This copies your `requirements.txt` into the container so you can install your dependencies.
    
- **RUN pip install --no-cache-dir -r requirements.txt**  
    This installs the dependencies.
    
- **COPY . /app**  
    This copies all your project files (including your application code and templates) into the container.
    
- **EXPOSE 5000**  
    This tells Docker that the container will listen on port 5000.
    
- **CMD ["flask", "run", "--host=0.0.0.0"]**  
    This runs your Flask application when the container starts.
    

---

### 3. Build and Run the Docker Container

Open a terminal in your project directory (where the Dockerfile is located) and run the following commands:

#### Build the Docker Image

```bash
docker build -t my-flask-app .
```

This command builds a Docker image named **my-flask-app** using the Dockerfile in the current directory.

#### Run the Docker Container

```bash
docker run -p 5000:5000 my-flask-app
```

This maps port 5000 of your container to port 5000 on your host machine. You can now open your browser and go to **[http://localhost:5000](http://localhost:5000/)** to see your Flask app.

---

### 4. Optional: Using Environment Variables

If you use a `.env` file for your environment variables, you can mount it into the container or use Docker’s `--env-file` flag. For example:

```bash
docker run -p 5000:5000 --env-file .env my-flask-app
```

This will load environment variables from your `.env` file into the container.

---

Below is a simple example of how you can use **Docker Compose** to manage and run your Flask app container (along with any other services you might need). Let’s assume you already have:

- A `Dockerfile` for building your Flask app image (named `my-flask-app`).
- A `.env` file that contains environment variables for your Notion secrets, database IDs, etc.
- A `requirements.txt` listing your Python dependencies.

Below is an example **docker-compose.yml** file and instructions on how to use it.

---

## **1. Example docker-compose.yml**

Create or edit a file named **docker-compose.yml** in the root of your project:

```yaml
version: "3.9"

services:
  web:
    build: .
    container_name: my-flask-app-container
    ports:
      - "5000:5000"
    env_file:
      - .env
    # If you want to run a command different from what's in the Dockerfile:
    # command: gunicorn app:app --bind 0.0.0.0:5000 --timeout 120
    volumes:
      - .:/app
```

**Explanation:**

- **version**: The Docker Compose file format version.
- **services**: You define services here—like `web` for your Flask app.
- **build: .**: Tells Docker Compose to build an image from the Dockerfile in the current directory.
- **container_name**: An optional name for the container.
- **ports**: Maps port 5000 on the host to port 5000 in the container (the same mapping as `-p 5000:5000`).
- **env_file**: Tells Docker Compose to load environment variables from `.env`.
- **volumes**: If you want changes on your host files to reflect inside the container without rebuilding, you can mount your current directory `.` to `/app` in the container. This is useful for development, but in production, you might omit it.

---

## **2. Building and Running with Docker Compose**

Once you have `docker-compose.yml` in place, you can do:

```bash
docker-compose build
```

This builds the image based on your Dockerfile. Then run:

```bash
docker-compose up
```

This starts the container, mapping port 5000 as configured. Check your terminal output for logs. If everything is correct, you can visit **[http://localhost:5000](http://localhost:5000/)** in your browser to see your Flask app.

---

## **3. Environment Variables**

In your `.env` file (used by Docker Compose), you might have lines like:

```env
FLASK_APP=app.py
FLASK_ENV=development
NOTION_SECRET=your_secret_here
NOTION_DATABASE_ID_LOGIN=some_uuid
NOTION_DATABASE_ID_STU_INFO=some_uuid
NOTION_DATABASE_ID_CERT_ATTEMPTS=some_uuid
NOTION_DATABASE_ID_CERTS=some_uuid
NOTION_DATABASE_ID_PROGRAMS=some_uuid
```

Make sure there are **no spaces** around `=`. For example:

```
FLASK_APP=app.py
```

(not `FLASK_APP = app.py`).

---

## **4. Using Gunicorn in Docker Compose**

If you prefer Gunicorn over the built-in Flask server, you can either specify it in your Dockerfile’s `CMD` or override it in your `docker-compose.yml` with a `command` key:

```yaml
services:
  web:
    build: .
    container_name: my-flask-app-container
    ports:
      - "5000:5000"
    env_file:
      - .env
    command: gunicorn app:app --bind 0.0.0.0:5000 --timeout 120
    volumes:
      - .:/app
```

Then run `docker-compose up`.

---

## **5. Troubleshooting**

- **Check Logs**: If you see errors, run `docker-compose logs web` or just look at the terminal output to see the error messages.
- **Verify .env**: Make sure Docker Compose is actually reading your `.env` file. The format must be `KEY=VALUE`.
- **Stop/Remove Containers**: If you need to rebuild or start fresh, do:
    
    ```bash
    docker-compose down
    docker-compose build
    docker-compose up
    ```
    
- **Production vs. Development**: In production, you might not want to mount volumes or run in `development` mode. Adjust your Compose file accordingly.

---

**Summary:**

1. Create `docker-compose.yml` with a `web` service pointing to your Dockerfile and exposing port 5000.
2. Specify your environment variables in a `.env` file and reference it with `env_file`.
3. Run `docker-compose up` to build and start your container.
4. Access your app at `http://localhost:5000`.

That’s it! You now have a straightforward Docker Compose setup for your Flask app. Let me know if you have any other questions!