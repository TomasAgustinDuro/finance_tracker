"""Capa de exportación a archivos de texto.

Genera reportes TXT a partir del historial de gastos.
No contiene lógica de negocio propia — delega cálculos a analytics.py.
"""

from src.analytics import calculate_summary_by_category
from src.validator import validate_category
import streamlit as st

GENERAL_REPORT_FILE = "resumen_general.txt"
DETAILED_REPORT_FILE = "resumen_detallado.txt"


def export_general_report(data: list) -> str | None :
    """Exporta un resumen de gastos totales por categoría a resumen_general.txt.

    Genera o sobreescribe el archivo con el total por categoría y el gran total acumulado.
    Si no hay datos, imprime un aviso y no escribe el archivo.

    Args:
        data (list[dict]): Lista de gastos con campos 'category' y 'value'.

    Returns:
        None
    """

    summary = calculate_summary_by_category(data)

    if not summary:
        st.warning("No hay información para escribir")
        return

    total_value = 0

    lineas_reporte=[]

    for category, value in summary.items():
        normalized_category = validate_category(category)
        total_value += value
        lineas_reporte.append(f"{normalized_category} : {value}")

    lineas_reporte.append(f"\nTotal Gastado {total_value}")

    contenido_txt = "\n".join(lineas_reporte)

    return contenido_txt

def export_detailed_report(data: list) -> None:
    """Exporta el historial completo de gastos con fecha a resumen_detalado.txt.

    Genera o sobreescribe el archivo con una línea por gasto en formato:
    'FECHA_ISO | CATEGORIA : MONTO'

    Args:
        data (list[dict]): Lista de gastos con campos 'date', 'category' y 'value'.

    Returns:
        None
    """

    lineas_reporte = []

    for item in data:
        category = item["category"]
        value = item["value"]
        date = item["date"]
        normalized_category = validate_category(category)
        lineas_reporte.append(f"\n{date} | {normalized_category} : {value}\n")
    
        contenido_txt = "\n".join(lineas_reporte)

    return contenido_txt

