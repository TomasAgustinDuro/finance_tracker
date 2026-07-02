"""Capa de lógica de negocio para análisis y cálculos sobre gastos.

Todas las funciones son puras: reciben datos como parámetro y retornan
resultados sin modificar estado global ni acceder a archivos o servicios externos.
"""

from datetime import datetime, timedelta


def calculate_expense_percentage(data: list) -> dict:
    """Calcula el porcentaje que representa cada categoría sobre el total gastado.

    Agrupa los gastos por categoría, suma sus valores y calcula el peso
    relativo de cada una sobre el total. Los porcentajes retornados suman 100.

    Args:
        data (list[dict]): Lista de gastos con campos `category` (str) y `value` (float).

    Returns:
        dict[str, float]: Diccionario `{categoria: porcentaje}`.
            Retorna `{}` si `data` está vacía.
    """
    if not data:
        return {}

    total_value = 0
    summary = {}

    for item in data:
        item_category = item["category"]
        item_value = item["value"]
        total_value += item_value
        summary[item_category] = summary.get(item_category, 0) + item_value

    return {
        category: (value / total_value) * 100
        for category, value in summary.items()
    }


def get_week_expenses(data: list) -> list:
    """Retorna los gastos registrados en los últimos 7 días, ordenados por fecha ascendente.

    La ventana temporal se calcula dinámicamente respecto a `datetime.now()`,
    por lo que el resultado varía según el momento de ejecución.

    Args:
        data (list[dict]): Lista de gastos con campo `date` en formato ISO 8601.

    Returns:
        list[dict]: Gastos dentro de la ventana de 7 días, ordenados del más
            antiguo al más reciente. Retorna `[]` si no hay gastos en ese período
            o si `data` está vacía.
    """
    if not data:
        return []

    today = datetime.now()
    week_ago = today - timedelta(days=7)

    recent_expenses = [
        expense
        for expense in data
        if week_ago <= datetime.fromisoformat(expense["date"]) <= today
    ]

    if not recent_expenses:
        return []

    return sorted(recent_expenses, key=lambda expense: expense["date"])


def get_top_expense_day(data: list) -> dict:
    """Identifica el día con mayor gasto acumulado en todo el historial.

    Agrupa los gastos por fecha (truncada a `YYYY-MM-DD`) y retorna el día
    cuya suma es la más alta. En caso de empate, retorna el primero según
    el orden de iteración del diccionario interno (no determinístico).

    Args:
        data (list[dict]): Lista de gastos con campos `date` (str ISO 8601)
            y `value` (float).

    Returns:
        dict: Diccionario con claves `date` (str, formato `YYYY-MM-DD`) y
            `value` (float, total acumulado ese día).
            Retorna `{}` si `data` está vacía.
    """
    if not data:
        return {}

    daily_totals: dict[str, float] = {}

    for item in data:
        day_key = item["date"][:10]
        daily_totals[day_key] = daily_totals.get(day_key, 0) + item["value"]

    max_date = max(daily_totals, key=daily_totals.get)

    return {"date": max_date, "value": daily_totals[max_date]}


def calculate_summary_by_category(data: list) -> dict:
    """Calcula el total gastado agrupado por categoría.

    Itera sobre todos los gastos y acumula los valores por categoría
    usando el nombre exacto como clave (sensible a mayúsculas).

    Args:
        data (list[dict]): Lista de gastos con campos `category` (str) y `value` (float).

    Returns:
        dict[str, float]: Diccionario `{categoria: total_gastado}`.
            Retorna `{}` si `data` está vacía.
    """
    if not data:
        return {}

    summary: dict[str, float] = {}

    for item in data:
        summary[item["category"]] = summary.get(item["category"], 0) + item["value"]

    return summary
