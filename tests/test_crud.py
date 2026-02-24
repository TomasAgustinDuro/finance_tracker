import unittest
import json
from crud import add_expense, read_history, delete_expense, modify_expense


class TestCRUD(unittest.TestCase):
    def setUp(self):
        with open("historial.json", "w") as f:
            json.dump([], f)

    # Agregar un gasto positivo, con categoria
    def test_add_expense(self):
        self.assertTrue(add_expense("Comida", 500))

        data = read_history()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], "Comida")
        self.assertEqual(data[0]["value"], 500)
        self.assertIn("id", data[0])
        self.assertIn("date", data[0])

    def test_delete_expense(self):
        add_expense("Comida", 200)

        data = read_history()

        self.assertTrue(delete_expense(0, data))

        data_after = read_history()

        self.assertEqual(len(data_after), 0)

    def test_modify_expense_category(self):
        add_expense("Comida", 400)

        data = read_history()

        self.assertTrue(modify_expense(data, 0, "Transporte", None))

        data_after = read_history()

        self.assertEqual(len(data_after), 1)
        self.assertEqual(data_after[0]["category"], "Transporte")

    def test_modify_value(self):
        add_expense("Comida", 400)

        data = read_history()

        self.assertTrue(modify_expense(data, 0, None, 1200))

        data_after = read_history()

        self.assertEqual(len(data_after), 1)
        self.assertEqual(data_after[0]["value"], 1200)

    def test_modify_both(self):
        add_expense("Comida", 400)

        data = read_history()

        self.assertTrue(modify_expense(data, 0, "Transporte", 200))

        data_after = read_history()

        self.assertEqual(len(data_after), 1)
        self.assertEqual(data_after[0]["category"], "Transporte")
        self.assertEqual(data_after[0]["value"], 200)
