"""
Punto de entrada para servidores WSGI.

Ejemplos:

gunicorn wsgi:app

waitress-serve --call wsgi:create_app
"""

from contable import create_app

app = create_app()


if __name__ == "__main__":
    app.run()