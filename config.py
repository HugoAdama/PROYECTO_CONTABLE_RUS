import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).parent.absolute()
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "data" / "rus.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_segura_para_doña_maria')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'uploads'
    BACKUP_FOLDER = BASE_DIR / 'data' / 'backups'
    LOG_FOLDER = BASE_DIR / 'logs'
    LIMITE_RUS = 8000
    IMPUESTO_NORMAL = 20.00
    IMPUESTO_ALERTA = 50.00

for folder in [Config.UPLOAD_FOLDER, Config.BACKUP_FOLDER, Config.LOG_FOLDER]:
    folder.mkdir(parents=True, exist_ok=True)
