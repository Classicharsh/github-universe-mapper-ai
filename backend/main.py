from fastapi import FastAPI

app = FastAPI(
    title="GitHub Universe Mapper AI",
    description="AI-powered technology trend analytics platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "GitHub Universe Mapper AI backend is running",
        "status": "success"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }