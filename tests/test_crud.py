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

    # --- Casos borde ---

    def test_read_history_creates_file_when_missing(self):
        """Verifica que read_history crea historial.json si no existe."""
        import os
        if os.path.isfile("historial.json"):
            os.remove("historial.json")
        result = read_history()
        self.assertEqual(result, [])
        self.assertTrue(os.path.isfile("historial.json"))

    def test_read_history_returns_empty_on_invalid_json(self):
        """Verifica que read_history retorna [] si el JSON está corrupto."""
        with open("historial.json", "w") as corrupt_file:
            corrupt_file.write("esto no es json válido {{{{")
        result = read_history()
        self.assertEqual(result, [])

    def test_add_multiple_expenses_generates_unique_ids(self):
        """Verifica que cada gasto recibe un id único."""
        add_expense("Comida", 100)
        add_expense("Comida", 200)
        data = read_history()
        self.assertNotEqual(data[0]["id"], data[1]["id"])

    def test_delete_only_removes_target_expense(self):
        """Verifica que al borrar un ítem los demás permanecen intactos."""
        add_expense("Comida", 100)
        add_expense("Transporte", 200)
        add_expense("Salud", 300)
        data = read_history()
        delete_expense(1, data)  # borra Transporte
        data_after = read_history()
        self.assertEqual(len(data_after), 2)
        categories = [expense["category"] for expense in data_after]
        self.assertIn("Comida", categories)
        self.assertIn("Salud", categories)
        self.assertNotIn("Transporte", categories)

    def test_modify_expense_without_changes_preserves_original(self):
        """Verifica que llamar modify_expense con None en ambos campos no altera el gasto."""
        add_expense("Comida", 400)
        data = read_history()
        modify_expense(data, 0, None, None)
        data_after = read_history()
        self.assertEqual(data_after[0]["category"], "Comida")
        self.assertEqual(data_after[0]["value"], 400)
