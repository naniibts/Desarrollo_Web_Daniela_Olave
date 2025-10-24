from flask import Flask, flash, request, render_template, redirect, url_for, jsonify
import sqlite3
from utils.validations import *
from database import db 
from werkzeug.utils import secure_filename
from database.db import existencia_comuna, get_regiones_y_comunas, agregar_redes_contacto, agregar_fotos ,contar_avisos, get_aviso_por_id, get_last_avisos
from database.db import agregar_aviso as db_agregar_aviso
from database.db import listar_avisos as db_listar_avisos
from datetime import datetime
import hashlib
import filetype
import os

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

app.secret_key = "s3cr3t_k3y_adopcion_2025"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# --- Portada ---
@app.route("/", methods=["GET"])
def index():
    avisos = get_last_avisos(limit=5)
    return render_template("index.html", avisos=avisos)

# --- Agregar aviso de adopción ---
@app.route("/agregar_aviso", methods=["GET", "POST"])
def agregar_aviso():
    if request.method == "GET":
        regiones = get_regiones_y_comunas()
        return render_template("aviso.html", regiones_con_comunas=regiones)
    
    elif request.method == "POST":
        errores = []

        try:
            comuna_id = int(request.form.get("select-comuna", 0))
        except (ValueError, TypeError):
            errores.append("Comuna inválida.")
            comuna_id = None

        sector = request.form.get("sector", "").strip()
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        redes = request.form.getlist("redes_contacto")  # lista de checkboxes
        red_id = request.form.get("red-id", "").strip()

        tipo_mascota = request.form.get("select-tipo", "").strip()
        try:
            cantidad = int(request.form.get("cantidad", 0))
        except (ValueError, TypeError):
            errores.append("Cantidad debe ser un número entero.")
            cantidad = None

        try:
            edad = int(request.form.get("edad", 0))
        except (ValueError, TypeError):
            errores.append("Edad debe ser un número entero.")
            edad = None 

        unidad_edad = request.form.get("select-medida", "").strip()
        fecha_entrega_str = request.form.get("fecha", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        fotos = request.files.getlist("fotos[]")  

        # Validaciones
        if not comuna_id or not existencia_comuna(comuna_id):
            errores.append("Debe seleccionar una comuna válida.")

        if len(nombre) < 3 or len(nombre) > 200:
            errores.append("Nombre debe tener entre 3 y 200 caracteres.")

        if not email or "@" not in email or len(email) < 15 or len(email) > 100:
            errores.append("Email inválido (15-100 caracteres).")

        if tipo_mascota not in ["Perro", "Gato"]:
            errores.append("Tipo de mascota debe ser Perro o Gato.")

        if cantidad is not None and cantidad < 1:
            errores.append("Cantidad debe ser al menos 1.")

        if edad is not None and edad < 1:
            errores.append("Edad debe ser al menos 1.")

        if unidad_edad not in ["Meses", "Años"]:
            errores.append("Unidad debe ser 'Meses' o 'Años'.")

        if not fecha_entrega_str:
            errores.append("Fecha de entrega es obligatoria.")
        else:
            try:
                fecha_entrega = datetime.fromisoformat(fecha_entrega_str.replace("T", " "))
            except ValueError:
                errores.append("Formato de fecha inválido.")

        if not fotos or all(f.filename == '' for f in fotos):
            errores.append("Debe subir al menos una foto.")
        else:
            for f in fotos:
                if f.filename == '':
                    continue
                try:
                    kind = filetype.guess(f)
                    if not kind or kind.mime not in ["image/jpeg", "image/png"]:
                        errores.append("Solo se permiten imágenes JPG o PNG.")
                        break
                except Exception:
                    errores.append("Error al procesar una imagen.")
                    break

        if len(redes) > 5:
            errores.append("Máximo 5 redes de contacto.")


        # Redirección en caso de errores
        if errores:
            regiones = get_regiones_y_comunas()
            return render_template("aviso.html",errores=errores,regiones_con_comunas=regiones)

        # Guardar aviso en la base de datos
        try:
            aviso_id = db_agregar_aviso(
                comuna_id=comuna_id,
                sector=sector,
                nombre=nombre,
                email=email,
                celular=phone if phone else None,
                tipo_mascota=tipo_mascota,
                cantidad=cantidad,
                edad=edad,
                unidad_edad=unidad_edad,
                fecha_entrega=fecha_entrega,
                descripcion=descripcion
            )
        except Exception as e:
            flash("Error al guardar el aviso. Intente nuevamente.", "error")
            regiones = get_regiones_y_comunas()
            return render_template("aviso.html", regiones_con_comunas=regiones)
        
        # Guardar redes de contacto
        if phone:
            agregar_redes_contacto(aviso_id, "phone")
        for red in redes:
            if red in ["Instagram", "WhatsApp", "Telegram", "TikTok", "X", "Otra"]:
                agregar_redes_contacto(aviso_id, red)

        # Guardar fotos
        for foto in fotos:
            if foto.filename == '':
                continue
            try:
                kind = filetype.guess(foto)
                extension = kind.extension if kind else "jpg"
                filename = secure_filename(foto.filename)
                hash_name = hashlib.sha256(filename.encode()).hexdigest()
                img_filename = f"{hash_name}.{extension}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
                foto.save(filepath)
                agregar_fotos(aviso_id, img_filename)
            except Exception:
                continue

        flash("¡Aviso de adopción agregado!", "success")
        return redirect(url_for("index"))
    

@app.route("/avisos")
def listar_avisos():
    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    total = contar_avisos()
    total_pages = (total + per_page - 1) // per_page
    avisos = db_listar_avisos(limit=per_page, offset=offset)

    return render_template("listado.html",avisos=avisos,page=page,total_pages=total_pages)

@app.route("/aviso/<int:aviso_id>")
def ver_aviso(aviso_id):
    aviso = get_aviso_por_id(aviso_id)
    if not aviso:
        flash("Aviso no encontrado.", "error")
        return redirect(url_for("listar_avisos"))
    return render_template("index.html", aviso=aviso)


@app.route("/estadisticas")
def estadisticas():
   return render_template("estadisticas.html")


# === ESTADÍSTICAS ===
# Estos endpoints entregan datos JSON a estadisticas.js

@app.route("/api/estadisticas/dias")
def api_estadisticas_dias():
    """
    Devuelve la cantidad de avisos agregados por día.
    Ejemplo: [{ "dia": "2025-10-01", "cantidad": 3 }, ...]
    """
    conn = get_db_connection()
    data = conn.execute("""
        SELECT DATE(fecha_publicacion) AS dia, COUNT(*) AS cantidad
        FROM aviso
        GROUP BY dia
        ORDER BY dia
    """).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])


@app.route("/api/estadisticas/tipos")
def api_estadisticas_tipos():
    """
    Devuelve cantidad de avisos por tipo (Perro/Gato).
    Ejemplo: [{ "tipo": "Perro", "cantidad": 10 }, ...]
    """
    conn = get_db_connection()
    data = conn.execute("""
        SELECT tipo_mascota AS tipo, COUNT(*) AS cantidad
        FROM aviso
        GROUP BY tipo_mascota
    """).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])


@app.route("/api/estadisticas/meses")
def api_estadisticas_meses():
    """
    Devuelve avisos por mes y tipo de mascota.
    Ejemplo: [{ "mes": "10", "gatos": 5, "perros": 3 }, ...]
    """
    conn = get_db_connection()
    data = conn.execute("""
        SELECT strftime('%m', fecha_publicacion) AS mes,
               SUM(CASE WHEN tipo_mascota='Gato' THEN 1 ELSE 0 END) AS gatos,
               SUM(CASE WHEN tipo_mascota='Perro' THEN 1 ELSE 0 END) AS perros
        FROM aviso
        GROUP BY mes
        ORDER BY mes
    """).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])





if __name__ == "__main__":
    app.run(debug=True)