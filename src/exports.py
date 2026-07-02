"""Capa de exportación de reportes de gastos.

Genera strings formateados listos para descargarse como archivos TXT desde
la UI de Streamlit. No escribe archivos en disco ni accede al storage directamente.
Delega todos los cálculos a `analytics.py`.
"""

import logging
from datetime import datetime

import streamlit as st

from src.analytics import calculate_summary_by_category
from src.validator import validate_category


def export_general_report(data: list) -> str | None:
    """Genera un reporte de texto con el total gastado por categoría.

    Calcula el resumen por categoría usando `calculate_summary_by_category`,
    formatea cada línea como `"Categoria : total"` y agrega el gran total
    acumulado al final. Las categorías con nombre inválido se omiten con un
    warning en el log (no interrumpen la generación del reporte).

    Args:
        data (list[dict]): Lista de gastos con campos `category` (str) y `value` (float).

    Returns:
        str | None: String multilínea con el reporte listo para descargarse.
            Retorna `None` si `data` está vacía o si el resumen no tiene contenido,
            y muestra un `st.warning` en la UI.
    """
    summary = calculate_summary_by_category(data)

    if not summary:
        st.warning("No hay información para escribir")
        return None

    total_value = 0
    report_lines = []

    for category, value in summary.items():
        normalized_category = validate_category(category)
        if not normalized_category:
            logging.warning("Categoría inválida ignorada en reporte general: '%s'", category)
            continue
        total_value += value
        report_lines.append(f"{normalized_category} : {value}")

    report_lines.append(f"Total Gastado {total_value}")

    return "\n".join(report_lines)


def export_detailed_report(data: list) -> str:
    """Genera un reporte de texto con el detalle completo de cada gasto.

    Formatea cada gasto como `"DD-MM-YYYY HH:MM | Categoria : valor"`.
    Las fechas en formato ISO 8601 se convierten al formato legible; si la
    fecha tiene un formato inesperado, se usa el string original como fallback.
    Las categorías con nombre inválido se omiten con un warning en el log.

    Args:
        data (list[dict]): Lista de gastos con campos `date` (str ISO 8601),
            `category` (str) y `value` (float).

    Returns:
        str: String multilínea con una línea por gasto. Retorna `""` si `data`
            está vacía.
    """
    report_lines = []

    for item in data:
        category = item["category"]
        value = item["value"]
        date_str = item["date"]

        normalized_category = validate_category(category)
        if not normalized_category:
            logging.warning("Categoría inválida ignorada en reporte detallado: '%s'", category)
            continue

        try:
            date_obj = datetime.fromisoformat(date_str)
            date_formatted = date_obj.strftime("%d-%m-%Y %H:%M")
        except (ValueError, TypeError):
            date_formatted = date_str

        report_lines.append(f"{date_formatted} | {normalized_category} : {value}")

    return "\n".join(report_lines)
