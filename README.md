# Containerized FastAPI CI/CD — Docker → GitHub Actions → Docker Hub → AWS EC2

A hands-on DevOps project that starts with a simple FastAPI application and progressively evolves into a containerized, tested, linted, CI/CD-enabled application deployed to AWS EC2.

The project is intentionally built phase by phase so that every change has a practical reason and an interview-relevant concept behind it.

---

# Project Roadmap

```text
Prerequisites
      ↓
Phase 1
Basic FastAPI + Docker
      ↓
Phase 2
Testing + Flake8 + Multi-stage Docker + GitHub Actions CI
      ↓
Phase 3
Alpine + Non-root User + HEALTHCHECK + CI
      ↓
Phase 4
GitHub Actions → Docker Hub
      ↓
Phase 5
Docker Hub → AWS EC2
      ↓
Phase 6
AWS ECR + ECS
      ↓
Phase 7
Kubernetes
      ↓
Phase 8
Terraform
```

## Final architecture so far

```text
Developer
    |
    | git push
    v
GitHub
    |
    v
GitHub Actions
    |
    +--> Flake8
    +--> pytest
    +--> Docker Build
    |
    v
Docker Hub
    |
    | docker pull
    v
AWS EC2
    |
    v
Docker Container
    |
    v
FastAPI
    |
    v
Internet
```

---

# Prerequisites

Before starting the project, install and configure:

- Visual Studio Code
- Git
- Python 3.12
- pip
- Docker Desktop
- GitHub account
- Docker Hub account
- AWS account for Phase 5 onward

## 1. Visual Studio Code

Install VS Code.

We use it to:

- Write the FastAPI application
- Create Dockerfiles
- Create GitHub Actions workflows
- Run PowerShell commands
- Inspect the project

Open:

```text
VS Code → Terminal → New Terminal
```

## 2. Git

Verify:

```powershell
git --version
```

Configure Git:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Verify:

```powershell
git config --global --list
```

## 3. Python

Install Python 3.12.

Verify:

```powershell
python --version
pip --version
```

If `python` is not recognized:

```powershell
py --version
```

## 4. Docker Desktop

Install Docker Desktop for Windows.

Start Docker Desktop and wait until Docker Engine is running.

Verify:

```powershell
docker --version
docker info
```

Test:

```powershell
docker run hello-world
```

For Windows, Docker Desktop commonly uses the WSL 2 backend.

Check:

```text
Docker Desktop
→ Settings
→ General
```

Enable the WSL 2 based engine if available.

You do not need to manually use WSL for this project. The project can be completed from the VS Code PowerShell terminal with Docker Desktop.

## 5. GitHub

Create/sign in to GitHub.

The repository used for this project is:

```text
containerized-fastapi-cicd
```

## 6. Final environment check

```powershell
git --version
python --version
pip --version
docker --version
docker info
docker run hello-world
```

---

# Phase 1 — Basic Dockerization

## Goal

Build a basic FastAPI application and run it inside Docker.

```text
FastAPI
   ↓
Python dependencies
   ↓
Dockerfile
   ↓
Docker image
   ↓
Docker container
   ↓
localhost:8000
```

At this stage we intentionally use Ubuntu as the base image and install Python manually.

---

## 1. Create the project

```powershell
mkdir docker-project
cd docker-project
code .
```

Create:

```powershell
mkdir phase-1
mkdir phase-1\app
```

Structure:

```text
docker-project/
└── phase-1/
    └── app/
```

---

## 2. Create FastAPI application

Create:

```text
phase-1\app\main.py
```

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

We have three endpoints:

```text
GET /
GET /health
GET /info
```

The `/health` endpoint will later be used by Docker's `HEALTHCHECK`.

---

## 3. Create requirements.txt

Create:

```text
phase-1\requirements.txt
```

Contents:

```text
fastapi
uvicorn[standard]
```

---

## 4. Create virtual environment

```powershell
cd phase-1
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The virtual environment is only for local development.

Docker will have its own Python environment.

---

## 5. Test FastAPI locally

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/health
http://127.0.0.1:8000/info
http://127.0.0.1:8000/docs
```

Stop:

```text
CTRL + C
```

Important troubleshooting rule:

```text
Doesn't work locally
    ↓
Fix application

Works locally but not in Docker
    ↓
Investigate Docker configuration
```

---

## 6. Create .dockerignore

Create:

```text
phase-1\.dockerignore
```

```text
venv
__pycache__
*.pyc
.git
```

This prevents unnecessary files from becoming part of the Docker build context.

---

## 7. Create Dockerfile

Create:

```text
phase-1\Dockerfile
```

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

### What is happening?

```text
FROM
 ↓
Choose base image

WORKDIR
 ↓
Set /app

RUN
 ↓
Install Python and dependencies

COPY
 ↓
Copy application

EXPOSE
 ↓
Document application port

CMD
 ↓
Start Uvicorn
```

`EXPOSE 8000` documents the port; it does not publish it.

---

## 8. Build image

Inside `phase-1`:

```powershell
docker build -t docker-mastery:phase1 .
```

Check:

```powershell
docker images
```

---

## 9. Run container

```powershell
docker run -d --name phase1-app -p 8000:8000 docker-mastery:phase1
```

Check:

```powershell
docker ps
```

Expected port mapping:

```text
0.0.0.0:8000->8000/tcp
```

Check logs:

```powershell
docker logs phase1-app
```

Test:

```text
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/info
http://localhost:8000/docs
```

---

## 10. Inspect container

```powershell
docker exec -it phase1-app bash
```

Inside:

```bash
ls
ls app
```

Exit:

```bash
exit
```

---

## Phase 1 interview concepts

Know:

- Docker image vs container
- Dockerfile
- Docker build context
- `.dockerignore`
- `WORKDIR`
- `COPY`
- `RUN`
- `EXPOSE`
- `CMD`
- Port mapping
- Why `0.0.0.0` is used inside a container
- Why containers improve environment consistency

---

# Phase 2 — Testing + Linting + Multi-stage Docker + GitHub Actions

Phase 2 improves the basic setup.

We introduce:

- pytest
- httpx
- Flake8
- `requirements-dev.txt`
- Python Slim image
- Multi-stage Docker build
- Git
- GitHub
- GitHub Actions CI

---

## 1. Create Phase 2

From `docker-project`:

```powershell
mkdir phase-2
mkdir phase-2\app
Copy-Item phase-1\app\main.py phase-2\app\main.py
New-Item phase-2\requirements.txt -ItemType File
New-Item phase-2\requirements-dev.txt -ItemType File
```

## 2. requirements.txt

```text
fastapi
uvicorn[standard]
```

## 3. requirements-dev.txt

```text
-r requirements.txt
pytest
httpx
flake8
```

Runtime dependencies belong in `requirements.txt`.

Development/testing tools belong in `requirements-dev.txt`.

---

## 4. Create virtual environment

```powershell
cd phase-2
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest --version
flake8 --version
```

---

## 5. Create test_main.py

Create:

```text
phase-2\test_main.py
```

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

Run:

```powershell
pytest -v
```

Expected:

```text
3 passed
```

---

## 6. Flake8

Run:

```powershell
flake8 app test_main.py --max-line-length=100
```

If you see:

```text
W292 no newline at end of file
```

Open the affected file, go to the last character, press Enter, save, and run Flake8 again.

Expected:

```text
No output
```

---

## 7. Create .dockerignore

```text
venv
__pycache__
*.pyc
.git
```

---

## 8. Multi-stage Dockerfile

Create `phase-2\Dockerfile`:

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

### Why multi-stage?

The builder stage installs dependencies.

The final stage receives only what is required at runtime.

```text
Builder
  ↓
Install dependencies
  ↓
Final image
  ↓
Runtime dependencies + application
```

Development tools such as pytest and Flake8 are not copied into the runtime image.

---

## 9. Build and run Phase 2

```powershell
docker build -t docker-mastery:phase2 .
docker images
docker run -d --name phase2-app -p 8000:8000 docker-mastery:phase2
docker ps
docker logs phase2-app
```

Inspect:

```powershell
docker exec -it phase2-app bash
```

Inside:

```bash
ls
ls app
```

You should not see:

```text
venv
test_main.py
requirements-dev.txt
.git
```

Exit:

```bash
exit
```

---

# Git setup

From `docker-project`:

```powershell
cd ..
git status
git add .
git commit -m "Add Docker Phase 1 and Phase 2"
```

Create/connect the GitHub repository:

```powershell
git remote add origin https://github.com/<YOUR_USERNAME>/containerized-fastapi-cicd.git
git remote -v
```

Push:

```powershell
git push -u origin main
```

If the remote already has a separate initial commit and push is rejected:

```powershell
git pull origin main --allow-unrelated-histories
git log --oneline --graph --all --decorate
git status
git push -u origin main
```

Final check:

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

Create:

```text
docker-project\.github\workflows\ci.yml
```

If needed:

```powershell
mkdir .github
mkdir .github\workflows
```

Workflow:

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

Verify:

```powershell
Get-Content .github\workflows\ci.yml
```

Commit:

```powershell
git add .
git commit -m "Add Phase 2 CI workflow"
git push
```

Go to GitHub → Actions.

A successful workflow should show a green check.

### Why `needs: lint-and-test`?

It means:

```text
lint-and-test
      |
      | SUCCESS
      ↓
build-image
```

If linting or tests fail, the Docker build does not run.

---

## Phase 2 interview concepts

Know:

- pytest
- Flake8
- CI
- GitHub Actions
- GitHub Actions runner
- `needs`
- multi-stage builds
- build context
- `requirements.txt` vs `requirements-dev.txt`
- why tests should run before building/deploying

---

# Phase 3 — Container Hardening

Phase 3 makes the container more production-oriented.

Main changes:

1. `python:3.12-alpine`
2. Multi-stage build
3. Non-root `appuser`
4. Docker `HEALTHCHECK`
5. Separate Phase 3 CI workflow
6. Docker Buildx

---

## 1. Check Git

From `docker-project`:

```powershell
git status
```

Start Phase 3 with a clean repository.

---

## 2. Create Phase 3

```powershell
mkdir phase-3
mkdir phase-3\app
Copy-Item phase-2\app\main.py phase-3\app\main.py
New-Item phase-3\requirements.txt -ItemType File
New-Item phase-3\requirements-dev.txt -ItemType File
```

## 3. Requirements

`phase-3\requirements.txt`:

```text
fastapi
uvicorn[standard]
```

`phase-3\requirements-dev.txt`:

```text
-r requirements.txt
pytest
httpx
flake8
```

---

## 4. Virtual environment

```powershell
cd phase-3
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest --version
flake8 --version
```

---

## 5. Tests

Create `phase-3\test_main.py`:

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

Run:

```powershell
pytest -v
```

Expected:

```text
3 passed
```

Run Flake8:

```powershell
flake8 app test_main.py --max-line-length=100
```

Fix `W292` by adding a newline at the end of the affected file if necessary.

---

## 6. .dockerignore

```text
venv
__pycache__
*.pyc
.git
```

---

## 7. Phase 3 Dockerfile

Create `phase-3\Dockerfile`:

```dockerfile
# =========================
# Stage 1: Builder
# =========================
FROM python:3.12-alpine AS builder

WORKDIR /app

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

COPY --from=builder /install /usr/local

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

COPY app/ ./app/

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Why Alpine?

Alpine is a lightweight Linux distribution commonly used for containers.

### Why non-root?

Running the application as `appuser` reduces privileges.

### Why HEALTHCHECK?

Docker can use the health check to determine whether the application is healthy.

The check calls:

```text
http://127.0.0.1:8000/health
```

---

## 8. Build Phase 3

Inside `phase-3`:

```powershell
docker build -t docker-mastery:phase3 .
```

Run:

```powershell
docker run -d --name phase3-app -p 8000:8000 docker-mastery:phase3
```

Check:

```powershell
docker ps
docker logs phase3-app
```

Eventually the container should show:

```text
Up ... (healthy)
```

Verify the application:

```text
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/info
http://localhost:8000/docs
```

---

# Phase 3 CI

Create:

```text
.github\workflows\phase3-ci.yml
```

The workflow should:

```text
git push
    ↓
GitHub Actions
    ↓
lint-and-test
    ├── Flake8
    └── pytest
    ↓
build-image
    └── Docker Buildx
```

Important:

```yaml
needs: lint-and-test
```

Path filter:

```yaml
paths:
  - "phase-3/**"
  - ".github/workflows/phase3-ci.yml"
```

Commit:

```powershell
cd ..
git add .
git commit -m "Add Phase 3 Docker hardening and CI"
git push
```

Check:

```text
GitHub → Actions → Phase 3 CI
```

A successful workflow shows a green check.

---

# Phase 3 interview cheat sheet

### What changed?

> I hardened the container by moving to Alpine, keeping a multi-stage build, running the application as a non-root user, and adding a Docker HEALTHCHECK. I also added CI that runs Flake8 and pytest before building the Docker image.

Important terms:

- Alpine
- Multi-stage build
- Non-root user
- HEALTHCHECK
- Build context
- Buildx
- CI
- `needs`

---

# Phase 4 — GitHub Actions → Docker Hub

Phase 4 takes the image built in CI and publishes it to Docker Hub.

Before Phase 4:

```text
git push
    ↓
GitHub Actions
    ↓
Flake8
    ↓
pytest
    ↓
Docker build
    ↓
PASS
```

Phase 4:

```text
git push
    ↓
GitHub Actions
    ↓
Flake8
    ↓
pytest
    ↓
Docker build
    ↓
Docker Hub login
    ↓
Docker push
    ↓
Docker Hub
```

The important change is:

```yaml
push: false
```

becomes:

```yaml
push: true
```

---

## 1. Create Docker Hub repository

Create a public Docker Hub repository:

```text
containerized-fastapi-cicd
```

Image format:

```text
YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

Docker Hub is a container registry.

It stores images so other machines can later pull and run them.

---

## 2. Create Docker Hub access token

Do not put your Docker Hub password in the workflow.

Create a Docker Hub access token with permission to push images.

Keep the token private.

Never put it in:

- source code
- README
- workflow file
- Git commit

---

## 3. Add GitHub Secrets

Go to:

```text
GitHub Repository
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Create:

```text
DOCKERHUB_USERNAME
```

Value:

```text
Your Docker Hub username
```

Create:

```text
DOCKERHUB_TOKEN
```

Value:

```text
Your Docker Hub access token
```

The workflow uses:

```yaml
${{ secrets.DOCKERHUB_USERNAME }}
${{ secrets.DOCKERHUB_TOKEN }}
```

The actual token is never stored in source code.

---

## 4. Check repository

From:

```text
docker-project
```

run:

```powershell
git status
```

---

## 5. Phase 4 workflow

Create:

```text
.github\workflows\phase4-ci-cd.yml
```

Example:

```yaml
name: Phase 4 - CI/CD to Docker Hub

on:
  push:
    branches:
      - main
    paths:
      - "phase-3/**"
      - ".github/workflows/phase4-ci-cd.yml"

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

  build-and-push:
    runs-on: ubuntu-latest
    needs: lint-and-test

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: ./phase-3
          file: ./phase-3/Dockerfile
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/containerized-fastapi-cicd:latest
```

---

## 6. Understand the workflow

There are two jobs:

```text
lint-and-test
      |
      | SUCCESS
      ↓
build-and-push
```

The dependency:

```yaml
needs: lint-and-test
```

prevents an image from being published when tests/linting fail.

### `actions/checkout`

Copies repository code onto the GitHub Actions runner.

### `setup-python`

Installs Python 3.12 on the runner.

### `docker/login-action`

Authenticates the runner with Docker Hub.

### `docker/setup-buildx-action`

Sets up Docker Buildx.

### `docker/build-push-action`

Builds and pushes the image.

---

## 7. Understand `context`

```yaml
context: ./phase-3
file: ./phase-3/Dockerfile
```

This means:

```text
phase-3/
├── Dockerfile
├── app/
└── requirements.txt
```

is used as the Docker build context.

This is equivalent to locally doing:

```powershell
cd phase-3
docker build -t docker-mastery:phase3 .
```

---

## 8. Understand `push: true`

Phase 3:

```yaml
push: false
```

```text
Docker build
    ↓
Image exists only on CI runner
```

Phase 4:

```yaml
push: true
```

```text
Docker build
    ↓
Docker image
    ↓
Docker Hub
```

---

## 9. Understand image tag

```text
USERNAME/REPOSITORY:TAG
```

Example:

```text
swayam248/containerized-fastapi-cicd:latest
```

Here:

```text
swayam248
    ↓
Docker Hub username

containerized-fastapi-cicd
    ↓
Repository

latest
    ↓
Image tag
```

`latest` is intentionally used for learning.

Later, better strategies include:

- semantic version tags
- Git commit SHA
- release tags

---

## 10. Check and push

```powershell
git status
Get-Content .github\workflows\phase4-ci-cd.yml
```

Make sure the file contains:

```text
${{ secrets.DOCKERHUB_USERNAME }}
${{ secrets.DOCKERHUB_TOKEN }}
```

Never put the actual token in the file.

Commit:

```powershell
git add .github/workflows/phase4-ci-cd.yml
git commit -m "Add Phase 4 Docker Hub CI/CD"
git push
```

---

## 11. Check GitHub Actions

Go to:

```text
GitHub → Actions
```

Find:

```text
Phase 4 - CI/CD to Docker Hub
```

Expected:

```text
lint-and-test
    ├── Flake8
    └── pytest
        ↓
build-and-push
    ├── Docker Login
    ├── Buildx
    ├── Docker Build
    └── Docker Push
        ↓
PASS
```

A successful workflow shows a green check.

---

## 12. Check Docker Hub

Open:

```text
containerized-fastapi-cicd
```

You should see:

```text
latest
```

GitHub Actions performed the build and push automatically.

---

## 13. Pull the image locally

```powershell
docker pull YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

Check:

```powershell
docker images
```

This proves the image can be consumed independently of GitHub Actions.

---

## 14. Run Docker Hub image

```powershell
docker run -d --name phase4-app -p 8000:8000 YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

Check:

```powershell
docker ps
docker logs phase4-app
```

Test:

```text
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/info
http://localhost:8000/docs
```

The container should eventually show:

```text
Up ... (healthy)
```

The health check comes from the Phase 3 Dockerfile.

Stop/remove after testing:

```powershell
docker stop phase4-app
docker rm phase4-app
```

---

# Phase 4 complete flow

```text
Developer
    |
    | git push
    v
GitHub
    |
    v
GitHub Actions
    |
    +--> Flake8
    +--> pytest
    |
    | SUCCESS
    v
Build and Push
    |
    +--> Docker Login
    +--> Docker Buildx
    +--> Docker Build
    +--> Docker Push
    |
    v
Docker Hub
    |
    | docker pull
    v
Docker Container
    |
    v
FastAPI
```

---

# Phase 5 — AWS EC2

Phase 5 takes the Docker image from Docker Hub and deploys it to an AWS EC2 server.

## What are we adding?

```text
Docker Hub
    ↓
AWS EC2
    ↓
Docker Container
    ↓
FastAPI
    ↓
Internet
```

The important DevOps principle is:

```text
Build once
    ↓
Store artifact
    ↓
Deploy the same artifact
```

We do NOT build the Docker image again on EC2.

---

# Phase 5 architecture

```text
Developer
    |
    | git push
    v
GitHub
    |
    v
GitHub Actions
    |
    +--> Flake8
    +--> pytest
    +--> Docker build
    |
    v
Docker Hub
    |
    | docker pull
    v
AWS EC2
    |
    +--> Security Group
    |
    v
Docker Container
    |
    v
FastAPI
    |
    v
Internet
```

---

## 1. AWS EC2 concepts

### EC2

EC2 stands for Elastic Compute Cloud.

It provides virtual servers in AWS.

### EC2 instance

A virtual machine running in AWS with CPU, memory, storage and networking resources.

### AMI

Amazon Machine Image.

A template used to launch an EC2 instance.

We use an Ubuntu Server AMI.

### Instance type

Defines resources such as CPU, memory and network performance.

For this learning project, use a small instance appropriate for the current AWS free-tier/credit eligibility.

### Key pair

Used for secure SSH access.

The private `.pem` key must never be committed to GitHub.

### SSH

Secure Shell. Used to remotely administer the Linux server.

### Security Group

A virtual firewall controlling network access to the EC2 instance.

---

# 2. Launch EC2

In AWS:

```text
AWS Console
→ EC2
→ Launch instance
```

Use:

```text
Name:
docker-project-server
```

Select:

```text
Ubuntu Server
```

Choose a small instance appropriate for your account.

Create/select a key pair.

Example:

```text
docker-project-key
```

Download the `.pem` file.

Keep it secure.

---

# 3. Configure Security Group

Inbound rules:

### SSH

```text
Type: SSH
Port: 22
Source: My IP
```

Purpose:

```text
Your PC
    ↓
SSH :22
    ↓
EC2
```

### FastAPI

```text
Type: Custom TCP
Port: 8000
Source: 0.0.0.0/0
```

Purpose:

```text
Internet
    ↓
EC2 :8000
    ↓
FastAPI
```

For learning, port 8000 is exposed publicly.

A production system would normally use a load balancer/reverse proxy and HTTPS instead of directly exposing the application port.

---

# 4. Connect to EC2

On Windows PowerShell, go to the `.pem` location:

```powershell
cd C:\path\to\key
dir
```

Connect:

```powershell
ssh -i "docker-project-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP
```

Example:

```powershell
ssh -i "docker-project-key.pem" ubuntu@13.xxx.xxx.xxx
```

Successful connection:

```text
ubuntu@ip-172-31-33-130:~$
```

From this point, commands are being executed on EC2.

---

# 5. Prepare Ubuntu

Update package information:

```bash
sudo apt update
```

Upgrade packages:

```bash
sudo apt upgrade -y
```

Check Ubuntu:

```bash
lsb_release -a
```

Meaning:

```text
sudo
    → administrator privileges

apt update
    → refresh package information

apt upgrade
    → upgrade installed packages

-y
    → automatically answer yes
```

---

# 6. Install Docker

Install:

```bash
sudo apt install docker.io -y
```

Verify:

```bash
docker --version
```

Check Docker service:

```bash
sudo systemctl status docker
```

Look for:

```text
Active: active (running)
```

If the status screen opens:

```text
q
```

Enable Docker at boot:

```bash
sudo systemctl enable docker
```

Test:

```bash
sudo docker run hello-world
```

Expected:

```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

# 7. Allow ubuntu user to run Docker without sudo

Run:

```bash
sudo usermod -aG docker $USER
```

Apply the group change:

```bash
newgrp docker
```

Test:

```bash
docker ps
```

Check groups:

```bash
groups
```

The output should contain:

```text
docker
```

Now we can use:

```bash
docker ps
```

instead of:

```bash
sudo docker ps
```

---

# 8. Pull image from Docker Hub

Use the image created in Phase 4:

```bash
docker pull YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

Example:

```bash
docker pull swayam248/containerized-fastapi-cicd:latest
```

Verify:

```bash
docker images
```

The image should now exist locally on EC2.

This proves:

```text
Docker Hub
    ↓
EC2
```

---

# 9. Run FastAPI on EC2

Run:

```bash
docker run -d --name phase5-app -p 8000:8000 YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

Example:

```bash
docker run -d --name phase5-app -p 8000:8000 swayam248/containerized-fastapi-cicd:latest
```

Meaning:

```text
-d
    → detached/background mode

--name phase5-app
    → container name

-p 8000:8000
    → EC2 host port 8000 → container port 8000
```

---

# 10. Verify the container

```bash
docker ps
```

Look for:

```text
0.0.0.0:8000->8000/tcp
```

Logs:

```bash
docker logs phase5-app
```

The logs should show Uvicorn starting.

Test from EC2 itself:

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"healthy"}
```

---

# 11. Access application from internet

Find the EC2 Public IPv4 address.

Open:

```text
http://YOUR_EC2_PUBLIC_IP:8000
```

Expected:

```json
{
  "message": "Welcome to Docker Mastery Project"
}
```

Also test:

```text
http://YOUR_EC2_PUBLIC_IP:8000/health
http://YOUR_EC2_PUBLIC_IP:8000/info
http://YOUR_EC2_PUBLIC_IP:8000/docs
```

Network flow:

```text
Internet
    ↓
EC2 Public IP :8000
    ↓
Security Group
    ↓
EC2 host :8000
    ↓
Docker container :8000
    ↓
FastAPI
```

---

# 12. Public IP vs Private IP

EC2 has private networking inside the AWS VPC.

Private IP:

```text
Used inside the VPC/internal network
```

Public IP:

```text
Used to communicate with the EC2 instance from the internet
```

---

# 13. Inspect the container

```bash
docker inspect phase5-app
```

This provides detailed information about:

- Container
- Image
- Network
- Ports
- Environment
- Mounts
- Configuration
- Restart policy

---

# 14. Stop and start container

Stop:

```bash
docker stop phase5-app
```

Check:

```bash
docker ps
```

Check all containers:

```bash
docker ps -a
```

Start:

```bash
docker start phase5-app
```

Verify:

```bash
docker ps
```

Test:

```bash
curl http://localhost:8000/health
```

Important:

```text
docker stop
    ↓
Stops an existing container

docker start
    ↓
Starts that same container
```

---

# 15. Configure restart policy

Remove old container:

```bash
docker rm -f phase5-app
```

Create it again:

```bash
docker run -d \
  --name phase5-app \
  --restart unless-stopped \
  -p 8000:8000 \
  YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

Example:

```bash
docker run -d \
  --name phase5-app \
  --restart unless-stopped \
  -p 8000:8000 \
  swayam248/containerized-fastapi-cicd:latest
```

`--restart unless-stopped` tells Docker to attempt to restart the container after Docker/host restarts or unexpected failures unless it was explicitly stopped.

Verify:

```bash
docker ps
```

Then:

```bash
docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' phase5-app
```

Expected:

```text
unless-stopped
```

---

# 16. Important deployment concept — new versions

Suppose we change the application.

```text
Developer
    ↓
git commit
    ↓
git push
    ↓
GitHub Actions
    ↓
Flake8 + pytest
    ↓
Docker build
    ↓
Docker push
    ↓
Docker Hub
    ↓
NEW IMAGE
```

EC2 does NOT automatically replace its running container.

We need:

```bash
docker pull YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

Then recreate/restart the container using the new image.

This is why Phase 5 is a manual deployment.

Later phases will introduce managed/automated deployment.

---

# 17. Important `latest` concept

We currently use:

```text
containerized-fastapi-cicd:latest
```

If:

```text
latest → Version 1
```

and later:

```text
latest → Version 2
```

an existing running container does not magically become Version 2.

The deployment process must:

```text
Pull new image
    ↓
Stop/remove old container
    ↓
Start new container
```

Later we will learn better versioning strategies.

---

# Phase 5 final architecture

```text
                         INTERNET
                            |
                            | HTTP :8000
                            v
                 +----------------------+
                 |       AWS EC2        |
                 |                      |
                 |   Security Group     |
                 |     Port 8000        |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   Docker Container   |
                 |                      |
                 |      FastAPI         |
                 |      Port 8000       |
                 +----------+-----------+
                            ^
                            |
                       docker pull
                            |
                 +----------+-----------+
                 |      Docker Hub      |
                 |                      |
                 | containerized-       |
                 | fastapi-cicd:latest  |
                 +----------+-----------+
                            ^
                            |
                       docker push
                            |
                 +----------+-----------+
                 |    GitHub Actions    |
                 |                      |
                 | Flake8 + pytest      |
                 |       ↓              |
                 | Docker build         |
                 |       ↓              |
                 | Docker push          |
                 +----------+-----------+
                            ^
                            |
                         git push
                            |
                      +-----+-----+
                      | Developer |
                      +-----------+
```

---

# Phase 5 — Useful command reference

## Windows / SSH

```powershell
cd C:\path\to\key
dir
ssh -i "docker-project-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP
```

## Ubuntu preparation

```bash
sudo apt update
sudo apt upgrade -y
lsb_release -a
```

## Docker

```bash
sudo apt install docker.io -y
docker --version
sudo systemctl status docker
sudo systemctl enable docker
sudo docker run hello-world
```

## Docker permissions

```bash
sudo usermod -aG docker $USER
newgrp docker
docker ps
groups
```

## Pull image

```bash
docker pull YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
docker images
```

## Run

```bash
docker run -d --name phase5-app -p 8000:8000 YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

## Verify

```bash
docker ps
docker logs phase5-app
curl http://localhost:8000/health
```

## Inspect

```bash
docker inspect phase5-app
```

## Stop/start

```bash
docker stop phase5-app
docker ps
docker ps -a
docker start phase5-app
docker ps
```

## Restart policy

```bash
docker rm -f phase5-app

docker run -d \
  --name phase5-app \
  --restart unless-stopped \
  -p 8000:8000 \
  YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest

docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' phase5-app
```

---

# Phase 5 troubleshooting

## SSH fails

Check:

- EC2 is running
- Correct Public IPv4
- Correct `.pem`
- Username is `ubuntu`
- Security Group allows port 22
- If using `My IP`, your current public IP is correct

## Application does not open

Run:

```bash
docker ps
docker logs phase5-app
curl http://localhost:8000/health
```

If localhost works but the browser does not, check the Security Group port 8000 rule.

## Docker permission denied

Run:

```bash
sudo usermod -aG docker $USER
newgrp docker
docker ps
```

## Image not found

Check:

```bash
docker images
```

Then:

```bash
docker pull YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

## Container exits

Run:

```bash
docker ps -a
docker logs phase5-app
```

The logs normally reveal the startup problem.

## Port 8000 already in use

Check:

```bash
docker ps
```

If an old container owns the port:

```bash
docker rm -f phase5-app
```

Then recreate it.

---

# Phase 5 interview questions

## What is AWS EC2?

EC2 is AWS's service for provisioning and running virtual servers in the cloud.

## What is an EC2 instance?

A virtual machine running in AWS with compute, memory, storage and networking resources.

## What is an AMI?

An AMI is a template used to launch EC2 instances. It contains the operating system and configuration required to create the server.

## What is a Security Group?

A Security Group is a stateful virtual firewall associated with AWS resources such as EC2. It controls allowed network traffic using rules.

## Why port 22?

Port 22 is the standard SSH port used to remotely connect to the Linux server.

## Why port 8000?

Our FastAPI application listens on port 8000.

## What is SSH?

SSH is a secure protocol used to remotely access and administer Linux servers.

## Public IP vs private IP?

Private IP is used inside the VPC/internal AWS network. Public IP enables communication with the internet.

## Why Docker on EC2?

Docker provides the runtime environment needed to run the containerized FastAPI application.

## Why Docker Hub?

Docker Hub is the container registry used to store and distribute the image created by CI.

## Why not clone GitHub on EC2?

We separate source/build from runtime. GitHub Actions builds and tests the artifact, Docker Hub stores it, and EC2 pulls and runs that artifact.

## Why not build on EC2?

Building in CI and deploying the resulting artifact gives a more consistent deployment and separates build and runtime responsibilities.

## What does `-p 8000:8000` mean?

It maps port 8000 on the EC2 host to port 8000 inside the Docker container.

## What does `-d` mean?

It runs the container in detached/background mode.

## What does `--restart unless-stopped` mean?

It tells Docker to automatically restart the container after Docker/host restarts or unexpected failures unless the container was explicitly stopped.

## Does `docker pull` update a running container?

No. It downloads the image but does not replace the already-running container. The container must be recreated using the new image.

## Is Phase 5 production-ready?

Not fully. It is a learning deployment.

A production architecture would normally add:

- HTTPS
- Load balancer/reverse proxy
- More restrictive network rules
- Monitoring
- Centralized logging
- Automated deployment
- Image versioning
- Secrets management
- High availability
- Auto scaling

---

# Phase comparison

| Feature | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|---|---|---|---|---|---|
| FastAPI | Yes | Yes | Yes | Yes | Yes |
| Docker | Yes | Yes | Yes | Yes | Yes |
| Base image | Ubuntu | Python Slim | Python Alpine | Python Alpine | Python Alpine |
| Multi-stage | No | Yes | Yes | Yes | Yes |
| pytest | No | Yes | Yes | Yes | Yes |
| Flake8 | No | Yes | Yes | Yes | Yes |
| Git/GitHub | No | Yes | Yes | Yes | Yes |
| GitHub Actions | No | Yes | Yes | Yes | Yes |
| Buildx | No | Yes | Yes | Yes | Yes |
| Non-root user | No | No | Yes | Yes | Yes |
| HEALTHCHECK | No | No | Yes | Yes | Yes |
| Docker Hub | No | No | No | Yes | Yes |
| AWS EC2 | No | No | No | No | Yes |
| Cloud deployment | No | No | No | No | Yes |
| Restart policy | No | No | No | No | Yes |

---

# Project evolution

## Phase 1

```text
FastAPI
   ↓
Docker image
   ↓
Container
```

## Phase 2

```text
FastAPI
   ↓
Tests + Linting
   ↓
Multi-stage Docker image
   ↓
GitHub Actions CI
```

## Phase 3

```text
FastAPI
   ↓
Tests + Linting
   ↓
Hardened Docker image
   ├── Alpine
   ├── Multi-stage
   ├── Non-root user
   └── HEALTHCHECK
   ↓
GitHub Actions CI
```

## Phase 4

```text
FastAPI
   ↓
Tests + Linting
   ↓
Docker Build
   ↓
Docker Hub
```

## Phase 5

```text
FastAPI
   ↓
Tests + Linting
   ↓
Docker Build
   ↓
Docker Hub
   ↓
EC2
   ↓
Docker Container
   ↓
Internet
```

---

# Running the project again after shutdown

## Local Docker environment

Start Docker Desktop.

Open:

```text
docker-project
```

in VS Code.

Check:

```powershell
git status
docker ps -a
```

If the Phase 3 container already exists:

```powershell
docker start phase3-app
docker ps
```

If it does not exist:

```powershell
cd phase-3
docker build -t docker-mastery:phase3 .
docker run -d --name phase3-app -p 8000:8000 docker-mastery:phase3
docker ps
docker logs phase3-app
```

## EC2 deployment

If the EC2 instance was stopped rather than terminated:

1. Start the EC2 instance.
2. Get its current Public IPv4 address.
3. SSH into it.
4. Check Docker:

```bash
docker ps
```

5. If the container exists:

```bash
docker start phase5-app
```

6. Check:

```bash
docker ps
curl http://localhost:8000/health
```

If the container does not exist:

```bash
docker pull YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest

docker run -d \
  --name phase5-app \
  --restart unless-stopped \
  -p 8000:8000 \
  YOUR_DOCKERHUB_USERNAME/containerized-fastapi-cicd:latest
```

Then access:

```text
http://YOUR_EC2_PUBLIC_IP:8000
```

Important: an EC2 instance's public IPv4 address can change after stopping/starting unless an Elastic IP or another stable addressing mechanism is used.

---

# Phase 5 completion checklist

## AWS

- [x] EC2 instance created
- [x] Ubuntu AMI selected
- [x] Key pair created
- [x] Security Group configured
- [x] SSH port 22 configured
- [x] FastAPI port 8000 configured

## Server

- [x] Connected using SSH
- [x] Ubuntu packages updated
- [x] Docker installed
- [x] Docker service verified
- [x] Docker enabled at boot
- [x] Docker `hello-world` tested
- [x] `ubuntu` user configured for Docker

## Deployment

- [x] Docker image pulled from Docker Hub
- [x] Container started
- [x] Port 8000 mapped
- [x] Container logs checked
- [x] `/health` verified
- [x] Application accessed through EC2 public IP
- [x] Stop/start tested
- [x] Restart policy configured
- [x] Restart policy verified

---

# Current Status

- Phase 1: Complete
- Phase 2: Complete
- Phase 2 CI: Complete
- Phase 3: Complete
- Phase 3 CI: Green
- Phase 4: Complete
- Phase 5: Complete

---

# What comes next?

## Phase 6 — AWS ECR + ECS

We will move from:

```text
Docker Hub
    ↓
EC2
    ↓
docker run
```

towards:

```text
Docker Image
    ↓
Amazon ECR
    ↓
Amazon ECS
    ↓
ECS Task
    ↓
ECS Service
    ↓
Running container
```

This will introduce:

- Amazon ECR
- Amazon ECS
- ECS task definitions
- ECS services
- IAM roles
- AWS networking
- Managed container deployment
- Service desired count
- Container orchestration

Then:

```text
Phase 7 → Kubernetes
Phase 8 → Terraform
```

---

# License

This project is intended for learning and portfolio purposes.
