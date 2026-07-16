import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=debug
    )