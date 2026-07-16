"""Rutas de reportes."""

from datetime import datetime

from flask import render_template

from contable.api import main_bp
from contable.services.ventas_service import VentasService

ventas_service = VentasService()


@main_bp.route("/reportes")
def reportes():
    try:
        now = datetime.now()
        resumen = ventas_service.get_resumen_mensual(now.year, now.month)
        meses, ventas_meses, compras_meses = [], [], []
        for i in range(6):
            month = now.month - i
            year = now.year
            if month <= 0:
                month += 12
                year -= 1
            datos = ventas_service.get_resumen_mensual(year, month)
            meses.append(f"{year}-{month:02d}")
            ventas_meses.append(datos.get("ventas", 0))
            compras_meses.append(datos.get("compras", 0))
        return render_template(
            "reportes.html",
            resumen=resumen,
            meses=meses[::-1],
            ventas_meses=ventas_meses[::-1],
            compras_meses=compras_meses[::-1],
        )
    except Exception as exc:
        return render_template("reportes.html", error=str(exc))
