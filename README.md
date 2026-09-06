# Prerequisites

Before starting the project, install and configure the following tools.

## 1. Visual Studio Code

Install Visual Studio Code.

We will use VS Code to:

- Write the FastAPI application
- Create Dockerfiles and configuration files
- Create GitHub Actions workflows
- Run commands through the integrated terminal

Open the project in VS Code and use:

```text
Terminal → New Terminal
```

---

## 2. Git

Install Git for Windows.

Verify the installation:

```powershell
git --version
```

Configure your Git identity:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Verify the configuration:

```powershell
git config --global --list
```

Git will be used to version-control the project and push it to GitHub.

---

## 3. Python

Install Python 3.12.

Verify:

```powershell
python --version
```

Also verify pip:

```powershell
pip --version
```

If `python` is not recognized, try:

```powershell
py --version
```

Python is required locally for:

- Creating virtual environments
- Installing dependencies
- Running FastAPI locally
- Running pytest
- Running Flake8

Docker will later provide its own Python environment inside the container.

---

## 4. pip

`pip` is Python's package manager.

We will use it to install packages such as:

```text
fastapi
uvicorn
pytest
httpx
flake8
```

Verify:

```powershell
pip --version
```

If `pip` is not recognized, use:

```powershell
python -m pip --version
```

---

## 5. Docker Desktop

Install Docker Desktop for Windows.

After installation, start Docker Desktop and wait until the Docker Engine is running.

Verify:

```powershell
docker --version
```

Then:

```powershell
docker info
```

`docker info` should return information about the Docker Engine.

### Important

Docker Desktop must be running whenever we use commands such as:

```powershell
docker build
docker run
docker ps
```

---

## 6. Configure Docker Desktop

For Windows, Docker Desktop commonly uses the WSL 2 backend.

Open:

```text
Docker Desktop
→ Settings
→ General
```

Make sure the WSL 2 based engine option is enabled if available.

If you use WSL, check:

```text
Docker Desktop
→ Settings
→ Resources
→ WSL Integration
```

and enable integration with your WSL distribution.

### Important

You do not need to manually use WSL for this project. The project can be completed using the VS Code PowerShell terminal and Docker Desktop.

---

## 7. Test Docker

Run:

```powershell
docker run hello-world
```

If Docker is configured correctly, Docker will download the `hello-world` image and run a test container.

This confirms that:

```text
Docker CLI
    ↓
Docker Engine
    ↓
Docker Container
```

is working correctly.

---

## 8. GitHub Account

Create or sign in to a GitHub account.

We will eventually:

- Create a GitHub repository
- Push the project using Git
- Configure GitHub Actions
- Run automated CI workflows

The repository used for this project is:

```text
containerized-fastapi-cicd
```

---

## 9. Final Environment Check

Before starting Phase 1, run:

```powershell
git --version
python --version
pip --version
docker --version
docker info
```

Finally:

```powershell
docker run hello-world
```

If these commands work successfully, the development environment is ready.

---

# Project Roadmap

We will build the project incrementally.

```text
Prerequisites
      ↓
Phase 1
Basic FastAPI + Docker
      ↓
Phase 2
Testing + Flake8 + Multi-stage Docker + GitHub Actions
      ↓
Phase 3
Alpine + Non-root User + HEALTHCHECK + CI
```

The objective is not simply to make the application work.

With every phase, we will understand **what we are changing, why we are changing it, and what interview concept that change demonstrates**.

---

# Phase 1 — Basic Dockerization

Phase 1 is where we start the project **from scratch**.

The goal is not just to make the FastAPI application run. We want to understand the complete basic Docker workflow:

```text
FastAPI Application
        ↓
Python Dependencies
        ↓
Dockerfile
        ↓
Docker Image
        ↓
Docker Container
        ↓
Application accessible through localhost
```

At this stage, we intentionally keep things simple. We will use an Ubuntu base image and manually install Python inside it.

Later phases will improve this setup.

---

## What We Are Building

We are creating a small FastAPI application with three endpoints:

```text
GET /
GET /health
GET /info
```

Then we will package the application into a Docker image and run it as a container.

---

## 1. Create the Project Directory

Create the main project directory:

```powershell
mkdir docker-project
cd docker-project
```

Open the folder in VS Code:

```powershell
code .
```

### What are we doing?

`docker-project` is the root directory for the entire project.

All phases will live inside this directory:

```text
docker-project/
├── phase-1/
├── phase-2/
└── phase-3/
```

Keeping each phase separate lets us compare how the Docker setup evolves.

---

## 2. Create the Phase-1 Directory

Inside `docker-project`:

```powershell
mkdir phase-1
mkdir phase-1\app
```

We are creating:

```text
phase-1/
└── app/
```

The actual FastAPI application will live inside the `app` directory.

---

## 3. Create the FastAPI Application

Inside:

```text
phase-1\app
```

create:

```text
main.py
```

Contents:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Docker Mastery Project"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/info")
def info():
    return {
        "application": "FastAPI Docker App",
        "version": "1.0.0",
        "environment": "development",
    }
```

### What are we doing?

We are creating a basic FastAPI application.

This line:

```python
app = FastAPI()
```

creates the FastAPI application object.

The decorators:

```python
@app.get("/")
@app.get("/health")
@app.get("/info")
```

define HTTP GET endpoints.

We will later use the `/health` endpoint for Docker's health check in Phase 3.

---

## 4. Create `requirements.txt`

Inside:

```text
phase-1
```

create:

```text
requirements.txt
```

Contents:

```text
fastapi
uvicorn[standard]
```

### What are we doing?

This file tells Python/pip which packages the application needs.

- `fastapi` → web framework
- `uvicorn[standard]` → ASGI server used to run the FastAPI application

We keep dependencies in a separate file instead of installing them one by one.

---

## 5. Create the Python Virtual Environment

Inside `phase-1`:

```powershell
cd phase-1
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the application dependencies:

```powershell
pip install -r requirements.txt
```

### What are we doing?

The virtual environment gives us an isolated Python environment for local development.

Without a virtual environment, installing packages could affect the global Python installation.

Important distinction:

```text
Local development:
venv → used on our computer

Docker:
container → gets its own Python environment
```

The local `venv` is only for development. We will later exclude it using `.dockerignore`.

---

## 6. Run the FastAPI Application Locally

Inside `phase-1`:

```powershell
uvicorn app.main:app --reload
```

The application should start on:

```text
http://127.0.0.1:8000
```

Open:

```text
http://127.0.0.1:8000
```

Expected response:

```json
{
  "message": "Welcome to Docker Mastery Project"
}
```

Test:

```text
http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

Test:

```text
http://127.0.0.1:8000/info
```

You can also open:

```text
http://127.0.0.1:8000/docs
```

This is FastAPI's automatically generated Swagger/OpenAPI documentation.

Stop the development server:

```text
CTRL + C
```

### Why are we doing this before Docker?

We first verify that the application itself works.

This gives us a useful troubleshooting rule:

```text
If it doesn't work locally → fix the application.

If it works locally but not in Docker → investigate the Docker setup.
```

---

## 7. Create `.dockerignore`

Inside:

```text
phase-1
```

create:

```text
.dockerignore
```

Contents:

```text
venv
__pycache__
*.pyc
.git
```

### What are we doing?

When we run:

```powershell
docker build .
```

Docker uses the current directory as the **build context**.

Without `.dockerignore`, unnecessary files could be sent to Docker.

We therefore exclude:

```text
venv
```

Our local virtual environment can contain thousands of files and does not belong inside the image.

```text
__pycache__
*.pyc
```

These are Python cache/compiled files and are not needed.

```text
.git
```

Git metadata is not required by the application.

### Key concept

```text
.dockerignore
      ↓
controls what is sent as Docker build context
```

This becomes especially important as projects become larger.

---

## 8. Create the Phase-1 Dockerfile

Inside:

```text
phase-1
```

create:

```text
Dockerfile
```

Contents:

```dockerfile
FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 9. Understand the Phase-1 Dockerfile

This is one of the most important parts of Phase 1.

We are telling Docker exactly how to construct the environment in which our application will run.

---

### Step 1 — Choose a Base Image

```dockerfile
FROM ubuntu:22.04
```

We start with a general-purpose Ubuntu Linux image.

At this point, the image does not contain the Python environment our application needs.

So we will install Python manually.

### Why is this important?

This is intentionally a basic approach.

Later, in Phase 2, we will replace this with:

```dockerfile
FROM python:3.12-slim
```

That image already provides Python.

So Phase 1 teaches us what is actually happening underneath a higher-level Python base image.

---

### Step 2 — Set the Working Directory

```dockerfile
WORKDIR /app
```

This creates/sets:

```text
/app
```

as the working directory inside the image.

Commands after this point operate relative to `/app`.

Instead of having files scattered around the container, our application will live under:

```text
/app
```

---

### Step 3 — Install Python and pip

```dockerfile
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*
```

We are doing three things:

```text
apt-get update
      ↓
refresh Ubuntu package information

apt-get install
      ↓
install Python 3 and pip

rm -rf /var/lib/apt/lists/*
      ↓
remove unnecessary package-list files
```

This is necessary because our Ubuntu base image does not provide the Python environment required by the application.

---

### Step 4 — Copy Requirements

```dockerfile
COPY requirements.txt .
```

This copies the local:

```text
phase-1/requirements.txt
```

into:

```text
/app/requirements.txt
```

inside the image.

---

### Step 5 — Install Dependencies

```dockerfile
RUN pip3 install --no-cache-dir -r requirements.txt
```

This installs:

```text
FastAPI
Uvicorn
```

inside the Docker image.

`--no-cache-dir` prevents pip from keeping its package cache, helping reduce unnecessary image contents.

---

### Step 6 — Copy the Application

```dockerfile
COPY app/ ./app/
```

This copies:

```text
phase-1/app/
```

into:

```text
/app/app/
```

inside the image.

So the container will contain:

```text
/app
└── app
    └── main.py
```

---

### Step 7 — Document the Port

```dockerfile
EXPOSE 8000
```

This documents that the application listens on port `8000`.

Important:

`EXPOSE` does **not** publish the port to the host by itself.

The actual host-to-container mapping will happen later with:

```powershell
-p 8000:8000
```

---

### Step 8 — Define the Container Startup Command

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

This tells Docker what command should run when the container starts.

We are starting:

```text
uvicorn
```

and telling it to load:

```text
app.main:app
```

which means:

```text
app/
└── main.py
        └── app = FastAPI()
```

---

### Why `0.0.0.0`?

Inside a container, the application must accept connections through the container's network interface.

Therefore we use:

```text
--host 0.0.0.0
```

instead of:

```text
--host 127.0.0.1
```

This is important for accessing the application from the host machine.

---

## 10. Build the Docker Image

### Location

Inside:

```text
phase-1
```

Run:

```powershell
docker build -t docker-mastery:phase1 .
```

### What are we doing?

Docker reads the `Dockerfile` and builds an image from it.

Breakdown:

```text
docker build
```

Build a Docker image.

```text
-t docker-mastery:phase1
```

Give the image:

```text
name = docker-mastery
tag  = phase1
```

```text
.
```

Use the current directory as the Docker build context.

The process is roughly:

```text
Dockerfile
    ↓
execute instructions
    ↓
install Python
    ↓
install dependencies
    ↓
copy application
    ↓
Docker image
```

---

## 11. Check the Docker Image

Run:

```powershell
docker images
```

You should see an image similar to:

```text
docker-mastery    phase1
```

### Image vs Container

At this point we only have an **image**.

An image is a template.

We have not started the application inside a container yet.

```text
Docker Image
     |
     | docker run
     ↓
Docker Container
```

---

## 12. Run the Container

Run:

```powershell
docker run -d --name phase1-app -p 8000:8000 docker-mastery:phase1
```

### What are we doing?

We are creating a container from the image and starting it.

Breakdown:

```text
-d
```

Runs the container in detached/background mode.

```text
--name phase1-app
```

Gives the container a convenient name.

```text
-p 8000:8000
```

Maps:

```text
HOST PORT       CONTAINER PORT
8000      →     8000
```

So:

```text
localhost:8000
```

on our computer reaches:

```text
port 8000
```

inside the container.

Finally:

```text
docker-mastery:phase1
```

is the image from which the container is created.

---

## 13. Check the Running Container

Run:

```powershell
docker ps
```

You should see:

```text
phase1-app
```

and a port mapping similar to:

```text
0.0.0.0:8000->8000/tcp
```

### What is happening?

The architecture is now:

```text
Browser
   |
   | localhost:8000
   ↓
Host machine port 8000
   |
   | Docker port mapping
   ↓
Container port 8000
   |
   ↓
Uvicorn
   |
   ↓
FastAPI
```

---

## 14. Check Container Logs

Run:

```powershell
docker logs phase1-app
```

You should see Uvicorn startup logs.

### Why check logs?

Logs are one of the first places to look when a container starts but the application does not behave as expected.

For example, logs can reveal:

- Python errors
- Import errors
- Missing packages
- Incorrect startup commands
- Port/configuration problems

---

## 15. Test the Dockerized Application

Open:

```text
http://localhost:8000
```

Then:

```text
http://localhost:8000/health
```

Then:

```text
http://localhost:8000/info
```

And:

```text
http://localhost:8000/docs
```

At this point, the FastAPI application is no longer running directly from our local Python environment.

It is running inside the Docker container.

---

## 16. Enter the Running Container

Run:

```powershell
docker exec -it phase1-app bash
```

### What are we doing?

`docker exec` allows us to execute a command inside an already-running container.

Inside the container:

```bash
ls
```

You should see something similar to:

```text
app
requirements.txt
```

Then:

```bash
ls app
```

You should see:

```text
main.py
```

This lets us inspect what actually exists inside the container.

Exit:

```bash
exit
```

---

## 17. Stop and Remove the Container

When finished testing:

```powershell
docker stop phase1-app
```

This stops the running container.

Remove it:

```powershell
docker rm phase1-app
```

Check running containers:

```powershell
docker ps
```

Check all containers, including stopped ones:

```powershell
docker ps -a
```

### Important distinction

```text
docker stop
```

stops a container.

```text
docker rm
```

removes a container.

The image still exists.

Check it:

```powershell
docker images
```

The image:

```text
docker-mastery:phase1
```

can still be used to create another container.

---

## Phase-1 Architecture

```text
                  LOCAL MACHINE
                       |
                       |
                 FastAPI Source
                       |
                       v
                  Dockerfile
                       |
                       v
              Docker Build Context
                       |
                       v
                Docker Image
            docker-mastery:phase1
                       |
                 docker run
                       |
                       v
                Docker Container
                   phase1-app
                       |
                       v
                    Uvicorn
                       |
                       v
                    FastAPI
                       |
                       v
                 Port 8000
                       |
                       v
              http://localhost:8000
```

---

# Phase-1 Interview Notes

## What did we do?

> We created a FastAPI application and containerized it using Docker. We started with an Ubuntu base image, manually installed Python and pip, installed the application's dependencies, copied the application into the image, and ran it using Uvicorn inside a Docker container.

---

## Why Docker?

Docker packages an application together with its runtime environment and dependencies.

Without Docker:

```text
Developer machine
    ↓
Python version
    ↓
Installed packages
    ↓
Application
```

Different machines may have different configurations.

With Docker:

```text
Docker Image
    ↓
Application
    ↓
Dependencies
    ↓
Runtime
```

The environment becomes much more consistent.

---

## What is a Docker Image?

A Docker image is a packaged, immutable template used to create containers.

In our project:

```text
docker-mastery:phase1
```

is the image.

---

## What is a Container?

A container is a running instance of a Docker image.

```text
Image
  |
  | docker run
  ↓
Container
```

One image can be used to create multiple containers.

---

## What is a Dockerfile?

A Dockerfile is a text file containing instructions used by Docker to build an image.

Our Dockerfile describes:

```text
Base OS
   ↓
Python installation
   ↓
Dependencies
   ↓
Application
   ↓
Port
   ↓
Startup command
```

---

## What is Docker Build Context?

When we run:

```powershell
docker build -t docker-mastery:phase1 .
```

the final:

```text
.
```

means the current directory is the build context.

Docker can access files from that context during instructions such as:

```dockerfile
COPY requirements.txt .
COPY app/ ./app/
```

The `.dockerignore` file controls which files are excluded from the context.

---

## Why `.dockerignore`?

It prevents unnecessary files from being sent to Docker during the build.

We excluded:

```text
venv
__pycache__
*.pyc
.git
```

This makes the build context smaller and prevents development-only files from being included unnecessarily.

---

## Why `EXPOSE 8000`?

```dockerfile
EXPOSE 8000
```

documents that the application listens on port 8000.

It does not publish the port to the host.

Port publishing is done with:

```powershell
docker run -p 8000:8000 ...
```

---

## Why `0.0.0.0`?

We start Uvicorn with:

```text
--host 0.0.0.0
```

so the application can accept connections through the container's network interface.

---

## What is `docker exec`?

`docker exec` allows us to execute a command inside a running container.

Example:

```powershell
docker exec -it phase1-app bash
```

This is useful for:

- Debugging
- Inspecting files
- Checking installed packages
- Investigating configuration
- Understanding the container environment

---

# Phase 1 → Phase 2

Phase 1 gives us the basic Docker workflow:

```text
FastAPI
   ↓
Dockerfile
   ↓
Docker Image
   ↓
Docker Container
```

However, there are several things we can improve.

### Problem 1 — Ubuntu is a general-purpose base image

We manually installed Python:

```dockerfile
apt-get install -y python3 python3-pip
```

Instead, we can use an image that already contains Python.

Phase 2 will use:

```dockerfile
FROM python:3.12-slim
```

---

### Problem 2 — No automated tests

Phase 1 only checks whether the application runs.

Phase 2 introduces:

```text
pytest
```

so we can automatically verify the API endpoints.

---

### Problem 3 — No linting

Phase 2 introduces:

```text
Flake8
```

to catch Python code-quality and style problems.

---

### Problem 4 — Build and runtime environments are mixed

Phase 2 introduces a:

```text
multi-stage Docker build
```

so dependencies can be prepared in a builder stage and only the required runtime contents are copied into the final image.

---

### Problem 5 — No CI

In Phase 1, everything is executed manually.

Phase 2 introduces:

```text
GitHub Actions
```

so every relevant push/pull request can automatically run:

```text
Lint
  ↓
Tests
  ↓
Docker Build
```

---

# Phase 1 → Phase 2 Summary

```text
PHASE 1

Ubuntu
  ↓
Install Python manually
  ↓
Install dependencies
  ↓
Copy application
  ↓
Build image
  ↓
Run container


PHASE 2

Python Slim
  ↓
Multi-stage build
  ↓
Runtime dependencies
  ↓
Tests
  ↓
Flake8
  ↓
GitHub
  ↓
GitHub Actions
  ↓
Lint + Test
  ↓
Docker Build
```

The purpose of Phase 2 is therefore not simply to "make another Docker image".

It is to take the basic containerized application from Phase 1 and start turning it into a **repeatable, testable CI workflow**.

---

# Phase 2

Phase 2 improves the basic Docker setup from Phase 1.

The major changes are:

- Use `python:3.12-slim`
- Use a multi-stage Docker build
- Separate runtime and development dependencies
- Add automated tests with pytest
- Add linting with Flake8
- Add `.dockerignore`
- Add Git/GitHub
- Add GitHub Actions CI
- Build the Docker image automatically in CI

---

## 1. Create the Phase-2 Directory

### Location

Inside `docker-project`:

```powershell
mkdir phase-2
mkdir phase-2\app
```

Copy the FastAPI application from Phase 1:

```powershell
Copy-Item phase-1\app\main.py phase-2\app\main.py
```

Create the requirements files:

```powershell
New-Item phase-2\requirements.txt -ItemType File
New-Item phase-2\requirements-dev.txt -ItemType File
```

---

## 2. Create `requirements.txt`

### File

```text
phase-2\requirements.txt
```

Contents:

```text
fastapi
uvicorn[standard]
```

These are the runtime dependencies required by the FastAPI application.

---

## 3. Create `requirements-dev.txt`

### File

```text
phase-2\requirements-dev.txt
```

Contents:

```text
-r requirements.txt
pytest
httpx
flake8
```

`requirements-dev.txt` contains the runtime dependencies plus development and testing dependencies.

---

## 4. Create the Python Virtual Environment

### Location

Inside `docker-project`:

```powershell
cd phase-2
```

Create the virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements-dev.txt
```

Verify pytest:

```powershell
pytest --version
```

Verify Flake8:

```powershell
flake8 --version
```

---

## 5. Create `test_main.py`

### Location

Inside:

```text
phase-2
```

Create:

```text
test_main.py
```

Contents:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Docker Mastery Project"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_info():
    response = client.get("/info")

    assert response.status_code == 200
```

---

## 6. Run the Tests

### Location

Inside `phase-2`:

```powershell
pytest -v
```

Expected result:

```text
3 passed
```

The tests verify:

- `GET /`
- `GET /health`
- `GET /info`

---

## 7. Run Flake8

Run:

```powershell
flake8 app test_main.py --max-line-length=100
```

If you get:

```text
app\main.py:30:6: W292 no newline at end of file
test_main.py:24:39: W292 no newline at end of file
```

Fix it by opening the affected file, going to the last character, pressing `Enter`, and saving the file.

Run Flake8 again:

```powershell
flake8 app test_main.py --max-line-length=100
```

Expected result:

```text
No output
```

Run the tests again:

```powershell
pytest -v
```

---

## 8. Create `.dockerignore`

### Location

Inside:

```text
phase-2
```

Create:

```text
.dockerignore
```

Contents:

```text
venv
__pycache__
*.pyc
.git
```

### Why?

The `venv` directory can contain thousands of files and potentially hundreds of MB.

We do not want Docker receiving the local virtual environment as part of the build context.

We also exclude:

- `__pycache__`
- compiled Python files
- Git metadata

This keeps the Docker build context smaller and cleaner.

---

## 9. Create the Phase-2 Dockerfile

### Location

Inside:

```text
phase-2
```

Create:

```text
Dockerfile
```

Contents:

```dockerfile
# =========================
# Stage 1: Builder
# =========================
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# =========================
# Stage 2: Final Image
# =========================
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 10. Build the Phase-2 Docker Image

### Location

Inside `phase-2`:

```powershell
docker build -t docker-mastery:phase2 .
```

Check the images:

```powershell
docker images
```

### Important Comparison

Phase 1 used Ubuntu and manually installed Python.

Phase 2 uses:

- `python:3.12-slim`
- Multi-stage Docker build

The Python base image already contains Python, so we no longer need to manually install Python inside an Ubuntu image.

---

## 11. Run the Phase-2 Container

Run:

```powershell
docker run -d --name phase2-app -p 8000:8000 docker-mastery:phase2
```

Check the running container:

```powershell
docker ps
```

Check logs:

```powershell
docker logs phase2-app
```

---

## 12. Inspect the Container

Enter the container:

```powershell
docker exec -it phase2-app bash
```

Inside the container:

```bash
ls
```

Then:

```bash
ls app
```

You should see the application.

You should not see:

```text
venv
test_main.py
requirements-dev.txt
.git
```

The final Docker image only needs the application and runtime dependencies.

Exit:

```bash
exit
```

---

# Phase 2 — Git and GitHub

## 13. Go Back to the Project Root

After exiting the container:

### Current location

```text
docker-project\phase-2
```

Go back to the project root:

```powershell
cd ..
```

You should now be inside:

```text
docker-project
```

---

## 14. Check Git Status

Run:

```powershell
git status
```

If the Phase-2 files have not been added to Git yet, they may appear as untracked files.

---

## 15. Add the Project Files

From `docker-project`:

```powershell
git add .
```

Check:

```powershell
git status
```

---

## 16. Commit the Project

Run:

```powershell
git commit -m "Add Docker Phase 1 and Phase 2"
```

If Git shows:

```text
Author identity unknown
```

Configure your identity:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Then commit again:

```powershell
git commit -m "Add Docker Phase 1 and Phase 2"
```

---

## 17. Create / Connect the GitHub Repository

Create a GitHub repository named:

```text
containerized-fastapi-cicd
```

Add the remote:

```powershell
git remote add origin https://github.com/<YOUR_USERNAME>/containerized-fastapi-cicd.git
```

Check:

```powershell
git remote -v
```

> Replace `<YOUR_USERNAME>` with your own GitHub username.

---

## 18. Push to GitHub

The project uses the `main` branch.

If your local branch is already named `main`:

```powershell
git push -u origin main
```

If Git asks for authentication, complete the authentication in the browser.

GitHub does not accept a normal account password for Git HTTPS authentication.

---

## 19. If Push Is Rejected with `fetch first`

If the remote repository already contains an initial commit, Git may reject the push.

Run:

```powershell
git pull origin main --allow-unrelated-histories
```

Then:

```powershell
git log --oneline --graph --all --decorate
```

Check:

```powershell
git status
```

Then push again:

```powershell
git push -u origin main
```

---

## 20. Final Git Check

Run:

```powershell
git status
```

Expected:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

# Phase 2 — GitHub Actions CI

GitHub Actions is used to automatically run linting, tests, and a Docker build.

---

## 21. Create the GitHub Actions Folder

GitHub Actions workflow files are stored in:

```text
docker-project\.github\workflows\
```

From `docker-project`:

```powershell
mkdir .github
mkdir .github\workflows
```

---

## 22. Move the Phase-2 CI Workflow

If the workflow was initially created inside:

```text
phase-2\.github\workflows\ci.yml
```

move it to:

```text
docker-project\.github\workflows\ci.yml
```

Run from `docker-project`:

```powershell
Move-Item phase-2\.github\workflows\ci.yml .github\workflows\ci.yml
```

Check:

```powershell
git status
```

Git may recognize this as a rename:

```text
phase-2/.github/workflows/ci.yml
        ->
.github/workflows/ci.yml
```

Stage it:

```powershell
git add .
```

---

## 23. Create / Verify `ci.yml`

### Location

```text
docker-project\.github\workflows\ci.yml
```

Contents:

```yaml
name: Phase 2 CI

on:
  push:
    branches:
      - main
    paths:
      - "phase-2/**"

  pull_request:
    branches:
      - main
    paths:
      - "phase-2/**"

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r phase-2/requirements-dev.txt

      - name: Run Flake8
        run: |
          flake8 phase-2/app phase-2/test_main.py --max-line-length=100

      - name: Run tests
        run: |
          pytest -v phase-2/test_main.py

  build-image:
    runs-on: ubuntu-latest
    needs: lint-and-test

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v6
        with:
          context: ./phase-2
          file: ./phase-2/Dockerfile
          push: false
          tags: docker-mastery:phase2
```

You can verify the file from PowerShell:

```powershell
Get-Content .github\workflows\ci.yml
```

---

## 24. Understand the Phase-2 CI Flow

```text
git push
    |
    v
GitHub Actions
    |
    v
lint-and-test
    |
    +--> Checkout code
    +--> Install Python 3.12
    +--> Install dependencies
    +--> Run Flake8
    +--> Run pytest
    |
    | SUCCESS
    v
build-image
    |
    +--> Setup Docker Buildx
    +--> Build Docker image
    |
    v
PASS
```

The `build-image` job contains:

```yaml
needs: lint-and-test
```

Therefore, the Docker image is built only if linting and testing succeed.

---

## 25. Understand `push: false`

The Docker build step contains:

```yaml
push: false
```

This means GitHub Actions builds the Docker image but does not push it to Docker Hub or another container registry.

At this stage, CI only verifies that the Docker image can be built successfully.

---

## 26. Commit the CI Workflow

Run:

```powershell
git add .
git commit -m "Add Phase 2 CI workflow"
git push
```

---

## 27. Check GitHub Actions

Open the GitHub repository and go to:

```text
Actions
```

You should see:

```text
Phase 2 CI
```

A successful workflow will show a green check mark.

---

# Phase 2 — Interview Notes

## What did we do in Phase 2?

Phase 2 improved the basic Docker setup from Phase 1.

We moved from a manually configured Ubuntu container to a Python Slim base image and introduced a multi-stage Docker build.

We also added:

- Automated tests
- Flake8 linting
- Git
- GitHub
- GitHub Actions CI
- Docker image building in CI

---

## Why `python:3.12-slim`?

Instead of starting with a general Ubuntu image and manually installing Python, we use an official Python image that already contains Python.

The Slim variant is smaller than the full Python image and contains fewer unnecessary packages.

---

## What is a Multi-Stage Build?

There are two stages.

### Stage 1 — Builder

```dockerfile
FROM python:3.12-slim AS builder
```

This stage installs the Python dependencies.

### Stage 2 — Final Image

```dockerfile
FROM python:3.12-slim
```

This is the final runtime image.

Only the installed dependencies are copied:

```dockerfile
COPY --from=builder /install /usr/local
```

And the application is copied:

```dockerfile
COPY app/ ./app/
```

### Why?

The build environment may contain tools and files that are not required to run the application.

Using separate builder and final stages keeps the final image cleaner and smaller.

---

## Why `requirements.txt` and `requirements-dev.txt`?

### `requirements.txt`

Contains runtime dependencies:

```text
fastapi
uvicorn[standard]
```

### `requirements-dev.txt`

Contains runtime dependencies plus development/testing tools:

```text
-r requirements.txt
pytest
httpx
flake8
```

This separation prevents development-only packages from being required in the production Docker image.

---

## Why `.dockerignore`?

`.dockerignore` prevents unnecessary files from being sent as part of the Docker build context.

We exclude:

```text
venv
__pycache__
*.pyc
.git
```

This keeps the build context smaller and prevents development-only files from entering the Docker build context.

---

## What is pytest?

`pytest` is a Python testing framework.

Our tests verify:

```text
GET /
GET /health
GET /info
```

---

## What is Flake8?

Flake8 is a Python linting tool.

It checks Python code for common style and formatting problems.

Example:

```text
W292 no newline at end of file
```

This was fixed by adding a newline at the end of the affected files.

---

## What is GitHub Actions?

GitHub Actions is a CI/CD platform integrated into GitHub.

Our workflow automatically:

1. Checks out the repository.
2. Installs Python.
3. Installs dependencies.
4. Runs Flake8.
5. Runs pytest.
6. Builds the Docker image.

---

## Why Run Tests Before Building the Image?

We do not want to build and potentially deploy an application whose tests or code-quality checks have already failed.

The:

```yaml
needs: lint-and-test
```

dependency makes the Docker build wait for linting and testing.

---

# Phase 3

Phase 3 makes the container more production-oriented and secure.

### Main changes

1. Alpine base image
2. Multi-stage Docker build
3. Non-root user
4. Docker `HEALTHCHECK`
5. GitHub Actions CI
6. Docker Buildx in CI

---

## 1. Check Git Status

### Location

```text
docker-project
```

Run:

```powershell
git status
```

Expected:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

## 2. Create Phase-3 Directory

### Location

```text
docker-project
```

Run:

```powershell
mkdir phase-3
mkdir phase-3\app
```

Copy the Phase-2 application:

```powershell
Copy-Item phase-2\app\main.py phase-3\app\main.py
```

Create the requirements files:

```powershell
New-Item phase-3\requirements.txt -ItemType File
New-Item phase-3\requirements-dev.txt -ItemType File
```

---

## 3. Create Phase-3 Requirements

### `phase-3\requirements.txt`

```text
fastapi
uvicorn[standard]
```

### `phase-3\requirements-dev.txt`

```text
-r requirements.txt
pytest
httpx
flake8
```

---

## 4. Create the Phase-3 Virtual Environment

### Location

```text
docker-project
```

Go to Phase 3:

```powershell
cd phase-3
```

Create the virtual environment:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements-dev.txt
```

Verify:

```powershell
pytest --version
flake8 --version
```

---

## 5. Create Phase-3 `test_main.py`

### Location

```text
phase-3
```

Create:

```text
test_main.py
```

Contents:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Docker Mastery Project"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_info():
    response = client.get("/info")

    assert response.status_code == 200
```

---

## 6. Run Phase-3 Tests

### Location

```text
phase-3
```

Run:

```powershell
pytest -v
```

Expected:

```text
3 passed
```

---

## 7. Run Flake8

Run:

```powershell
flake8 app test_main.py --max-line-length=100
```

If you get:

```text
W292 no newline at end of file
```

Go to the end of the affected file, press `Enter`, and save.

Run again:

```powershell
flake8 app test_main.py --max-line-length=100
```

Expected:

```text
No output
```

---

## 8. Create Phase-3 `.dockerignore`

### Location

```text
phase-3
```

Create:

```text
.dockerignore
```

Contents:

```text
venv
__pycache__
*.pyc
.git
```

The same principle as Phase 2 applies.

Do not send:

- Local virtual environments
- Python cache files
- Compiled Python files
- Git metadata

as Docker build context.

---

## 9. Create Phase-3 Dockerfile

### Location

```text
phase-3
```

Create:

```text
Dockerfile
```

Contents:

```dockerfile
# =========================
# Stage 1: Builder
# =========================
FROM python:3.12-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# =========================
# Stage 2: Final Image
# =========================
FROM python:3.12-alpine

WORKDIR /app

# Copy only installed Python packages
COPY --from=builder /install /usr/local

# Create non-root user
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

COPY app/ ./app/

# Run application as non-root user
USER appuser

EXPOSE 8000

# Container health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 10. Build the Phase-3 Image

### Location

```text
phase-3
```

Run:

```powershell
docker build -t docker-mastery:phase3 .
```

Check:

```powershell
docker images
```

### Important Comparison

| Feature | Phase 2 | Phase 3 |
|---|---|---|
| Base image | `python:3.12-slim` | `python:3.12-alpine` |
| Multi-stage build | Yes | Yes |
| Non-root user | No | Yes |
| HEALTHCHECK | No | Yes |
| Container hardening | Basic | Improved |

Phase 3 focuses on container hardening.

---

## 11. Run the Phase-3 Container

Run:

```powershell
docker run -d --name phase3-app -p 8000:8000 docker-mastery:phase3
```

Check:

```powershell
docker ps
```

Check logs:

```powershell
docker logs phase3-app
```

The container should eventually show:

```text
Up ... (healthy)
```

---

## 12. Understand `HEALTHCHECK`

The Dockerfile contains:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8000/health || exit 1
```

Docker periodically checks:

```text
http://127.0.0.1:8000/health
```

If the check succeeds:

```text
healthy
```

If repeated checks fail:

```text
unhealthy
```

---

## 13. Enter the Phase-3 Container

Alpine normally uses `sh` instead of `bash`.

Run:

```powershell
docker exec -it phase3-app sh
```

Inside:

```sh
ls
```

Then:

```sh
ls app
```

`main.py` should be present.

The following should not be present:

```text
venv
test_main.py
requirements-dev.txt
.git
```

Exit:

```sh
exit
```

---

## 14. Verify the Non-Root User

Run:

```powershell
docker exec -it phase3-app sh
```

Inside the container:

```sh
whoami
```

Expected:

```text
appuser
```

Also run:

```sh
id
```

This displays the user and group information.

Exit:

```sh
exit
```

---

## 15. Why Use a Non-Root User?

Containers can run processes as root by default.

Running the application as a dedicated non-root user reduces unnecessary privileges.

Phase 3 creates:

```text
appgroup
appuser
```

and then uses:

```dockerfile
USER appuser
```

### Interview Answer

> I hardened the container by creating a dedicated non-root user and running the application under that user instead of root.

---

## 16. Test Phase-3 Endpoints

From the Windows host:

```powershell
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/info
```

You can also open these in a browser:

```text
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/info
http://localhost:8000/docs
```

Then check:

```powershell
docker ps
```

The container should show:

```text
healthy
```

---

## 17. Stop the Phase-3 Container

When testing is complete:

```powershell
docker stop phase3-app
```

Check:

```powershell
docker ps
```

The stopped container still exists:

```powershell
docker ps -a
```

Start it again:

```powershell
docker start phase3-app
```

Remove it when no longer needed:

```powershell
docker rm phase3-app
```

---

# Phase 3 — GitHub Actions

## 18. Create the Workflow Folder

### Location

```text
docker-project
```

If the folders do not already exist:

```powershell
mkdir .github
mkdir .github\workflows
```

---

## 19. Create `phase3-ci.yml`

### Location

```text
docker-project\.github\workflows
```

Create:

```text
phase3-ci.yml
```

---

## 20. Phase-3 CI File

Contents:

```yaml
name: Phase 3 CI

on:
  push:
    branches:
      - main
    paths:
      - "phase-3/**"
      - ".github/workflows/phase3-ci.yml"

  pull_request:
    branches:
      - main
    paths:
      - "phase-3/**"
      - ".github/workflows/phase3-ci.yml"

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r phase-3/requirements-dev.txt

      - name: Run Flake8
        run: |
          flake8 phase-3/app phase-3/test_main.py --max-line-length=100

      - name: Run tests
        run: |
          pytest -v phase-3/test_main.py

  build-image:
    runs-on: ubuntu-latest
    needs: lint-and-test

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v6
        with:
          context: ./phase-3
          file: ./phase-3/Dockerfile
          push: false
          tags: docker-mastery:phase3
```

---

## 21. Understand Phase-3 CI

```text
git push
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    v
lint-and-test
    |
    +--> Checkout
    +--> Python 3.12
    +--> Install dependencies
    +--> Flake8
    +--> pytest
    |
    | SUCCESS
    v
build-image
    |
    +--> Docker Buildx
    +--> Docker build
    |
    v
PASS
```

The important dependency is:

```yaml
needs: lint-and-test
```

Therefore, `build-image` waits for `lint-and-test`.

If Flake8 or pytest fails, `build-image` does not run.

---

## 22. Understand Path Filters

The workflow contains:

```yaml
paths:
  - "phase-3/**"
  - ".github/workflows/phase3-ci.yml"
```

This means the workflow runs when:

1. Files inside `phase-3` change.
2. The Phase-3 workflow itself changes.

A change only inside Phase 1 or Phase 2 does not trigger this Phase-3 workflow.

---

## 23. Stage Phase-3

### Location

```text
docker-project
```

Check:

```powershell
git status
```

Stage:

```powershell
git add .
```

Check again:

```powershell
git status
```

---

## 24. Commit Phase-3

Run:

```powershell
git commit -m "Add Phase 3 Docker hardening and CI"
```

---

## 25. Push Phase-3

Run:

```powershell
git push
```

---

## 26. Check GitHub Actions

Open the GitHub repository.

Go to:

```text
Actions
```

Find:

```text
Phase 3 CI
```

The workflow should run automatically.

A successful workflow shows a green check mark.

---

## 27. Phase-3 CI Formatting Issue

If Flake8 reports:

```text
W292 no newline at end of file
```

Open:

```text
phase-3\test_main.py
```

Go to the final character.

Press `Enter`.

Save.

Verify locally:

```powershell
flake8 app test_main.py --max-line-length=100
```

Then:

```powershell
pytest -v
```

Expected:

```text
3 passed
```

---

## 28. Commit the Fix

Run:

```powershell
git add phase-3/test_main.py
git commit -m "Fix Phase 3 test file formatting"
git push
```

GitHub Actions will run again.

---

## 29. Successful Phase-3 CI

Final flow:

```text
git push
    |
    v
GitHub Actions
    |
    +--> lint-and-test
    |       |
    |       +--> Flake8    PASS
    |       +--> Pytest    PASS
    |
    v
build-image
    |
    +--> Docker Buildx
    +--> Docker image build
    |
    v
GREEN CHECK
```

---

# Phase 3 — Interview Cheat Sheet

## What did you improve in Phase 3?

### Interview Answer

> I hardened the Docker container and made it more production-oriented. I moved from `python:3.12-slim` to `python:3.12-alpine`, kept the multi-stage build so the final image contains only runtime requirements, created a dedicated non-root `appuser`, and added a Docker `HEALTHCHECK` that calls the FastAPI `/health` endpoint. I also created a separate GitHub Actions workflow for Phase 3 that runs Flake8 and pytest before building the Docker image. The `build-image` job depends on `lint-and-test`, so a failed quality check prevents the Docker image from being built.

---

## Important Terms

### Alpine

A lightweight Linux distribution commonly used for containers.

### Multi-stage Build

Uses separate build and final stages so build-only dependencies do not need to remain in the final runtime image.

### Non-root Container

Runs the application with reduced privileges.

### HEALTHCHECK

Provides Docker with a mechanism to determine whether the application is healthy.

### Build Context

The directory whose files are available to Docker during a build.

For Phase 3:

```yaml
context: ./phase-3
```

### Buildx

Docker's modern build system used by Docker build actions.

### CI

Continuous Integration. Code is automatically checked when changes are pushed.

### Flake8

Python linting tool.

### pytest

Python testing framework.

### `needs`

A GitHub Actions keyword used to make one job depend on another job.

---

# Running the Project Again After Shutdown

## 1. Start Docker Desktop

Start Docker Desktop before running Docker commands.

---

## 2. Open the Project

Open:

```text
docker-project
```

in VS Code.

---

## 3. Check Git

From `docker-project`:

```powershell
git status
```

---

## 4. Start Phase-3 Container If It Already Exists

Check:

```powershell
docker ps -a
```

If `phase3-app` exists but is stopped:

```powershell
docker start phase3-app
```

Check:

```powershell
docker ps
```

---

## 5. If `phase3-app` Does Not Exist

Go to:

```text
phase-3
```

Build:

```powershell
docker build -t docker-mastery:phase3 .
```

Run:

```powershell
docker run -d --name phase3-app -p 8000:8000 docker-mastery:phase3
```

---

## 6. Check the Container

Run:

```powershell
docker ps
```

Check logs:

```powershell
docker logs phase3-app
```

The container should eventually become:

```text
healthy
```

---

## 7. Python Development

Go to:

```text
phase-3
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If the virtual environment does not exist:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

---

## 8. When Finished for the Day

Stop the container:

```powershell
docker stop phase3-app
```

You can shut down the laptop after the container has been stopped.

---

# Final Phase Comparison

| Feature | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|
| Base image | Ubuntu | `python:3.12-slim` | `python:3.12-alpine` |
| Python | Installed manually | Included in base image | Included in base image |
| Multi-stage build | No | Yes | Yes |
| Automated tests | No | pytest | pytest |
| Linting | No | Flake8 | Flake8 |
| `.dockerignore` | Basic | Yes | Yes |
| Non-root user | No | No | Yes |
| HEALTHCHECK | No | No | Yes |
| Git/GitHub | No | Yes | Yes |
| GitHub Actions | No | Yes | Yes |
| Docker Buildx in CI | No | Yes | Yes |
| Container hardening | Basic | Improved | Further improved |

---

# Project Evolution

## Phase 1

```text
FastAPI application
        |
        v
Docker image
        |
        v
Container
```

## Phase 2

```text
FastAPI application
        |
        v
Tests + Linting
        |
        v
Multi-stage Docker image
        |
        v
GitHub Actions CI
```

## Phase 3

```text
FastAPI application
        |
        v
Tests + Linting
        |
        v
Hardened Docker image
        |
        +--> Alpine
        +--> Multi-stage build
        +--> Non-root user
        +--> HEALTHCHECK
        |
        v
GitHub Actions CI
        |
        v
Docker Build
```

---

# Current Status

- Phase 1: Complete
- Phase 2: Complete
- Phase 3: Complete
- Phase 2 CI: Complete
- Phase 3 CI: Green

---

# What Comes Next?

The next phase should build on the existing Docker and CI foundation rather than repeating the same concepts.

Possible next topics include:

- Docker image tagging strategy
- Container registry
- Docker Hub / GitHub Container Registry
- CI/CD separation
- Image publishing
- Environment variables
- Docker Compose
- Application configuration
- Deployment
- AWS
- Kubernetes
- Infrastructure as Code
- Monitoring and logging
- Production-grade CI/CD

The project can progressively evolve from:

```text
Application
    ↓
Docker
    ↓
Testing + Linting
    ↓
CI
    ↓
Container Hardening
    ↓
Container Registry
    ↓
CD
    ↓
Cloud Deployment
    ↓
Kubernetes
```

---

# License

This project is intended for learning and portfolio purposes.
