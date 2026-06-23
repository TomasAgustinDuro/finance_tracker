"""Capa de exportación a archivos de texto.

Genera reportes TXT a partir del historial de gastos.
No contiene lógica de negocio propia — delega cálculos a analytics.py.
"""

from analytics import calculate_summary_by_category


def export_general_report(data):
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
        print('No hay información para escribir')

    total_value = 0

    with open("resumen_general.txt", "w") as f:
        for category, value in summary.items():
            normalized_category = category.strip()
            total_value += value
            f.write(f"\n{normalized_category} : {value}\n")
        f.write(f"\nTotal Gastado {total_value}")


def export_detailed_report(data):
    """Exporta el historial completo de gastos con fecha a resumen_detalado.txt.

    Genera o sobreescribe el archivo con una línea por gasto en formato:
    'FECHA_ISO | CATEGORIA : MONTO'

    Args:
        data (list[dict]): Lista de gastos con campos 'date', 'category' y 'value'.

    Returns:
        None
    """
    with open("resumen_detalado.txt", "w") as f:
        for item in data:
            category = item["category"]
            value = item["value"]
            date = item["date"]
            normalized_category = category.strip()
            f.write(f"\n{date} | {normalized_category} : {value}\n")
