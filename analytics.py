"""Capa de lógica de negocio para análisis y cálculos sobre gastos.

Todas las funciones son puras: reciben datos como parámetro y retornan
resultados sin modificar estado global ni acceder a archivos.
"""

from datetime import datetime, timedelta

def calculate_expense_percentage(data):
    """Calcula el porcentaje que representa cada categoría sobre el total gastado.

    Args:
        data (list[dict]): Lista de gastos con campos 'category' y 'value'.

    Returns:
        dict[str, float]: Diccionario {categoria: porcentaje}. Los valores suman 100.
            Retorna dict vacío si la lista está vacía.
    """
    total_value = 0

    if len(data) == 0:
        return {}

    summary = {}

    for item in data:
        cat = item["category"]
        val = item["value"]
        total_value += item['value']
        summary[cat] = summary.get(cat, 0) + val

    percentages = {}

    for category, value in summary.items():
        percentages[category] = (value / total_value) * 100

    return percentages

def get_week_expenses(data):
    """Retorna los gastos registrados en los últimos 7 días, ordenados del más reciente al más antiguo.

    Args:
        data (list[dict]): Lista de gastos con campo 'date' en formato ISO 8601.

    Returns:
        list[dict]: Gastos dentro de la ventana de 7 días, ordenados por fecha descendente.
            Retorna lista vacía si no hay gastos en ese período.
    """
    if len(data) == 0:
        return {}

    today = datetime.now()
    week = today - timedelta(days=7)

    last_expenses = [
        last
        for last in data
        if week <= datetime.fromisoformat(last["date"]) <= today
    ]

    if len(last_expenses) == 0:
        print("No hubo gastos los ultimos 7 dias")

    sorted_expenses = sorted(last_expenses, key=lambda item: item["date"], reverse=True)

    return sorted_expenses

def get_top_expense_day(data):
    """Identifica el día con mayor gasto acumulado en todo el historial.

    Agrupa los gastos por fecha (YYYY-MM-DD) y retorna el día cuya suma es mayor.

    Args:
        data (list[dict]): Lista de gastos con campos 'date' y 'value'.

    Returns:
        dict: Diccionario con claves 'date' (str, formato YYYY-MM-DD) y 'value' (int).
            Retorna dict vacío si la lista está vacía.
    """
    if not data:
        return {}

    more_expenses = {}

    for item in data:
        more_expenses[item["date"][:10]] = (
            more_expenses.get(item["date"][:10], 0) + item["value"]
        )

    max_date = max(more_expenses, key=more_expenses.get)
    max_value = more_expenses[max_date]

    return {"date": max_date, "value": max_value}

def calculate_summary_by_category(data):
    """Calcula el total gastado agrupado por categoría.

    Args:
        data (list[dict]): Lista de gastos con campos 'category' y 'value'.

    Returns:
        dict[str, int]: Diccionario {categoria: total_gastado}.
            Retorna dict vacío si la lista está vacía.
    """
    if not data:
        return{}

    summary = {}
    for item in data:
        summary[item["category"]] = summary.get(item["category"], 0) + item["value"]

    return summary

# Helper
def calculate_daily_average(data):
    """Calcula el promedio diario de gasto para los últimos 7 días.

    Suma todos los gastos de la última semana y divide por 7, independientemente
    de cuántos días tuvieron actividad real.

    Args:
        data (list[dict]): Lista completa de gastos del historial.

    Returns:
        float: Promedio diario de los últimos 7 días. Retorna 0 si no hay gastos en ese período.
    """
    last_week = get_week_expenses(data)
    total_week = 0

    if not last_week:
        return 0

    for expense_value in last_week:
        total_week += expense_value["value"]

    return total_week / 7

# Helper
def calculate_historical_daily_average(data):
    """Calcula el promedio diario de gasto a lo largo de todo el historial.

    Divide el total gastado entre la cantidad de días únicos con al menos un gasto registrado,
    ignorando los días sin actividad.

    Args:
        data (list[dict]): Lista completa de gastos del historial.

    Returns:
        float: Promedio de gasto por día activo. Retorna 0 si no hay datos.
    """
    days_with_expense = []
    value_expense = 0

    if not data:
        return 0

    for expense_date in data:
        days_with_expense.append(expense_date["date"][:10])

    unique_days = set(days_with_expense)

    for expense in data:
        value_expense += expense["value"]

    average = value_expense / len(unique_days)

    return average
