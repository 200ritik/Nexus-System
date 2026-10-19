from dotenv import load_dotenv
import os

SECRET_KEY = os.environ["JWT_SECRET_KEY"]

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30