"""
DTLab: Network Device Management API

This application serves as a backend to manage network devices (routers/switches).

Usage with `uv` (Local development):
1. Ensure `uv` is installed: https://docs.astral.sh/uv/
2. Sync dependencies: uv sync
3. Run the app:
   uv run flask --app app.py run --port 5000
"""

import os
from flask import Flask
from dotenv import load_dotenv

# Local imports
from routers import router_blueprint
from switches import switches_blueprint
from models import db

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database Configuration
# WARNING: In production, never expose raw DB credentials.
db_uri = os.getenv("DB_URI", "postgresql://user:__pass__@localhost/db")

# For local testing, you might need to set the password manually if
# the docker secret path doesn't exist
secret_path = "/run/secrets/postgres_password"
try:
    with open(secret_path, "r") as f:
        password = f.readline().strip()
        db_uri = db_uri.replace("__pass__", password)
except FileNotFoundError:
    # Fallback to local dev password
    db_uri = db_uri.replace("__pass__", os.getenv("DB_PASSWORD", "password"))

app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

# Initialize database
db.init_app(app)

# Create models within the application context
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(router_blueprint, url_prefix="/routers")
app.register_blueprint(switches_blueprint, url_prefix="/switches")


@app.route("/", methods=["GET"])
def test() -> str:
    return "DTLab API is up and running!"
