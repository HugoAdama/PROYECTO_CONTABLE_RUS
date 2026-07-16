"""Rutas de configuración."""

from flask import jsonify, render_template, request

from contable.api import main_bp
from src.database.models import Configuracion, Historial


@main_bp.route("/configuracion")
def configuracion():
    try:
        config = {
            "nombre_negocio": Configuracion.get("nombre_negocio", "Maria Boutique"),
            "color_primario": Configuracion.get("color_primario", "#4A90D9"),
            "limite_rus": Configuracion.get("limite_rus", "8000"),
            "impuesto_normal": Configuracion.get("impuesto_normal", "20"),
            "impuesto_alerta": Configuracion.get("impuesto_alerta", "50"),
        }
        return render_template("configuracion.html", config=config)
    except Exception as exc:
        return render_template("configuracion.html", error=str(exc))


@main_bp.route("/api/config", methods=["POST"])
def api_config():
    try:
        data = request.get_json() or {}
        allowed = {"nombre_negocio", "color_primario", "limite_rus", "impuesto_normal", "impuesto_alerta"}
        for key, value in data.items():
            if key in allowed:
                Configuracion.set(key, value)
        Historial.registrar("config", "Configuración actualizada")
        return jsonify({"success": True, "message": "Configuración guardada"})
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500
