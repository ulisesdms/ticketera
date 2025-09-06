from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from datetime import datetime
import os
from typing import Optional

load_dotenv()
def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

DB_HOST = get_env("DB_HOST", "localhost")
DB_PORT = get_env("DB_PORT", "3306")
DB_USER = get_env("DB_USER", "root")
DB_PASSWORD = get_env("DB_PASSWORD", "")
DB_NAME = get_env("DB_NAME", "pedidos_app")

APP_HOST = get_env("APP_HOST", "0.0.0.0")
APP_PORT = int(get_env("APP_PORT", "5000"))

def build_db_url(include_db: bool = True) -> str:
    base = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    return f"{base}/{DB_NAME}?charset=utf8mb4" if include_db else f"{base}/?charset=utf8mb4"



# Definimos el Blueprint para usuarios
usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

@usuarios_bp.route("", methods=["GET"])
def listar_usuarios():
    """
    GET /usuarios
    Lista usuarios desde la tabla 'usuarios' (id, nombre, email).
    """
    try:
        with get_db() as conn:
            result = conn.execute(text("SELECT id, nombre, email FROM usuarios ORDER BY id"))
            rows = [dict(row._mapping) for row in result]
            return jsonify(rows), 200
    except SQLAlchemyError as e:
        # Si la tabla no existe u otro error de SQL, devolvemos detalle
        return jsonify({
            "error": "DB query failed",
            "details": str(getattr(e, "orig", e))
        }), 500

@usuarios_bp.route("/ping", methods=["GET"])
def ping_usuarios():
    """
    GET /usuarios/ping
    Endpoint simple para verificar que el blueprint esté montado.
    """
    return jsonify({"status": "ok"}), 200


from flask import Flask

from db import APP_HOST, APP_PORT, ping_db
from routes.usuarios import usuarios_bp

# Si ya tienes tickets_bp en routes/tickets.py, lo importamos y registramos
try:
    from routes.tickets import tickets_bp
except Exception:
    tickets_bp = None

def create_app() -> Flask:
    app = Flask(__name__)

    # Registrar blueprints
    app.register_blueprint(usuarios_bp)
    if tickets_bp is not None:
        app.register_blueprint(tickets_bp)

    # Ruta de salud opcional
    @app.get("/health")
    def health():
        return {"ok": True, "db": ping_db()}

    return app

app = create_app()

if __name__ == "__main__":
    # Ejecuta la app con host/port definidos en variables de entorno
    app.run(host=APP_HOST, port=APP_PORT, debug=True)
