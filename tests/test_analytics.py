import unittest

from analytics import (
    calculate_expense_percentage,
    get_week_expenses,
    get_top_expense_day,
    calculate_summary_by_category,
    calculate_daily_average,
    calculate_historical_daily_average,
)


class testANALYTICS(unittest.TestCase):
    test_data = [
        {
            "id": "abc123",
            "category": "Comida",
            "value": 500,
            "date": "2026-02-20T10:00:00",
        },
        {
            "id": "def456",
            "category": "Transporte",
            "value": 300,
            "date": "2026-02-21T15:30:00",
        },
        {
            "id": "ghi789",
            "category": "Comida",
            "value": 200,
            "date": "2026-02-22T18:45:00",
        },
    ]

    def test_calculate_expense_percentage(self):
        data = calculate_expense_percentage(self.test_data)

        self.assertAlmostEqual(data["Comida"], 70.0, places=1)
        self.assertAlmostEqual(data["Transporte"], 30.0, places=1)

    def test_get_week_expenses(self):
        data = get_week_expenses(self.test_data)

        self.assertEqual(
            data,
            [
                {
                    "id": "ghi789",
                    "category": "Comida",
                    "value": 200,
                    "date": "2026-02-22T18:45:00",
                },
                {
                    "id": "def456",
                    "category": "Transporte",
                    "value": 300,
                    "date": "2026-02-21T15:30:00",
                },
                {
                    "id": "abc123",
                    "category": "Comida",
                    "value": 500,
                    "date": "2026-02-20T10:00:00",
                },
            ],
        )

    def test_get_top_expense_day(self):
        data = get_top_expense_day(self.test_data)

        self.assertEqual(
            data,
            {
                "date": "2026-02-20", 
                "value": 500,
            },
        )

    def test_calculate_summary_by_category(self):
        data = calculate_summary_by_category(self.test_data)

        self.assertEqual(data, {"Comida": 700, "Transporte": 300})

    def test_calculate_daily_average(self):
        data = calculate_daily_average(self.test_data)

        self.assertAlmostEqual(data, 142.857, places=2)

    def test_calculate_historical_daily_average(self):
        data = calculate_historical_daily_average(self.test_data)

        self.assertAlmostEqual(data, 333.33, places=2)
