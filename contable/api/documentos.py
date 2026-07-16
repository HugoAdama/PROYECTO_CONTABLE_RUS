"""Rutas para carga y consulta de documentos."""

from datetime import datetime

from flask import current_app, jsonify, render_template, request
from werkzeug.utils import secure_filename

from contable.api import main_bp
from contable.services.documento_service import DocumentoService
from contable.services.ventas_service import VentasService
from src.database.models import Documento

ventas_service = VentasService()
documento_service = DocumentoService()


@main_bp.route("/subir")
def subir():
    return render_template("subir.html")


@main_bp.route("/ver_datos")
def ver_datos():
    try:
        now = datetime.now()
        latest = Documento.query.order_by(Documento.fecha_emision.desc()).first()
        default_year = latest.fecha_emision.year if latest else now.year
        default_month = latest.fecha_emision.month if latest else now.month
        year = request.args.get("year", type=int, default=default_year)
        month = request.args.get("month", type=int, default=default_month)
        tipo = request.args.get("tipo", default="")
        documentos = ventas_service.get_documentos_mes(year, month)
        years = sorted({d.fecha_emision.year for d in Documento.query.all()}, reverse=True) or [now.year]
        months = [(1,"Enero"),(2,"Febrero"),(3,"Marzo"),(4,"Abril"),(5,"Mayo"),(6,"Junio"),(7,"Julio"),(8,"Agosto"),(9,"Septiembre"),(10,"Octubre"),(11,"Noviembre"),(12,"Diciembre")]
        return render_template(
            "ver_datos.html", documentos=documentos, resumen=ventas_service.get_resumen_mensual(year, month),
            year=year, month=month, tipo=tipo, years=years, months=months,
        )
    except Exception as exc:
        return render_template("ver_datos.html", error=str(exc))


@main_bp.route("/api/upload", methods=["POST"])
def api_upload():
    try:
        if "file" not in request.files:
            return jsonify({"success": False, "message": "No se seleccionó archivo"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"success": False, "message": "Nombre vacío"}), 400
        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"success": False, "message": "Solo PDFs"}), 400

        filename = secure_filename(file.filename)
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        file_path = upload_dir / filename
        counter = 1
        original = file_path
        while file_path.exists():
            file_path = upload_dir / f"{original.stem}_{counter}{original.suffix}"
            counter += 1
        file.save(str(file_path))
        return jsonify(documento_service.procesar_archivo(file_path))
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500


@main_bp.route("/api/documentos", methods=["GET"])
def api_documentos():
    try:
        tipo = request.args.get("tipo")
        fecha_desde = request.args.get("fecha_desde")
        fecha_hasta = request.args.get("fecha_hasta")
        query = Documento.query
        if tipo:
            query = query.filter_by(tipo=tipo)
        if fecha_desde:
            query = query.filter(Documento.fecha_emision >= fecha_desde)
        if fecha_hasta:
            query = query.filter(Documento.fecha_emision <= fecha_hasta)
        documentos = query.order_by(Documento.fecha_emision.desc()).limit(100).all()
        return jsonify({"success": True, "documentos": [doc.to_dict() for doc in documentos]})
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500
