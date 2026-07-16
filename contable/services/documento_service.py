"""Orquestador del flujo de carga de documentos financieros."""

import logging
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from contable.extractors import (
    BoletaExtractor,
    DetectorExtractor,
    FacturaExtractor,
    PercepcionExtractor,
)
from contable.extensions import db
from src.database.models import Documento, Historial

logger = logging.getLogger(__name__)


class DocumentoService:
    """Detecta, extrae, normaliza y persiste un PDF en una sola operación."""

    EXTRACTORES = {
        "factura": FacturaExtractor,
        "boleta": BoletaExtractor,
        "percepcion": PercepcionExtractor,
    }

    def __init__(self) -> None:
        self.detector = DetectorExtractor()

    def procesar_archivo(self, archivo: Path | str, tipo_seleccionado: Optional[str] = None) -> Dict[str, Any]:
        """Procesa un PDF y devuelve el contrato usado por ``/api/upload``."""
        ruta = Path(archivo)
        try:
            tipo = self._detectar_tipo(ruta, tipo_seleccionado)
            datos_extraidos = self._extraer(tipo, ruta)
            datos = self._normalizar(tipo, datos_extraidos, ruta)

            existente = Documento.query.filter_by(numero=datos["numero"]).first()
            if existente:
                return {
                    "success": False,
                    "message": f'Documento {datos["numero"]} ya existe',
                    "data": datos,
                }

            documento = Documento(**datos)
            db.session.add(documento)
            db.session.flush()
            Historial.registrar(
                "upload",
                f'Documento {datos["numero"]} ({tipo}) - S/{datos["monto_total"]:.2f}',
            )

            logger.info("Documento guardado: %s (%s)", datos["numero"], tipo)
            return {
                "success": True,
                "message": f'Documento {datos["numero"]} procesado correctamente',
                "data": documento.to_dict(),
            }
        except Exception as exc:
            db.session.rollback()
            logger.exception("Error procesando documento %s", ruta)
            return {
                "success": False,
                "message": f"Error al procesar: {exc}",
                "data": None,
            }

    def procesar_documento(
        self,
        archivo: Path | str,
        tipo_seleccionado: str = "automatico",
        mes_seleccionado: Optional[int] = None,
        anio_seleccionado: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Contrato compatible con consumidores anteriores del servicio."""
        tipo = None if tipo_seleccionado in {"", "automatico", "auto"} else tipo_seleccionado
        resultado = self.procesar_archivo(archivo, tipo)
        mensajes = [resultado["message"]]
        return resultado, mensajes

    def _detectar_tipo(self, ruta: Path, tipo_seleccionado: Optional[str]) -> str:
        if tipo_seleccionado:
            tipo = tipo_seleccionado.lower().strip()
        else:
            deteccion = self.detector.extraer(str(ruta))
            tipo = (deteccion or {}).get("tipo_detectado", "desconocido")

        if tipo not in self.EXTRACTORES:
            raise ValueError("No se pudo determinar el tipo de documento")
        return tipo

    def _extraer(self, tipo: str, ruta: Path) -> Dict[str, Any]:
        datos = self.EXTRACTORES[tipo]().extraer(str(ruta))
        if not datos:
            raise ValueError("El PDF no contiene datos legibles")
        return datos

    def _normalizar(self, tipo: str, datos: Dict[str, Any], ruta: Path) -> Dict[str, Any]:
        numero_keys = {
            "factura": "numero_factura",
            "boleta": "numero_boleta",
            "percepcion": "numero_comprobante",
        }
        numero = str(datos.get(numero_keys[tipo]) or datos.get("numero") or "").strip()
        if not numero or numero == "DESCONOCIDO":
            raise ValueError("No se pudo identificar el número del documento")

        monto = datos.get("monto_percibido") if tipo == "percepcion" else datos.get("total_pagar")
        if monto is None:
            monto = datos.get("monto", 0)
        monto = float(monto or 0)
        if monto <= 0:
            raise ValueError("No se pudo identificar un monto válido")

        fecha = self._parse_fecha(datos.get("fecha_emision"))
        nombre = datos.get("cliente") if tipo == "boleta" else datos.get("proveedor")
        percepcion = monto if tipo == "percepcion" else float(datos.get("percepcion", 0) or 0)

        return {
            "numero": numero,
            "tipo": tipo,
            "ruc_emisor": str(datos.get("ruc_proveedor") or ""),
            "ruc_cliente": str(datos.get("ruc_cliente") or ""),
            "nombre_cliente": str(nombre or ""),
            "fecha_emision": fecha,
            "monto_total": monto,
            "monto_base": float(datos.get("sub_total", 0) or 0),
            "percepcion": percepcion,
            "archivo_original": ruta.name,
            "documento_asociado": str(datos.get("documento_asociado") or ""),
            "ciclo": str(datos.get("ciclo") or ""),
        }

    @staticmethod
    def _parse_fecha(value: Any) -> date:
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if value:
            texto = str(value).strip()
            for formato in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(texto, formato).date()
                except ValueError:
                    continue
        raise ValueError("No se pudo identificar una fecha válida")

    def obtener_estadisticas(self, mes: int, anio: int) -> Dict[str, Any]:
        """Resume documentos del mes usando el modelo unificado vigente."""
        documentos = Documento.query.filter(
            db.extract("month", Documento.fecha_emision) == mes,
            db.extract("year", Documento.fecha_emision) == anio,
        ).all()
        return {
            "total_documentos": len(documentos),
            "facturas": sum(1 for item in documentos if item.tipo == "factura"),
            "boletas": sum(1 for item in documentos if item.tipo == "boleta"),
            "percepciones": sum(1 for item in documentos if item.tipo == "percepcion"),
            "monto_total": sum(float(item.monto_total) for item in documentos),
        }

    def close(self) -> None:
        """El servicio no mantiene recursos propios abiertos."""
