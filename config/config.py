from dotenv import load_dotenv
import os

load_dotenv()

GROK= os.getenv(key="GROQ_API_KEY")

DATABASE_URL = "sqlite:///database/sales.db"