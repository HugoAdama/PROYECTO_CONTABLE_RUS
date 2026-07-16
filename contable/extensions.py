"""
Inicialización de extensiones Flask.

Este módulo solamente crea las instancias.

Nunca debe importar modelos ni blueprints.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()