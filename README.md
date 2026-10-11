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

# Phase 6 — AWS ECR + ECS/Fargate + Application Load Balancer

## Goal

In this phase, we move our containerized FastAPI application from a manually managed Docker container on EC2 to a managed container deployment using Amazon ECS and AWS Fargate.

We also introduce Amazon ECR as the container image registry and an Application Load Balancer (ALB) to expose the application through a stable DNS endpoint.

In Phase 5, we used:

```text
Docker Hub
    ↓
AWS EC2
    ↓
Docker Container
    ↓
FastAPI
```

In Phase 6, we move towards:

```text
GitHub
    ↓
GitHub Actions
    ↓
Amazon ECR
    ↓
Amazon ECS
    ↓
AWS Fargate
    ↓
FastAPI Container
    ↓
Target Group
    ↓
Application Load Balancer
    ↓
Internet
```

The main difference is that we no longer need to manually manage the underlying server that runs the application container. Fargate manages the underlying compute infrastructure, while ECS manages the lifecycle of our containerized application.

### What we will implement

- Amazon ECR for storing Docker images
- Amazon ECS for container orchestration
- AWS Fargate for running containers without managing EC2 container hosts
- ECS cluster, task definition, task, and service
- IAM roles for authorized AWS access
- Application Load Balancer for incoming HTTP traffic
- Target group and health checks
- Security groups for controlling network traffic
- GitHub Actions integration for building and publishing the image to ECR
- Deployment verification and troubleshooting

---

# Phase 6 architecture

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +--> Flake8
    +--> pytest
    +--> Docker Build
    +--> AWS Authentication
    |
    v
Amazon ECR
    |
    | ECS pulls the configured image
    v
Amazon ECS Cluster
    |
    v
ECS Service
    |
    v
AWS Fargate Task
    |
    v
FastAPI Container :8000
    |
    v
Target Group
    |
    v
Application Load Balancer :80
    |
    v
Internet
```

**Important:** Publishing an image to ECR and deploying that image to ECS are two separate operations. The workflow must include an ECS deployment step to update the running service automatically. If the workflow only publishes the image, the ECS service must be updated separately.

---

# 1. AWS concepts required for Phase 6

Before creating the resources, understand the following concepts.

## Amazon ECR

Amazon Elastic Container Registry is an AWS-managed container image registry.

It stores Docker images that deployment platforms can pull and run.

Think of ECR as a storage location for our container images.

In Phase 4, we used Docker Hub. In Phase 6, we introduce ECR because it integrates with AWS IAM and ECS.

## Amazon ECS

Amazon Elastic Container Service is a managed container orchestration service.

It manages tasks, services, and deployments for containerized applications.

ECS helps maintain the desired number of running tasks and replaces failed tasks when possible.

## AWS Fargate

Fargate is a serverless compute engine for containers.

With ECS on EC2, we manage the EC2 container instances. With ECS on Fargate, AWS manages the underlying compute infrastructure for the tasks.

We still configure the task's CPU, memory, networking, IAM permissions, and application settings.

## ECS cluster

A cluster is a logical grouping for ECS services and tasks.

Our cluster is:

```text
containerized-fastapi-cluster
```

## Task definition

A task definition is a blueprint describing how ECS should run a task.

It includes configuration such as:

- Container image
- Container port
- CPU and memory
- IAM roles
- Environment variables
- Logging configuration
- Container health checks, if configured

## ECS task

A task is a running instance of a task definition.

It runs the configured container image.

## ECS service

An ECS service maintains the desired number of running tasks and manages the task deployment lifecycle.

Our service is:

```text
containerized-fastapi-task-service-5288p4im
```

The desired task count for this project was set to `1`.

## Application Load Balancer

An Application Load Balancer is a Layer 7 load balancer that receives HTTP/HTTPS requests and routes them to configured targets.

Our ALB is:

```text
fastapi-alb
```

## Target group

A target group identifies the destinations to which the ALB forwards requests.

Our target group is:

```text
fastapi-tg
```

## Health check

A health check periodically checks whether an application target responds as expected.

Our target group uses:

```text
/health
```

The application must respond successfully on this path for the target to become healthy under the configured health-check settings.

---

# 2. Prerequisites

Before starting Phase 6, make sure you have:

- An AWS account
- Access to the AWS Management Console
- Your Phase 5 FastAPI Docker image
- A GitHub repository containing the project
- A working GitHub Actions workflow
- An Amazon ECR repository
- An IAM role or credentials with the required permissions
- The application listening on port `8000`
- A working `/health` endpoint

Our AWS Region is:

```text
ap-southeast-2
```

This is the Asia Pacific (Sydney) Region.

**Important:** Keep all the Phase 6 resources in the same Region unless there is a specific reason to use another Region. ECR repositories, ECS resources, target groups, and load balancers are Region-specific.

Also, check the cost of Fargate tasks, load balancers, NAT gateways, data transfer, and CloudWatch Logs. These resources can incur charges even when the application receives little traffic. Delete resources when they are no longer required.

---

# 3. Create an Amazon ECR repository

## What are we doing?

Before ECS can run our application, the Docker image must be available in a registry that ECS can access.

We will create an ECR repository to store the image.

## Step 1: Open ECR

Navigate to:

```text
AWS Console
    → Search for ECR
    → Elastic Container Registry
    → Private registry
    → Repositories
```

Make sure the selected Region is:

```text
Asia Pacific (Sydney)
ap-southeast-2
```

## Step 2: Create a repository

Click:

```text
Create repository
```

Choose:

```text
Visibility settings:
Private
```

Give the repository a name, for example:

```text
containerized-fastapi-cicd
```

Use the repository name that actually exists in your account when following the remaining steps.

Keep other settings at their appropriate defaults for this learning project, unless you need to configure image scanning, encryption, or tag immutability.

Click:

```text
Create repository
```

## Step 3: Verify the repository

Open the repository and confirm that it exists.

Initially, the repository may contain no images.

That is expected. The image will appear after the CI/CD workflow successfully pushes it.

### What did we accomplish?

```text
Amazon ECR
    |
    v
Private image repository
    |
    v
Ready to store FastAPI Docker images
```

---

# 4. Understand ECR image names

An ECR image URI follows this general format:

```text
AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/REPOSITORY_NAME:TAG
```

For example:

```text
123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/containerized-fastapi-cicd:latest
```

The account ID in this example is illustrative.

The components are:

```text
AWS_ACCOUNT_ID
    ↓
Identifies the AWS account

dkr.ecr
    ↓
Amazon ECR registry endpoint

AWS_REGION
    ↓
Region containing the repository

REPOSITORY_NAME
    ↓
Repository storing the image

TAG
    ↓
Identifies the image version
```

You can find the actual repository URI by opening your ECR repository in the AWS Console.

We will use that URI in GitHub Actions and the ECS task definition.

**Important:** Do not guess or manually construct an incorrect account ID or repository URI. Copy the actual URI from ECR.

---

# 5. IAM permissions for ECR and ECS

## What is IAM?

AWS Identity and Access Management controls who can access AWS resources and what actions they can perform.

ECR, ECS, and GitHub Actions need appropriate permissions to complete their operations.

There are three important permission contexts in this phase.

### A. GitHub Actions AWS access

GitHub Actions needs authorized AWS access to publish Docker images to ECR.

If the workflow also deploys ECS, it needs the relevant permissions to update the task definition and ECS service.

### B. ECS task execution role

The ECS task execution role allows ECS/Fargate to perform operations needed to start the task.

Examples include:

- Pulling images from ECR
- Sending logs to CloudWatch Logs when configured
- Retrieving supported secrets during startup when configured

The AWS-managed policy `AmazonECSTaskExecutionRolePolicy` provides common execution permissions. Additional permissions may be needed depending on the features configured.

### C. ECS task role

The task role grants AWS permissions to the application code inside the container.

For example, if our FastAPI application needs to read from S3, the task role can grant narrowly scoped access to the required bucket.

If the application does not call AWS APIs, additional task-role permissions may not be necessary.

## Step 1: Check the ECS task execution role

Navigate to:

```text
AWS Console
    → IAM
    → Roles
```

Look for an ECS task execution role, commonly named:

```text
ecsTaskExecutionRole
```

The role must trust the ECS tasks service principal and have the permissions required to pull images and perform the configured startup operations.

If the standard role does not exist, create it through the ECS task execution role setup or the IAM role creation wizard.

For a normal ECS task execution role, the trusted service is:

```text
ecs-tasks.amazonaws.com
```

Attach the appropriate execution permissions, including the standard ECR image-pull and CloudWatch logging permissions if those features are used.

Do not attach administrator permissions just to make the deployment work.

## Step 2: Configure GitHub Actions AWS access

The workflow needs credentials or an assumed IAM role to access AWS.

Two common approaches are:

**Option A — GitHub Actions OIDC**

GitHub Actions assumes a restricted IAM role through OpenID Connect. This avoids storing long-lived AWS access keys in GitHub.

**Option B — GitHub Actions secrets**

Store the AWS credentials as GitHub repository secrets and reference them in the workflow.

OIDC is generally preferable when properly configured.

Whichever method you use, grant only the permissions required for the intended operations. The example workflow later in this phase uses repository secrets for simplicity; it must match the authentication method configured in your account.

---

# 6. Configure GitHub Actions for ECR

## Goal

Our existing CI workflow runs linting and tests. We now want a workflow that builds the Docker image and publishes it to ECR.

The flow becomes:

```text
git push
    |
    v
GitHub Actions
    |
    +--> Flake8
    +--> pytest
    |
    v
Docker Build
    |
    v
AWS Authentication
    |
    v
Amazon ECR Login
    |
    v
Docker Image Push
```

The existing Phase 3 Dockerfile uses the FastAPI application, dependencies, non-root user, and health check.

For this example, the image is built from:

```text
phase-3/
```

Use the Dockerfile and build context that your working workflow actually uses.

## Step 1: Configure GitHub repository secrets

Open your GitHub repository:

```text
GitHub
    → containerized-fastapi-cicd
    → Settings
    → Secrets and variables
    → Actions
```

If using the access-key approach, create the required secrets:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

Create a Region variable or secret:

```text
AWS_REGION
```

Set it to:

```text
ap-southeast-2
```

Also configure the ECR repository name using a repository variable or workflow environment value, for example:

```text
ECR_REPOSITORY
```

Set it to the exact repository name created in Step 3.

Do not store actual credentials in the README or workflow file.

If you use OIDC, configure the GitHub identity provider, IAM role trust policy, role permissions, and role ARN instead of adding long-lived access keys.

## Step 2: Understand the workflow

The workflow needs to perform the following operations:

1. Check out the repository.
2. Install the required Python dependencies.
3. Run Flake8.
4. Run pytest.
5. Authenticate to AWS.
6. Authenticate Docker to ECR.
7. Build the Docker image.
8. Tag the image with the ECR registry and repository.
9. Push the image to ECR.

A simplified example of the ECR publishing workflow is shown below.

**Important:** This is an example template. Keep your existing working Phase 6 workflow if it already performs these operations. Do not replace a working workflow with this example without checking its paths, credentials, repository name, and build context.

Create or inspect:

```text
.github/workflows/phase6-ecr.yml
```

Example:

```yaml
name: Phase 6 - Build and Push to ECR

on:
  push:
    branches:
      - main
    paths:
      - "phase-3/**"
      - ".github/workflows/phase6-ecr.yml"

  workflow_dispatch:

permissions:
  contents: read

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

    env:
      AWS_REGION: ${{ secrets.AWS_REGION }}
      ECR_REPOSITORY: ${{ vars.ECR_REPOSITORY }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Log in to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push image
        uses: docker/build-push-action@v6
        with:
          context: ./phase-3
          file: ./phase-3/Dockerfile
          push: true
          tags: |
            ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:latest
            ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:${{ github.sha }}
```

This example uses repository secrets for AWS credentials. If your setup uses OIDC, change the workflow to request the required OIDC token permission and assume the configured IAM role instead.

The workflow's AWS identity must have permission to authenticate to ECR and push images to the target repository.

## Step 3: Understand `needs`

The workflow contains:

```yaml
needs: lint-and-test
```

This creates the following dependency:

```text
lint-and-test
      |
      | SUCCESS
      v
build-and-push
```

If the linting or tests fail, the image-publishing job will not run.

## Step 4: Understand the image tags

The example publishes two tags:

```text
latest
```

and:

```text
Git commit SHA
```

The commit SHA identifies the source revision associated with the image and makes it easier to trace a deployed version back to Git.

For example:

```text
containerized-fastapi-cicd:latest
containerized-fastapi-cicd:a1b2c3d...
```

The actual image URI is the ECR registry address followed by the repository and tag.

## Step 5: Commit and push the workflow

From your project root:

```powershell
git status
git add .github/workflows/phase6-ecr.yml
git commit -m "Add Phase 6 ECR CI/CD"
git push origin main
```

If your Phase 6 workflow already exists and is working, do not create a duplicate workflow unnecessarily.

## Step 6: Verify GitHub Actions

Open:

```text
GitHub Repository
    → Actions
    → Phase 6 - Build and Push to ECR
```

Inspect the job logs.

Expected flow:

```text
Checkout code
    ↓
Install dependencies
    ↓
Flake8
    ↓
pytest
    ↓
Configure AWS credentials
    ↓
Login to ECR
    ↓
Build image
    ↓
Push image
```

The workflow should complete successfully.

## Step 7: Verify the image in ECR

Open:

```text
AWS Console
    → ECR
    → Repositories
    → Your ECR repository
    → Images
```

Confirm that the expected image tags appear.

If the repository remains empty, inspect the GitHub Actions logs, AWS permissions, Region, and repository name.

### What did we accomplish?

```text
GitHub
    ↓
GitHub Actions
    ↓
Build and test
    ↓
Amazon ECR
    ↓
Image stored and ready for deployment
```

---

# 7. Create the ECS cluster

## What are we doing?

We have a container image registry. Now we need an ECS cluster in which our service and tasks will be managed.

## Step 1: Open ECS

Navigate to:

```text
AWS Console
    → Search for ECS
    → Amazon Elastic Container Service
    → Clusters
```

Make sure the Region is:

```text
ap-southeast-2
```

## Step 2: Create the cluster

Click:

```text
Create cluster
```

Enter:

```text
Cluster name:
containerized-fastapi-cluster
```

Choose the Fargate/serverless option or the standard cluster configuration available in the current ECS console.

Fargate does not require you to create or manage EC2 container instances.

Keep any optional monitoring settings appropriate for your account and learning needs.

Click:

```text
Create
```

## Step 3: Verify the cluster

Open the cluster.

You should be able to view its services and tasks after they are created.

At this stage, the cluster may have no running tasks. That is normal.

### What did we accomplish?

```text
Amazon ECS
    |
    v
containerized-fastapi-cluster
    |
    v
Ready to manage the application service
```

---

# 8. Create the networking configuration

Before running the application, understand how traffic will reach the task.

## What is a VPC?

A Virtual Private Cloud is a logically isolated network in AWS.

Resources such as ECS tasks, load balancers, and EC2 instances are associated with VPC networking.

## What is a subnet?

A subnet is a range of IP addresses within a VPC.

Subnets are associated with Availability Zones. An ALB generally uses subnets in at least two Availability Zones for a standard highly available deployment.

## Public and private subnets

A public subnet has a route to an Internet Gateway.

A private subnet does not provide direct inbound internet access through an Internet Gateway.

A Fargate task can run in public or private subnets depending on the intended architecture.

For production, private task subnets with appropriate outbound access through NAT or suitable VPC endpoints are commonly preferred. For this learning deployment, use the networking arrangement already configured for the project and ensure it allows the required ECR access and application traffic.

## Security groups

Security groups act as virtual firewalls for the ALB and ECS tasks.

We need to permit traffic from the client to the ALB and from the ALB to the application container.

Our intended traffic flow is:

```text
Client
    |
    | HTTP :80
    v
ALB Security Group
    |
    | TCP :8000
    v
ECS Task Security Group
    |
    v
FastAPI Container
```

We will configure and verify the security groups in the following sections.

---

# 9. Create the ECS task security group

## Goal

Allow the application to receive traffic from the ALB without exposing the container port directly to the entire internet.

## Step 1: Open security groups

Navigate to:

```text
AWS Console
    → EC2
    → Network & Security
    → Security Groups
```

Make sure you are in the same Region and VPC used by your ECS service and ALB.

## Step 2: Create the task security group

Click:

```text
Create security group
```

Enter a name such as:

```text
fastapi-ecs-task-sg
```

Description:

```text
Security group for the FastAPI ECS tasks
```

Select the VPC used by the deployment.

Do not select a different VPC from the one used by the ALB.

## Step 3: Configure inbound rules

The intended inbound rule is:

| Type | Protocol | Port | Source |
|---|---|---:|---|
| Custom TCP | TCP | 8000 | ALB security group |

To configure it:

1. Select Custom TCP.
2. Enter port `8000`.
3. For Source, choose the security group associated with the ALB.
4. Save the rule.

Do not use `0.0.0.0/0` as the task's port 8000 source when only ALB traffic is required.

## Step 4: Configure outbound traffic

The task must be able to perform its required outbound operations, including retrieving images or communicating with required AWS endpoints according to the network design.

For a basic learning deployment, the default outbound rule may be used. In a production environment, restrict egress according to the actual application and endpoint requirements.

Save the security group.

---

# 10. Create the target group

## What is a target group?

A target group defines the destinations to which the ALB forwards requests.

For this project, the application runs on port `8000`, and the health check uses `/health`.

## Step 1: Open target groups

Navigate to:

```text
AWS Console
    → EC2
    → Load Balancing
    → Target Groups
    → Create target group
```

## Step 2: Configure the target group

Select:

```text
Target type:
IP addresses
```

This is important because Fargate tasks using `awsvpc` networking have their own network interfaces and IP addresses. The ALB target group should use IP targets for this configuration.

Enter:

```text
Target group name:
fastapi-tg
```

Configure:

```text
Protocol:
HTTP

Port:
8000
```

Select the same VPC that will be used by the ALB and ECS tasks.

## Step 3: Configure the health check

Set:

```text
Health check protocol:
HTTP

Health check path:
/health
```

The health-check port should use the configured traffic port unless there is a specific reason to use a different port.

Review the remaining health-check settings. The application's health endpoint must return a status accepted by the target group's success-code configuration.

## Step 4: Register targets

For an ECS service, allow ECS to register and deregister the Fargate task targets through the service's load-balancer integration.

Do not permanently register a temporary task IP manually as a substitute for ECS service registration. Task IPs can change when tasks are replaced.

Complete target-group creation.

### What did we accomplish?

```text
Target Group
    |
    +--> Protocol: HTTP
    +--> Port: 8000
    +--> Health check: /health
    +--> Target type: IP
```

---

# 11. Create the Application Load Balancer

## What is an ALB?

The Application Load Balancer receives HTTP/HTTPS requests and forwards them to registered targets.

The ALB provides a DNS endpoint for the application so users do not need to know the private IP address of a Fargate task.

## Step 1: Open load balancers

Navigate to:

```text
AWS Console
    → EC2
    → Load Balancing
    → Load Balancers
    → Create load balancer
```

Select:

```text
Application Load Balancer
```

## Step 2: Configure basic settings

Enter:

```text
Load balancer name:
fastapi-alb
```

Scheme:

```text
Internet-facing
```

Choose the IP address type appropriate for the deployment.

An internet-facing ALB requires suitable public subnets and routing.

## Step 3: Select the VPC and subnets

Select the same VPC used by the ECS service.

Select appropriate subnets in at least two Availability Zones for a standard internet-facing ALB deployment.

Verify that the selected subnets have the required routing and that the ALB is reachable through its intended public endpoint.

## Step 4: Create the ALB security group

If the ALB already has an appropriate security group, you can use it.

Otherwise, create one such as:

```text
fastapi-alb-sg
```

The inbound rule for this learning setup is:

| Type | Protocol | Port | Source |
|---|---|---:|---|
| HTTP | TCP | 80 | Intended client source |

For a public learning endpoint, the intended client source may be `0.0.0.0/0`. This exposes the HTTP endpoint to the internet, so use it only when appropriate.

For a production deployment, configure HTTPS with a suitable certificate and a port 443 listener.

## Step 5: Configure the listener

Create an HTTP listener:

```text
Protocol:
HTTP

Port:
80
```

Configure its default action to forward traffic to:

```text
fastapi-tg
```

If the target group is not yet available during ALB creation, create the ALB and configure the listener after creating the target group.

Review the settings and create the load balancer.

## Step 6: Verify the ALB

Wait until the ALB state becomes:

```text
Active
```

Copy its DNS name from the load balancer details.

We will use that DNS name after the ECS service has registered a healthy task.

---

# 12. Create the ECS task definition

## Goal

Define how ECS should run the FastAPI container.

## Step 1: Open task definitions

Navigate to:

```text
AWS Console
    → Amazon ECS
    → Task definitions
    → Create new task definition
```

Choose the Fargate-compatible launch configuration available in the current console.

## Step 2: Enter task definition details

Use a family name such as:

```text
containerized-fastapi-task
```

Select an appropriate task CPU and memory combination supported by Fargate.

For a lightweight learning application, a small supported configuration is generally sufficient, but choose values appropriate for the application and validate them against the available Fargate combinations.

## Step 3: Configure the task execution role

Select the task execution role configured earlier.

The role must have the permissions required to pull the ECR image and perform the configured startup operations.

If the application needs to access AWS services directly, configure a separate task role with the required application permissions.

## Step 4: Add the container

Enter a container name such as:

```text
fastapi-container
```

For the image URI, copy the actual ECR image URI from the ECR repository.

It should follow this pattern:

```text
AWS_ACCOUNT_ID.dkr.ecr.ap-southeast-2.amazonaws.com/REPOSITORY_NAME:TAG
```

Use an image tag that exists in ECR.

For a reproducible deployment, a versioned tag or image digest is preferable to relying only on `latest`.

## Step 5: Configure port mapping

The FastAPI application listens on:

```text
8000
```

Configure the container port as:

```text
8000
```

Use the appropriate TCP port mapping for the container.

The application command should start Uvicorn and bind to:

```text
0.0.0.0:8000
```

This makes the application listen on the container's network interface rather than only on the loopback interface.

## Step 6: Configure logging

If CloudWatch logging is enabled, select the appropriate log driver and configure a log group or log configuration.

The task execution role must have the required permissions.

CloudWatch Logs helps diagnose container startup failures and application errors.

## Step 7: Review and create

Review the following before creating the task definition:

- Correct ECR image URI
- Container port `8000`
- Appropriate CPU and memory
- Correct task execution role
- Application startup command
- Logging configuration, if enabled
- Any required environment variables

Create the task definition.

### What did we accomplish?

We created the blueprint ECS will use to launch the application container.

---

# 13. Create the ECS service

## What is an ECS service?

The ECS service manages the desired number of running tasks and their deployment lifecycle.

For this project, we want one running task.

## Step 1: Open the cluster

Navigate to:

```text
AWS Console
    → Amazon ECS
    → Clusters
    → containerized-fastapi-cluster
```

Open:

```text
Services
    → Create
```

## Step 2: Configure service details

Choose:

```text
Compute configuration:
AWS Fargate
```

Select the task definition family and revision created earlier.

Enter the service name:

```text
containerized-fastapi-task-service-5288p4im
```

If creating a new service from scratch, you may choose another valid name. The name above is the service used in this project.

Set:

```text
Desired tasks:
1
```

This tells ECS to attempt to keep one task running.

## Step 3: Configure networking

Select the VPC used by the ALB and target group.

Select the subnets appropriate for the task network design.

Choose the ECS task security group created earlier.

Configure public IP assignment according to the selected subnets and network design.

If tasks use private subnets, ensure they have the required access to ECR and other required AWS endpoints, typically through NAT or appropriate VPC endpoints.

If tasks use public subnets, verify that the routing and public IP settings support the intended outbound access.

## Step 4: Attach the load balancer

Enable the load-balancing integration.

Select:

```text
Load balancer:
fastapi-alb
```

Select the listener:

```text
HTTP :80
```

Select the target group:

```text
fastapi-tg
```

Map the target group to the FastAPI container and its port:

```text
fastapi-container : 8000
```

The exact container name must match the container configured in the task definition.

## Step 5: Create the service

Review the settings and create the ECS service.

ECS will attempt to launch the task and register its target with the target group.

Wait for the service to stabilize.

### Expected service status

The desired state for this project is:

```text
Desired tasks: 1
Running tasks: 1
Pending tasks: 0
```

A service can take time to stabilize while the task starts and the target group performs health checks.

---

# 14. Understand the complete ECS deployment flow

Once the service is created, the flow is:

```text
ECS Service
    |
    | Uses
    v
Task Definition
    |
    | References
    v
Amazon ECR Image
    |
    | Pulled by
    v
Fargate Task
    |
    v
FastAPI Container :8000
    |
    | Registered with
    v
Target Group
    |
    | Receives traffic from
    v
Application Load Balancer :80
```

The service maintains the desired task count. The task definition determines how the task runs. Fargate supplies the underlying compute infrastructure.

The ALB sends requests to eligible healthy targets.

---

# 15. Verify the ECS service

Navigate to:

```text
AWS Console
    → Amazon ECS
    → Clusters
    → containerized-fastapi-cluster
    → Services
    → containerized-fastapi-task-service-5288p4im
```

Check the service's deployment and task status.

Verify:

```text
Desired count: 1
Running count: 1
Pending count: 0
```

Also check:

- The task is in the `RUNNING` state.
- The task definition references the expected image.
- The latest service deployment completed successfully.
- There are no repeated task restarts.
- The service events do not show unresolved errors.

If the task stops, open the stopped task details and inspect the stopped reason and container exit code.

If logging is configured, inspect the container logs in CloudWatch.

---

# 16. Verify the target group health

Navigate to:

```text
AWS Console
    → EC2
    → Load Balancing
    → Target Groups
    → fastapi-tg
    → Targets
```

The ECS service should register its running task with the target group.

Verify:

```text
Target type: IP
Port: 8000
Health check path: /health
```

Wait for the health checks to complete.

Expected:

```text
Health status: Healthy
```

## Why can a target be unhealthy?

The container may be running but unable to respond correctly to the load balancer.

Possible causes:

- Incorrect target port
- Incorrect health-check path
- Application startup delay
- Application failure
- Security group blocking ALB traffic
- Incorrect VPC or networking configuration

During this project, an earlier target failed load-balancer health checks and entered a draining state. A replacement target later became healthy.

This is why we verify both the ECS task state and the target group health.

---

# 17. Configure security groups correctly

The intended traffic flow is:

```text
Internet
    |
    | HTTP :80
    v
ALB Security Group
    |
    | TCP :8000
    v
ECS Task Security Group
    |
    v
FastAPI Container
```

## ALB security group

Inbound:

```text
Protocol: TCP
Port: 80
Source: Intended client source
```

## ECS task security group

Inbound:

```text
Protocol: TCP
Port: 8000
Source: ALB security group
```

The task security group should allow application traffic from the ALB security group, not from every internet address.

## Important AWS console issue

When changing a security-group rule, AWS may reject an attempt to change an existing IPv4 CIDR source directly into a referenced security-group source.

For example, changing a rule from:

```text
0.0.0.0/0
```

to:

```text
ALB security group
```

may produce an error.

The solution is to remove the old rule if it is no longer needed and create a new rule with the correct security-group source.

After saving the rule, recheck the target group's health.

---

# 18. Access FastAPI through the ALB

## Step 1: Find the ALB DNS name

Navigate to:

```text
AWS Console
    → EC2
    → Load Balancers
    → fastapi-alb
```

Select the ALB and copy its DNS name.

The DNS name is assigned by AWS and can differ between deployments.

Do not use the Fargate task's private IP as the public application URL.

## Step 2: Open the root endpoint

In your browser:

```text
http://YOUR_ALB_DNS_NAME/
```

Replace `YOUR_ALB_DNS_NAME` with the actual DNS name.

Expected response:

```json
{
  "message": "Welcome to Docker Mastery Project"
}
```

## Step 3: Test the health endpoint

Open:

```text
http://YOUR_ALB_DNS_NAME/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

## Step 4: Test the info endpoint

Open:

```text
http://YOUR_ALB_DNS_NAME/info
```

Expected response:

```json
{
  "application": "FastAPI Docker App",
  "version": "1.0.0",
  "environment": "development"
}
```

## Step 5: Open Swagger UI

Open:

```text
http://YOUR_ALB_DNS_NAME/docs
```

FastAPI's interactive Swagger UI should appear.

In this project, the `/docs` page opened successfully in the browser, and the root endpoint was also verified through the ALB.

### What did we prove?

```text
Browser
    |
    v
ALB
    |
    v
Target Group
    |
    v
Fargate Task
    |
    v
FastAPI
```

The request can reach the application through the load balancer.

**Security note:** This project uses HTTP for learning. Do not send sensitive information through the public HTTP endpoint. Production systems should use HTTPS and appropriate security controls.

---

# 19. Understand how Phase 6 differs from Phase 5

In Phase 5, we manually pulled an image and ran a Docker container on EC2.

In Phase 6, we use ECS to manage the application's running tasks.

| Phase 5 | Phase 6 |
|---|---|
| Docker Hub stores the image. | Amazon ECR stores the image. |
| EC2 runs the Docker container. | Fargate runs the task's container. |
| We manually manage the container on EC2. | ECS service manages the desired task count. |
| EC2 is the server we administer. | AWS manages the underlying Fargate compute infrastructure. |
| We accessed the public EC2 IP and port. | We access the ALB DNS endpoint. |
| We used Docker restart policy. | ECS service manages task replacement and service deployments. |

The important change is not simply moving the image from Docker Hub to ECR. We have also changed the way the application is run and exposed.

---

# 20. Updating the application after a code change

Suppose we change the FastAPI application and push the changes to GitHub.

The image-publishing flow is:

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
Amazon ECR
    |
    v
New image available
```

However, the ECS service may still be running the previous image.

## Why?

ECR stores images. ECS runs the image referenced by the task definition used by the service.

Pushing a new image with the same mutable tag does not automatically replace a running task.

## Manual deployment approach

If your workflow only pushes the image to ECR:

1. Verify the new image exists in ECR.
2. Open the ECS task definition.
3. Create a new revision referencing the intended image tag or digest.
4. Open the ECS service.
5. Update the service to use the new task definition revision.
6. Wait for the deployment to complete.
7. Verify the new task is running.
8. Confirm the target group is healthy.
9. Test the application through the ALB.

## Automated deployment approach

A complete ECS deployment workflow can automate the task-definition update and ECS service deployment after successfully publishing the image.

The deployment stage would follow:

```text
Tests pass
    |
    v
Image built
    |
    v
Image pushed to ECR
    |
    v
Task definition updated
    |
    v
ECS service updated
    |
    v
Deployment completes
    |
    v
Target becomes healthy
```

Only describe ECS deployment as automated if the workflow actually performs these operations.

---

# 21. Troubleshooting

## Problem 1: GitHub Actions fails to publish to ECR

Check:

- AWS authentication configuration
- GitHub secrets or OIDC role configuration
- IAM permissions for ECR
- Correct AWS Region
- Correct ECR repository name
- Docker build context
- Dockerfile path
- GitHub Actions logs

Open:

```text
GitHub Repository
    → Actions
    → Failed workflow
    → Failed job
    → Failed step
```

Read the first meaningful error instead of changing permissions blindly.

## Problem 2: ECR repository exists but contains no images

Check:

- Did the workflow reach the image-push step?
- Did the Docker build succeed?
- Did authentication to ECR succeed?
- Was the image tagged with the correct registry and repository?
- Did the workflow push to the expected Region?

A successful Docker build does not necessarily mean the image was pushed.

## Problem 3: ECS task fails to start

Open:

```text
Amazon ECS
    → Clusters
    → containerized-fastapi-cluster
    → Services
    → Tasks
```

Inspect the stopped task.

Check:

- Stopped reason
- Container exit code
- Image URI and tag
- Task execution role
- CPU and memory
- Container command
- Required environment variables
- Network access to ECR
- CloudWatch logs, if configured

## Problem 4: ECS cannot pull the image

Check:

- The image exists in ECR.
- The task definition uses the correct image URI.
- The task execution role has the required permissions.
- The task's network configuration permits access to ECR and required endpoints.
- The image tag or digest is correct.

## Problem 5: ECS task is running, but the target is unhealthy

Check:

```text
Target Group
    → fastapi-tg
    → Targets
    → Health status and reason
```

Then verify:

- Target type is IP.
- Application port is `8000`.
- Health-check path is `/health`.
- The application starts correctly.
- The task security group allows traffic from the ALB security group.
- The ALB and task are in the intended VPC/network configuration.

A running task does not automatically mean that the ALB can successfully reach the application.

## Problem 6: ALB DNS name does not open

Check:

- ALB state is Active.
- Listener is configured on port `80`.
- ALB security group permits the intended client traffic.
- Target group has a healthy target.
- ECS service has a running task.
- Task security group permits traffic from the ALB security group.
- Application listens on port `8000`.

If the target group has no healthy targets, the ALB may return an error even when the load balancer itself is active.

## Problem 7: `/docs` does not open

Check the root endpoint first:

```text
http://YOUR_ALB_DNS_NAME/
```

Then test:

```text
http://YOUR_ALB_DNS_NAME/health
```

If both fail, investigate the ALB, target group, networking, and application.

If the root works but `/docs` does not, verify that the application exposes the FastAPI documentation endpoint and that no application-level configuration disables it.

## Problem 8: Security group rule cannot be changed

If AWS rejects a direct source-type change:

1. Inspect the existing rule.
2. Confirm whether the old rule is still needed.
3. Delete the old rule if it is safe to remove.
4. Create a replacement rule.
5. Choose the ALB security group as the source.
6. Save the rule.
7. Recheck target health.

Do not remove unrelated rules needed for SSH, administration, application access, or other services.

## Problem 9: New image exists, but ECS still runs the old version

Check:

- Whether the task definition references the new image.
- Whether a new task definition revision was created, if required.
- Whether the ECS service was updated.
- Whether the latest deployment completed.
- Whether the running task uses the expected image.

A new ECR image alone does not prove that ECS has deployed it.

---

# 22. Important commands and verification reference

Most Phase 6 configuration is managed through the AWS Console and GitHub Actions.

## Git verification from Windows PowerShell

Run from the project root:

```powershell
git status
git log --oneline -5
```

Check the workflows:

```powershell
Get-ChildItem .github\workflows
```

Inspect the Phase 6 workflow:

```powershell
Get-Content .github\workflows\phase6-ecr.yml
```

Use the actual filename if your existing workflow has a different name.

## AWS CLI verification

If AWS CLI credentials are configured, verify the current identity:

```powershell
aws sts get-caller-identity
```

Verify the Region:

```powershell
aws configure get region
```

List ECR repositories:

```powershell
aws ecr describe-repositories --region ap-southeast-2
```

List images in a repository, replacing the placeholder with your actual ECR repository name:

```powershell
aws ecr describe-images `
  --repository-name YOUR_ECR_REPOSITORY_NAME `
  --region ap-southeast-2
```

List ECS clusters:

```powershell
aws ecs list-clusters --region ap-southeast-2
```

List services in the project cluster:

```powershell
aws ecs list-services `
  --cluster containerized-fastapi-cluster `
  --region ap-southeast-2
```

Describe the service:

```powershell
aws ecs describe-services `
  --cluster containerized-fastapi-cluster `
  --services containerized-fastapi-task-service-5288p4im `
  --region ap-southeast-2
```

These commands require suitable AWS credentials and IAM permissions.

They verify AWS resource state; they do not replace the need to inspect target health and test the application through the ALB.

---

# 23. Phase 6 interview concepts

## What is Amazon ECR?

Amazon ECR is an AWS-managed container image registry used to store and distribute Docker images.

## Why did we use ECR instead of Docker Hub?

ECR integrates with AWS IAM and ECS. It allows us to store images within AWS and grant controlled access to deployment services.

## What is Amazon ECS?

ECS is a managed container orchestration service that manages containerized applications through task definitions, tasks, and services.

## What is AWS Fargate?

Fargate is a serverless compute engine for containers. It allows ECS to run tasks without requiring us to manage the underlying EC2 container hosts.

## What is an ECS cluster?

A logical grouping of ECS services and tasks.

## What is a task definition?

A blueprint that defines how ECS should run a task, including its image, port mappings, CPU, memory, IAM roles, and other configuration.

## What is an ECS task?

A running instance of a task definition.

## What is an ECS service?

A resource that maintains the desired number of tasks and manages their deployment lifecycle.

## What does desired count mean?

It is the number of running tasks ECS attempts to maintain for the service.

For this project, the desired count is `1`.

## What is the difference between a task and a service?

A task is a running instance of the application definition. A service manages the desired number of tasks and their deployment lifecycle.

## What is a task execution role?

It allows ECS/Fargate to perform startup operations such as pulling images from ECR and sending logs to CloudWatch when configured.

## What is a task role?

It grants AWS permissions to the application code running inside the container.

## What is an ALB?

An Application Load Balancer receives HTTP/HTTPS requests and routes them to configured targets.

## What is a target group?

A target group defines the destinations to which the load balancer forwards requests.

## Why is the target type IP used for Fargate?

Fargate tasks using `awsvpc` networking have their own network interfaces and IP addresses. The ALB uses IP targets to route traffic to them.

## Why do we need health checks?

Health checks help determine whether a target is ready to receive traffic.

## Can an ECS task be running but unhealthy?

Yes. The application may be running but unreachable from the load balancer, listening on the wrong port, or returning an unexpected health-check response.

## Does pushing a new image to ECR update ECS automatically?

Not by itself. The ECS service must be updated to use the new image through an appropriate task-definition/service deployment process.

## Why use an ALB instead of a task IP?

Task IP addresses can change when tasks are replaced. The ALB provides a stable DNS endpoint and routes traffic to eligible targets.

## Why restrict port 8000 to the ALB security group?

This limits access to the application to the intended traffic path instead of exposing the container port directly to all internet clients.

## Is this project production-ready?

This is a portfolio learning project. Production deployments may require HTTPS, private task subnets, stricter IAM and network policies, image scanning, secrets management, centralized logging, monitoring, high availability, and cost controls.

---

# Phase 6 command and configuration summary

## AWS resources

```text
Region:
ap-southeast-2

ECS cluster:
containerized-fastapi-cluster

ECS service:
containerized-fastapi-task-service-5288p4im

Load balancer:
fastapi-alb

Target group:
fastapi-tg

Container port:
8000

Health check:
/health
```

## GitHub Actions flow

```text
git push
    ↓
GitHub Actions
    ↓
Flake8 + pytest
    ↓
Docker build
    ↓
AWS authentication
    ↓
ECR login
    ↓
Push image
```

## ECS deployment flow

```text
Amazon ECR
    ↓
ECS task definition
    ↓
ECS service
    ↓
Fargate task
    ↓
FastAPI container
    ↓
Target group
    ↓
ALB
```

## Application verification

```text
http://YOUR_ALB_DNS_NAME/
http://YOUR_ALB_DNS_NAME/health
http://YOUR_ALB_DNS_NAME/info
http://YOUR_ALB_DNS_NAME/docs
```

Replace `YOUR_ALB_DNS_NAME` with the DNS name displayed for `fastapi-alb`.

---

# Phase 6 completion checklist

## ECR and CI/CD

- [x] ECR repository created
- [x] GitHub Actions configured to build and publish the container image to ECR
- [x] Image publishing workflow verified
- [x] Image available in ECR

## ECS and Fargate

- [x] ECS cluster created
- [x] Task definition configured
- [x] ECS service created
- [x] Desired task count set to `1`
- [x] Running task verified
- [x] Service deployment completed

## Load balancing and networking

- [x] Application Load Balancer created
- [x] Target group configured for IP targets
- [x] Application port configured as `8000`
- [x] Health-check path configured as `/health`
- [x] Security groups adjusted for ALB-to-task traffic
- [x] Target group health verified

## Application testing

- [x] Root endpoint opened through the ALB
- [x] FastAPI `/docs` opened through the ALB
- [x] ECS service verified with one running task and zero pending tasks

**Deployment automation note:** The checklist above marks the image-publishing workflow complete. Mark fully automated ECS deployment complete only if the workflow also updates the task definition/service. If that part is performed manually, document it as a manual deployment step.

---

# Phase 6 final architecture

```text
                          DEVELOPER
                              |
                              | git push
                              v
                     GITHUB REPOSITORY
                              |
                              v
                       GITHUB ACTIONS
                              |
                  +-----------+-----------+
                  |           |           |
                  v           v           v
                Flake8      pytest     Docker Build
                  |           |           |
                  +-----------+-----------+
                              |
                              v
                       AMAZON ECR
                              |
                              | Image pull
                              v
                       AMAZON ECS
                              |
                              v
                       ECS SERVICE
                              |
                              v
                       AWS FARGATE
                              |
                              v
                      FASTAPI :8000
                              |
                              v
                        TARGET GROUP
                              |
                              v
                     APPLICATION LOAD
                       BALANCER :80
                              |
                              v
                           INTERNET
```

---

# Project evolution

## Phase 1

```text
FastAPI
    ↓
Docker Image
    ↓
Docker Container
```

## Phase 2

```text
FastAPI
    ↓
Testing + Linting
    ↓
Multi-stage Docker
    ↓
GitHub Actions CI
```

## Phase 3

```text
FastAPI
    ↓
Tests + Linting
    ↓
Hardened Docker Image
    ├── Alpine
    ├── Multi-stage build
    ├── Non-root user
    └── HEALTHCHECK
```

## Phase 4

```text
GitHub Actions
    ↓
Build Docker Image
    ↓
Push to Docker Hub
```

## Phase 5

```text
Docker Hub
    ↓
AWS EC2
    ↓
Docker Container
    ↓
FastAPI
```

## Phase 6

```text
GitHub Actions
    ↓
Amazon ECR
    ↓
Amazon ECS
    ↓
AWS Fargate
    ↓
Application Load Balancer
    ↓
FastAPI
```

---

# Phase 6 final outcome

In Phase 6, we extended the project from a manually managed Docker deployment on EC2 to a managed container deployment using Amazon ECS and AWS Fargate.

We used Amazon ECR to store the application image, configured an ECS service to maintain the desired task count, and used an Application Load Balancer to expose the application through a DNS endpoint.

The phase demonstrates practical experience with:

- Container image registries
- AWS IAM
- ECS task definitions and services
- Fargate container execution
- VPC networking and security groups
- ALB listeners and target groups
- Health checks
- GitHub Actions image publishing
- Deployment verification and troubleshooting

The application was verified through the ALB, including the root endpoint and FastAPI documentation.

This completes the planned six-phase scope of the project.




This project is intended for learning and portfolio purposes.
