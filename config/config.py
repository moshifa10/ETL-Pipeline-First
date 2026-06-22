from dotenv import load_dotenv
import os
from sqlalchemy.orm import relationship

load_dotenv()

GROK= os.getenv(key="GROQ_API_KEY")