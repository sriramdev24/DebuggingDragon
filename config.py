import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "skillswap-dna-secret-key-2026")
    MONGO_URI = os.getenv("MONGO_URI", "")
    DB_NAME = os.getenv("DB_NAME", "skillswap_dna")
    PORT = int(os.getenv("PORT", 5001))
