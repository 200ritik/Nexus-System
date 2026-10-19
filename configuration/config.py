from dotenv import load_dotenv
from pathlib import Path
import os


# Find project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root
load_dotenv(BASE_DIR / ".env")


user_id = "temp0001"

# AWS configuration
access_key = os.getenv("ACCESS_KEY")
secret_access_key = os.getenv("SECRET_ACCESS_KEY")
bucket_name = os.getenv("BUCKET_NAME")
region = os.getenv("REGION_NAME")


# File validation configuration
MAX_SIZE_MB = 10
MAX_FILE = 1

ALLOWED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".jpg",
    ".png",
    ".jpeg"
]

FILE_SIGNATURES = {
    ".pdf": [b"%PDF-"],
    ".png": [b"\x89PNG\r\n\x1a\n"],
    ".jpg": [b"\xff\xd8\xff"],
    ".jpeg": [b"\xff\xd8\xff"],
}

# postgre sql configuration
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_database = os.getenv("POSTGRES_DATABASE")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")




# taviyl max_results during search 

TAVILY_MAX_RESULTS = 10