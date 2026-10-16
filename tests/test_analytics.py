"""Tests unitarios para analytics.py.

Cubre el happy path y casos borde de todas las funciones de análisis.
Las funciones son puras (sin I/O ni estado global), por lo que no se necesitan mocks.
"""

import unittest
from datetime import datetime, timedelta

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.analytics import (
    calculate_expense_percentage,
    get_week_expenses,
    get_top_expense_day,
    calculate_summary_by_category,
)


class TestCalculateExpensePercentage(unittest.TestCase):
    """Tests para calculate_expense_percentage."""

    static_data = [
        {"id": "abc123", "category": "Comida",     "value": 500, "date": "2020-02-20T10:00:00"},
        {"id": "def456", "category": "Transporte", "value": 300, "date": "2020-02-21T15:30:00"},
        {"id": "ghi789", "category": "Comida",     "value": 200, "date": "2020-02-22T18:45:00"},
    ]

    def test_percentages_are_correct_for_two_categories(self):
        """Verifica que Comida=70% y Transporte=30% sobre un total de 1000."""
        result = calculate_expense_percentage(self.static_data)
        self.assertAlmostEqual(result["Comida"],     70.0, places=1)
        self.assertAlmostEqual(result["Transporte"], 30.0, places=1)

    def test_percentages_sum_to_100(self):
        """Verifica que los porcentajes de todas las categorías suman exactamente 100."""
        result = calculate_expense_percentage(self.static_data)
        total = sum(result.values())
        self.assertAlmostEqual(total, 100.0, places=5)

    def test_single_category_returns_100_percent(self):
        """Verifica que con una sola categoría el porcentaje es 100%."""
        single = [{"id": "x", "category": "Comida", "value": 250, "date": "2020-01-01T00:00:00"}]
        result = calculate_expense_percentage(single)
        self.assertAlmostEqual(result["Comida"], 100.0, places=1)

    def test_empty_data_returns_empty_dict(self):
        """Verifica que con lista vacía retorna dict vacío."""
        self.assertEqual(calculate_expense_percentage([]), {})


class TestGetWeekExpenses(unittest.TestCase):
    """Tests para get_week_expenses."""

    def _make_recent_expense(self, days_ago: int, expense_id: str, value: int = 100) -> dict:
        """Genera un gasto con fecha relativa a hoy para aislar tests de la ventana temporal."""
        date_str = (datetime.now() - timedelta(days=days_ago)).isoformat()
        return {"id": expense_id, "category": "Comida", "value": value, "date": date_str}

    def test_returns_only_expenses_within_last_7_days(self):
        """Verifica que gastos de hace más de 7 días quedan excluidos."""
        recent  = self._make_recent_expense(days_ago=3, expense_id="recent")
        old     = {"id": "old", "category": "Comida", "value": 999, "date": "2020-01-01T10:00:00"}
        result  = get_week_expenses([recent, old])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "recent")

    def test_returns_all_expenses_within_window(self):
        """Verifica que todos los gastos dentro de los 7 días se incluyen."""
        expenses = [self._make_recent_expense(days_ago=i, expense_id=str(i)) for i in range(1, 4)]
        result   = get_week_expenses(expenses)
        self.assertEqual(len(result), 3)

    def test_results_are_sorted_ascending_by_date(self):
        """Verifica que los resultados vienen ordenados del más antiguo al más reciente."""
        older  = self._make_recent_expense(days_ago=5, expense_id="older")
        newer  = self._make_recent_expense(days_ago=1, expense_id="newer")
        result = get_week_expenses([older, newer])
        self.assertEqual(result[0]["id"], "older")
        self.assertEqual(result[-1]["id"], "newer")

    def test_empty_data_returns_empty_list(self):
        """Verifica que con lista vacía retorna lista vacía."""
        self.assertEqual(get_week_expenses([]), [])

    def test_all_old_expenses_returns_empty_list(self):
        """Verifica que si todos los gastos son viejos retorna lista vacía."""
        old_data = [
            {"id": "a", "category": "Comida", "value": 100, "date": "2019-01-01T10:00:00"},
            {"id": "b", "category": "Ocio",   "value": 200, "date": "2018-06-15T08:00:00"},
        ]
        self.assertEqual(get_week_expenses(old_data), [])


class TestGetTopExpenseDay(unittest.TestCase):
    """Tests para get_top_expense_day."""

    static_data = [
        {"id": "a", "category": "Comida",     "value": 500, "date": "2020-02-20T10:00:00"},
        {"id": "b", "category": "Transporte", "value": 300, "date": "2020-02-21T15:30:00"},
        {"id": "c", "category": "Comida",     "value": 200, "date": "2020-02-22T18:45:00"},
    ]

    def test_identifies_day_with_highest_single_expense(self):
        """Verifica que se identifica correctamente el día con mayor gasto individual."""
        result = get_top_expense_day(self.static_data)
        self.assertEqual(result["date"],  "2020-02-20")
        self.assertEqual(result["value"], 500)

    def test_accumulates_multiple_expenses_on_same_day(self):
        """Verifica que acumula correctamente varios gastos del mismo día."""
        same_day_data = [
            {"id": "a", "category": "Comida", "value": 300, "date": "2026-03-01T09:00:00"},
            {"id": "b", "category": "Ocio",   "value": 400, "date": "2026-03-01T20:00:00"},
            {"id": "c", "category": "Comida", "value": 100, "date": "2026-03-02T10:00:00"},
        ]
        result = get_top_expense_day(same_day_data)
        self.assertEqual(result["date"],  "2026-03-01")
        self.assertEqual(result["value"], 700)

    def test_single_entry_returns_that_entry(self):
        """Verifica que con un solo gasto ese día es el récord."""
        single = [{"id": "x", "category": "Salud", "value": 150, "date": "2025-05-10T12:00:00"}]
        result = get_top_expense_day(single)
        self.assertEqual(result["date"],  "2025-05-10")
        self.assertEqual(result["value"], 150)

    def test_empty_data_returns_empty_dict(self):
        """Verifica que con lista vacía retorna dict vacío."""
        self.assertEqual(get_top_expense_day([]), {})


class TestCalculateSummaryByCategory(unittest.TestCase):
    """Tests para calculate_summary_by_category."""

    static_data = [
        {"id": "abc123", "category": "Comida",     "value": 500, "date": "2020-02-20T10:00:00"},
        {"id": "def456", "category": "Transporte", "value": 300, "date": "2020-02-21T15:30:00"},
        {"id": "ghi789", "category": "Comida",     "value": 200, "date": "2020-02-22T18:45:00"},
    ]

    def test_accumulates_values_per_category(self):
        """Verifica que los totales por categoría son correctos."""
        result = calculate_summary_by_category(self.static_data)
        self.assertEqual(result["Comida"],     700)
        self.assertEqual(result["Transporte"], 300)

    def test_returns_all_present_categories(self):
        """Verifica que el dict contiene exactamente las categorías presentes."""
        result = calculate_summary_by_category(self.static_data)
        self.assertSetEqual(set(result.keys()), {"Comida", "Transporte"})

    def test_single_entry_returns_single_category(self):
        """Verifica que con un solo gasto el resumen tiene una sola clave."""
        single = [{"id": "x", "category": "Salud", "value": 999, "date": "2025-01-01T00:00:00"}]
        result = calculate_summary_by_category(single)
        self.assertEqual(result, {"Salud": 999})

    def test_empty_data_returns_empty_dict(self):
        """Verifica que con lista vacía retorna dict vacío."""
        self.assertEqual(calculate_summary_by_category([]), {})
