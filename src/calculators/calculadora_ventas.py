# src/calculators/calculadora_ventas.py
"""
Calculadora para gestionar ventas del mes
"""

from typing import List, Dict

class CalculadoraVentas:
    """Calculadora para gestionar ventas del mes"""
    
    def __init__(self, mes: int, año: int):
        self.mes = mes
        self.año = año
        self.boletas = []
    
    def cargar_boletas(self, boletas: List[Dict]):
        """Carga las boletas para calcular"""
        self.boletas = boletas
    
    def calcular_total_ventas(self) -> float:
        """Calcula el total de ventas"""
        return sum(b.get('monto_total', 0) for b in self.boletas)
    
    def contar_boletas(self) -> int:
        """Cuenta el número de boletas"""
        return len(self.boletas)
    
    def resumen_ventas(self) -> Dict:
        """Genera un resumen de las ventas del mes"""
        total = self.calcular_total_ventas()
        cantidad = self.contar_boletas()
        return {
            'total_ventas': total,
            'numero_boletas': cantidad,
            'promedio_por_boleta': total / cantidad if cantidad > 0 else 0,
            'detalle': self.boletas
        }