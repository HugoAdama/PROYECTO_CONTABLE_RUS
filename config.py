import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)


class Config:
    """Configuración base del proyecto."""

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DATA_DIR / 'rus.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = DATA_DIR / "uploads"

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

    LIMITE_RUS = int(os.getenv("LIMITE_RUS", 8000))
    IMPUESTO_NORMAL = float(os.getenv("IMPUESTO_NORMAL", 20))
    IMPUESTO_ALERTA = float(os.getenv("IMPUESTO_ALERTA", 50))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = False