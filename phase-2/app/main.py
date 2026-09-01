from fastapi import FastAPI

app = FastAPI(
    title="Docker Mastery API",
    description="FastAPI application for learning Docker",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Docker Mastery Project"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/info")
def info():
    return {
        "app": "Docker Mastery",
        "version": "1.0.0",
        "environment": "development"
    }
