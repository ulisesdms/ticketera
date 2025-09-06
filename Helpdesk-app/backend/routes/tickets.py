from flask import Blueprint, request, jsonify
from db import get_db

tickets_bp = Blueprint("tickets", __name__)

@tickets_bp.route("/nuevo", methods=["POST"])
def nuevo_ticket():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO tickets (titulo, descripcion, usuario_id, sector, sub_equipo, tipo_tarea)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["titulo"],
        data["descripcion"],
        data.get("usuario_id"),
        data.get("sector"),
        data.get("sub_equipo"),
        data.get("tipo_tarea")
    ))
    db.commit()
    return jsonify({"message": "Ticket creado correctamente"}), 201

@tickets_bp.route("/", methods=["GET"])
def listar_tickets():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets ORDER BY fecha_creacion DESC")
    result = cursor.fetchall()
    return jsonify(result)
