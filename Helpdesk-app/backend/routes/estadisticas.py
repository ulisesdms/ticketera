@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Total tickets
    cursor.execute("SELECT COUNT(*) AS total FROM tickets")
    total = cursor.fetchone()["total"]

    # Abiertos
    cursor.execute("SELECT COUNT(*) AS abiertos FROM tickets WHERE estado='abierto'")
    abiertos = cursor.fetchone()["abiertos"]

    # Pendientes
    cursor.execute("SELECT COUNT(*) AS pendientes FROM tickets WHERE estado='pendiente'")
    pendientes = cursor.fetchone()["pendientes"]

    # Cerrados
    cursor.execute("SELECT COUNT(*) AS cerrados FROM tickets WHERE estado='cerrado'")
    cerrados = cursor.fetchone()["cerrados"]

    # Prioridades
    cursor.execute("SELECT prioridad, COUNT(*) as cantidad FROM tickets GROUP BY prioridad")
    prioridades = cursor.fetchall()

    # Sectores
    cursor.execute("SELECT sector, COUNT(*) as cantidad FROM tickets GROUP BY sector")
    sectores = cursor.fetchall()

    # Sub-equipos
    cursor.execute("SELECT sub_equipo, COUNT(*) as cantidad FROM tickets GROUP BY sub_equipo")
    subequipos = cursor.fetchall()

    return jsonify({
        "total": total,
        "abiertos": abiertos,
        "pendientes": pendientes,
        "cerrados": cerrados,
        "prioridades": prioridades,
        "sectores": sectores,
        "subequipos": subequipos
    })
