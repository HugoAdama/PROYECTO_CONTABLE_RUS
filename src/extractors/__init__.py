"""Compatibilidad temporal con imports antiguos de extractores."""

from contable.extractors import (
    BaseExtractor,
    BoletaExtractor,
    DetectorExtractor,
    FacturaExtractor,
    PercepcionExtractor,
)


__all__ = [
    "BaseExtractor",
    "BoletaExtractor",
    "DetectorExtractor",
    "FacturaExtractor",
    "PercepcionExtractor",
]
