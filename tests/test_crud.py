"""Tests unitarios para crud.py.

Mockea S3StorageService para aislar completamente la capa de persistencia
y evitar cualquier llamada real a AWS durante los tests.
"""

import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import src.crud as _crud_module
from src.crud import add_expense, read_history, delete_expense, modify_expense

_mock_storage = MagicMock()
_crud_module._storage_instance = _mock_storage


class TestReadHistory(unittest.TestCase):
    """Tests para read_history."""

    def setUp(self):
        """Resetea el mock de storage y lo re-inyecta en el módulo antes de cada test."""
        _mock_storage.reset_mock()
        _crud_module._storage_instance = _mock_storage

    def test_returns_list_when_storage_returns_data(self):
        """Verifica que retorna la lista de gastos cuando S3 responde correctamente."""
        sample = [{"id": "abc", "category": "Comida", "value": "500", "date": "2026-01-01T10:00:00"}]
        _mock_storage.read_file.return_value = sample
        result = read_history()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["category"], "Comida")

    def test_converts_value_to_float(self):
        """Verifica que el campo 'value' se convierte a float al leer."""
        sample = [{"id": "abc", "category": "Comida", "value": "250.5", "date": "2026-01-01T10:00:00"}]
        _mock_storage.read_file.return_value = sample
        result = read_history()
        self.assertIsInstance(result[0]["value"], float)
        self.assertAlmostEqual(result[0]["value"], 250.5)

    def test_returns_empty_list_when_storage_returns_none(self):
        """Verifica que retorna [] cuando S3 no devuelve contenido."""
        _mock_storage.read_file.return_value = None
        result = read_history()
        self.assertEqual(result, [])

    def test_returns_empty_list_on_invalid_value(self):
        """Verifica que retorna [] si algún 'value' no es convertible a float."""
        invalid = [{"id": "x", "category": "Comida", "value": "no_es_numero", "date": "2026-01-01T00:00:00"}]
        _mock_storage.read_file.return_value = invalid
        result = read_history()
        self.assertEqual(result, [])


class TestAddExpense(unittest.TestCase):
    """Tests para add_expense."""

    def setUp(self):
        _mock_storage.reset_mock()
        _crud_module._storage_instance = _mock_storage
        _mock_storage.read_file.return_value = []
        _mock_storage.save_file.return_value = True

    def test_returns_true_on_success(self):
        """Verifica que retorna True cuando S3 confirma el guardado."""
        result = add_expense("Comida", 500)
        self.assertTrue(result)

    def test_calls_save_file_with_new_expense(self):
        """Verifica que se llama a save_file con el nuevo gasto incluido."""
        add_expense("Transporte", 200)
        saved_data = _mock_storage.save_file.call_args[0][0]
        self.assertEqual(len(saved_data), 1)
        self.assertEqual(saved_data[0]["category"], "Transporte")
        self.assertEqual(saved_data[0]["value"],    200)

    def test_new_expense_has_id_and_date(self):
        """Verifica que el nuevo gasto incluye los campos 'id' y 'date' generados automáticamente."""
        add_expense("Salud", 100)
        saved_data = _mock_storage.save_file.call_args[0][0]
        self.assertIn("id",   saved_data[0])
        self.assertIn("date", saved_data[0])

    def test_each_expense_gets_unique_id(self):
        """Verifica que dos gastos consecutivos reciben ids distintos."""
        existing = [{"id": "first-id", "category": "Comida", "value": 100.0, "date": "2026-01-01T00:00:00"}]
        _mock_storage.read_file.return_value = existing
        add_expense("Ocio", 50)
        saved_data = _mock_storage.save_file.call_args[0][0]
        self.assertNotEqual(saved_data[0]["id"], saved_data[1]["id"])

    def test_returns_false_when_storage_fails(self):
        """Verifica que retorna False si S3 no confirma el guardado."""
        _mock_storage.save_file.return_value = False
        result = add_expense("Comida", 100)
        self.assertFalse(result)

    def test_returns_false_on_storage_exception(self):
        """Verifica que retorna False si S3 lanza una excepción inesperada."""
        _mock_storage.save_file.side_effect = Exception("S3 unavailable")
        result = add_expense("Comida", 100)
        self.assertFalse(result)
        _mock_storage.save_file.side_effect = None  # limpia el side_effect


class TestDeleteExpense(unittest.TestCase):
    """Tests para delete_expense."""

    def setUp(self):
        _mock_storage.reset_mock()
        _crud_module._storage_instance = _mock_storage
        _mock_storage.save_file.return_value = True

    def _make_expenses(self) -> list:
        return [
            {"id": "a", "category": "Comida",     "value": 500.0, "date": "2026-01-01T10:00:00"},
            {"id": "b", "category": "Transporte", "value": 300.0, "date": "2026-01-02T15:00:00"},
            {"id": "c", "category": "Salud",      "value": 100.0, "date": "2026-01-03T08:00:00"},
        ]

    def test_returns_true_on_success(self):
        """Verifica que retorna True cuando se elimina y guarda correctamente."""
        data = self._make_expenses()
        result = delete_expense(0, data)
        self.assertTrue(result)

    def test_removes_only_target_expense(self):
        """Verifica que solo se elimina el ítem con el índice indicado."""
        data = self._make_expenses()
        delete_expense(1, data)  # elimina Transporte
        saved_data = _mock_storage.save_file.call_args[0][0]
        categories = [e["category"] for e in saved_data]
        self.assertIn("Comida",    categories)
        self.assertIn("Salud",     categories)
        self.assertNotIn("Transporte", categories)

    def test_returns_false_when_storage_fails(self):
        """Verifica que retorna False si S3 no confirma el guardado."""
        _mock_storage.save_file.return_value = False
        data = self._make_expenses()
        result = delete_expense(0, data)
        self.assertFalse(result)

    def test_returns_false_on_invalid_index(self):
        """Verifica que retorna False con un índice fuera de rango."""
        data = self._make_expenses()
        result = delete_expense(99, data)
        self.assertFalse(result)


class TestModifyExpense(unittest.TestCase):
    """Tests para modify_expense."""

    def setUp(self):
        _mock_storage.reset_mock()
        _crud_module._storage_instance = _mock_storage
        _mock_storage.save_file.return_value = True

    def _make_expenses(self) -> list:
        return [{"id": "a", "category": "Comida", "value": 400.0, "date": "2026-01-01T10:00:00"}]

    def test_modifies_category_only(self):
        """Verifica que solo la categoría se actualiza cuando new_value es None."""
        data = self._make_expenses()
        modify_expense(data, 0, new_category="Transporte", new_value=None)
        saved_data = _mock_storage.save_file.call_args[0][0]
        self.assertEqual(saved_data[0]["category"], "Transporte")
        self.assertEqual(saved_data[0]["value"],    400.0)

    def test_modifies_value_only(self):
        """Verifica que solo el monto se actualiza cuando new_category es None."""
        data = self._make_expenses()
        modify_expense(data, 0, new_category=None, new_value=1200)
        saved_data = _mock_storage.save_file.call_args[0][0]
        self.assertEqual(saved_data[0]["category"], "Comida")
        self.assertEqual(saved_data[0]["value"],    1200)

    def test_modifies_both_fields(self):
        """Verifica que ambos campos se actualizan correctamente."""
        data = self._make_expenses()
        modify_expense(data, 0, new_category="Salud", new_value=750)
        saved_data = _mock_storage.save_file.call_args[0][0]
        self.assertEqual(saved_data[0]["category"], "Salud")
        self.assertEqual(saved_data[0]["value"],    750)

    def test_preserves_original_when_both_params_are_none(self):
        """Verifica que con ambos parámetros None el gasto no se altera."""
        data = self._make_expenses()
        modify_expense(data, 0, new_category=None, new_value=None)
        saved_data = _mock_storage.save_file.call_args[0][0]
        self.assertEqual(saved_data[0]["category"], "Comida")
        self.assertEqual(saved_data[0]["value"],    400.0)

    def test_returns_true_on_success(self):
        """Verifica que retorna True cuando S3 confirma el guardado."""
        data = self._make_expenses()
        result = modify_expense(data, 0, new_category="Ocio", new_value=50)
        self.assertTrue(result)

    def test_returns_false_when_storage_fails(self):
        """Verifica que retorna False si S3 no confirma el guardado."""
        _mock_storage.save_file.return_value = False
        data = self._make_expenses()
        result = modify_expense(data, 0, new_category="Ocio", new_value=50)
        self.assertFalse(result)
