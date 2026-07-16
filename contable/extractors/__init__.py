"""Extractores de documentos de Contable RUS."""

from contable.extractors.base_extractor import BaseExtractor
from contable.extractors.boleta_extractor import BoletaExtractor
from contable.extractors.detector_extractor import DetectorExtractor
from contable.extractors.factura_extractor import FacturaExtractor
from contable.extractors.percepcion_extractor import PercepcionExtractor


__all__ = [
    "BaseExtractor",
    "BoletaExtractor",
    "DetectorExtractor",
    "FacturaExtractor",
    "PercepcionExtractor",
]
