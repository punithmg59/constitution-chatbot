import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # LLM Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Database Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "constitution")
    DB_USER = os.getenv("DB_USER", "959146")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "959146")
    
    # Database URL
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()