import unittest
from datetime import datetime, timedelta

from analytics import (
    calculate_expense_percentage,
    get_week_expenses,
    get_top_expense_day,
    calculate_summary_by_category,
    calculate_daily_average,
    calculate_historical_daily_average,
)


class testANALYTICS(unittest.TestCase):
    # Datos estáticos para tests que no dependen de la ventana temporal (7 días).
    # Fechas del pasado lejano: nunca caerán dentro de "última semana".
    static_data = [
        {
            "id": "abc123",
            "category": "Comida",
            "value": 500,
            "date": "2020-02-20T10:00:00",
        },
        {
            "id": "def456",
            "category": "Transporte",
            "value": 300,
            "date": "2020-02-21T15:30:00",
        },
        {
            "id": "ghi789",
            "category": "Comida",
            "value": 200,
            "date": "2020-02-22T18:45:00",
        },
    ]

    def _make_recent_data(self) -> list:
        """Genera datos con fechas dentro de los últimos 7 días para tests temporales."""
        today = datetime.now()
        return [
            {
                "id": "abc123",
                "category": "Comida",
                "value": 500,
                "date": (today - timedelta(days=6)).replace(hour=10, minute=0, second=0, microsecond=0).isoformat(),
            },
            {
                "id": "def456",
                "category": "Transporte",
                "value": 300,
                "date": (today - timedelta(days=5)).replace(hour=15, minute=30, second=0, microsecond=0).isoformat(),
            },
            {
                "id": "ghi789",
                "category": "Comida",
                "value": 200,
                "date": (today - timedelta(days=4)).replace(hour=18, minute=45, second=0, microsecond=0).isoformat(),
            },
        ]

    def test_calculate_expense_percentage(self):
        """Verifica que los porcentajes por categoría son correctos."""
        data = calculate_expense_percentage(self.static_data)

        self.assertAlmostEqual(data["Comida"], 70.0, places=1)
        self.assertAlmostEqual(data["Transporte"], 30.0, places=1)

    def test_get_week_expenses_returns_all_recent_entries(self):
        """Verifica que get_week_expenses retorna todos los gastos dentro de los últimos 7 días."""
        recent_data = self._make_recent_data()
        result = get_week_expenses(recent_data)
        self.assertEqual(len(result), 3)

    def test_get_week_expenses_order_is_descending(self):
        """Verifica que los resultados vienen ordenados del más reciente al más antiguo."""
        recent_data = self._make_recent_data()
        result = get_week_expenses(recent_data)
        # ghi789 es el más reciente (today - 4 días)
        self.assertEqual(result[0]["id"], "ghi789")
        self.assertEqual(result[-1]["id"], "abc123")

    def test_get_top_expense_day(self):
        """Verifica que se identifica el día con mayor gasto acumulado."""
        data = get_top_expense_day(self.static_data)
        # 2020-02-20 tiene 500, 2020-02-21 tiene 300, 2020-02-22 tiene 200
        self.assertEqual(data["date"], "2020-02-20")
        self.assertEqual(data["value"], 500)

    def test_calculate_summary_by_category(self):
        """Verifica que el resumen por categoría acumula correctamente."""
        data = calculate_summary_by_category(self.static_data)
        self.assertEqual(data, {"Comida": 700, "Transporte": 300})

    def test_calculate_daily_average(self):
        """Verifica que el promedio diario de la semana es correcto."""
        recent_data = self._make_recent_data()
        # total = 500 + 300 + 200 = 1000, dividido 7 días = 142.857
        result = calculate_daily_average(recent_data)
        self.assertAlmostEqual(result, 142.857, places=2)

    def test_calculate_historical_daily_average(self):
        """Verifica que el promedio histórico por día activo es correcto."""
        # static_data: total=1000, días únicos=3, promedio=333.33
        result = calculate_historical_daily_average(self.static_data)
        self.assertAlmostEqual(result, 333.33, places=2)

    # --- Casos borde ---

    def test_calculate_expense_percentage_empty_data(self):
        """Verifica que con lista vacía retorna dict vacío."""
        result = calculate_expense_percentage([])
        self.assertEqual(result, {})

    def test_calculate_summary_by_category_empty_data(self):
        """Verifica que con lista vacía retorna dict vacío."""
        result = calculate_summary_by_category([])
        self.assertEqual(result, {})

    def test_get_top_expense_day_empty_data(self):
        """Verifica que con lista vacía retorna dict vacío."""
        result = get_top_expense_day([])
        self.assertEqual(result, {})

    def test_get_week_expenses_empty_data(self):
        """Verifica que con lista vacía retorna lista vacía."""
        result = get_week_expenses([])
        self.assertEqual(result, [])

    def test_get_week_expenses_with_recent_dates(self):
        """Verifica que get_week_expenses detecta gastos con fechas dentro de los últimos 7 días."""
        today = datetime.now()
        recent_expense = {
            "id": "recent1",
            "category": "Ocio",
            "value": 150,
            "date": (today - timedelta(days=2)).isoformat(),
        }
        old_expense = {
            "id": "old1",
            "category": "Ocio",
            "value": 999,
            "date": "2020-01-01T10:00:00",
        }
        result = get_week_expenses([recent_expense, old_expense])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "recent1")

    def test_get_week_expenses_sorted_descending(self):
        """Verifica que los resultados vienen ordenados del más reciente al más antiguo."""
        today = datetime.now()
        expense_older = {
            "id": "older",
            "category": "Comida",
            "value": 100,
            "date": (today - timedelta(days=5)).isoformat(),
        }
        expense_newer = {
            "id": "newer",
            "category": "Comida",
            "value": 200,
            "date": (today - timedelta(days=1)).isoformat(),
        }
        result = get_week_expenses([expense_older, expense_newer])
        self.assertEqual(result[0]["id"], "newer")
        self.assertEqual(result[1]["id"], "older")

    def test_calculate_daily_average_empty_data(self):
        """Verifica que con lista vacía retorna 0."""
        result = calculate_daily_average([])
        self.assertEqual(result, 0)

    def test_calculate_historical_daily_average_empty_data(self):
        """Verifica que con lista vacía retorna 0."""
        result = calculate_historical_daily_average([])
        self.assertEqual(result, 0)

    def test_get_top_expense_day_multiple_expenses_same_day(self):
        """Verifica que acumula correctamente varios gastos del mismo día."""
        same_day_data = [
            {"id": "a", "category": "Comida", "value": 300, "date": "2026-03-01T09:00:00"},
            {"id": "b", "category": "Ocio", "value": 400, "date": "2026-03-01T20:00:00"},
            {"id": "c", "category": "Comida", "value": 100, "date": "2026-03-02T10:00:00"},
        ]
        result = get_top_expense_day(same_day_data)
        self.assertEqual(result["date"], "2026-03-01")
        self.assertEqual(result["value"], 700)
