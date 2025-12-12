
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv
load_dotenv()
cors = CORS()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[os.environ.get("RATE_LIMIT_DEFAULT", "200 per hour")],
    storage_uri=os.environ.get("RATE_LIMIT_STORAGE_URL", "memory://"),
)