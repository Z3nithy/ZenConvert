from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import CORS_ORIGINS
from routes import conversoes_router
import uvicorn

app = FastAPI(title="ZenConvert API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(conversoes_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)