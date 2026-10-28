import os
from dotenv import load_dotenv

load_dotenv()

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "25"))
CORS_ORIGINS = [
    origem.strip()
    for origem in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if origem.strip()
]