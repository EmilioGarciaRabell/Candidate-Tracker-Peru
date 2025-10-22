import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
