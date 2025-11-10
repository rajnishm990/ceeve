import os 
from dotenv import load_dotenv 

load_dotenv()

class Settings:
    PROJECT_NAME : str = "CeeVee"
    DEBUG : bool = os.getenv("DEBUG", "True").lower() == "true"

    #db 
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg2://resumehub:resumehub@localhost:5432/resumehub"
    )

    # Redis (for caching / background tasks)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # JWT Config
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretjwtkey")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRY_MINUTES: int = int(os.getenv("JWT_EXPIRY_MINUTES", "60"))

    # AWS S3 / File storage
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "")

    # Misc
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")


settings = Settings()
