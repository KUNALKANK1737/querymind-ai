from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="QueryMind AI",
    description="LLM-powered natural language to SQL analytics platform",
    version="0.1.0",
)

app.include_router(router)