@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, email, rol FROM usuarios")
    return jsonify(cursor.fetchall())
