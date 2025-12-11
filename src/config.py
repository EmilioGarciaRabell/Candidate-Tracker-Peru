import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    
    FRONTEND_ORIGINS = [
        os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000")
    ]

    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    RATE_LIMIT_DEFAULT = os.environ.get("RATE_LIMIT_DEFAULT", "200 per hour")
    RATE_LIMIT_STORAGE_URL = os.environ.get("RATE_LIMIT_STORAGE_URL", "memory://")