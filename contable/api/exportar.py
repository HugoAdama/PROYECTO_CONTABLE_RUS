"""Rutas de exportación."""

from datetime import datetime

from flask import send_file, request

from contable.api import main_bp
from contable.services.export_service import ExportService


@main_bp.route("/exportar")
def exportar():
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    output = ExportService.exportar_reporte_completo(mes=month, anio=year)
    filename = f"reporte_rus_{datetime.now():%Y%m%d_%H%M}.xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
