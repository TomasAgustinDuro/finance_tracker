import unittest

from filters import get_unique_categories, filter_by_category


class testFILTERS(unittest.TestCase):
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

    def test_get_unique_categories(self):
        data = get_unique_categories(self.test_data)

        self.assertIn("Comida", data)
        self.assertIn("Transporte", data)
        self.assertEqual(len(data), 2)

    def test_filter_by_category(self):
        data = filter_by_category(self.test_data, "Comida")

        self.assertEqual(
            data,
            [
                {
                    "id": "abc123",
                    "category": "Comida",
                    "value": 500,
                    "date": "2026-02-20T10:00:00",
                },
                {
                    "id": "ghi789",
                    "category": "Comida",
                    "value": 200,
                    "date": "2026-02-22T18:45:00",
                },
            ],
        )
