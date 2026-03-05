import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

MAX_CODE_LENGTH: int = 8000
SEVERITY_LEVELS: list[str] = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]

SUPPORTED_LANGUAGES: list[str] = [
    "python", "javascript", "typescript", "java",
    "c", "c++", "go", "rust", "ruby", "php", "unknown"
]

REPORTS_DIR: str = "output_reports"