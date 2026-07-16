"""
Application Factory de Contable RUS.

Este módulo construye la aplicación Flask utilizando
una arquitectura modular basada en Factory Pattern.
"""

from flask import Flask

from config import DevelopmentConfig
from contable.extensions import db


def create_app(config_class=DevelopmentConfig):
    """
    Crea y configura una instancia de Flask.

    Parameters
    ----------
    config_class
        Clase de configuración a utilizar.

    Returns
    -------
    Flask
        Aplicación configurada.
    """

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.config.from_object(config_class)

    register_extensions(app)

    register_blueprints(app)

    register_filters(app)

    return app


def register_extensions(app):
    """
    Inicializa todas las extensiones Flask.
    """

    db.init_app(app)


def register_blueprints(app):
    """
    Registro de Blueprints.

    Sprint 2:
    Todavía no existen blueprints nuevos.
    """

    pass


def register_filters(app):
    """
    Registro de filtros Jinja2.
    """

    @app.template_filter("currency")
    def currency(value):

        if value is None:
            return "S/ 0.00"

        return f"S/ {float(value):,.2f}"