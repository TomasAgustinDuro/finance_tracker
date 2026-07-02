"""Tests unitarios para filters.py.

Cubre el happy path y casos borde de get_unique_categories y filter_by_category.
Funciones puras, sin dependencias externas — no se necesitan mocks.
"""

import unittest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.filters import get_unique_categories, filter_by_category


SAMPLE_DATA = [
    {"id": "abc123", "category": "Comida",     "value": 500, "date": "2026-02-20T10:00:00"},
    {"id": "def456", "category": "Transporte", "value": 300, "date": "2026-02-21T15:30:00"},
    {"id": "ghi789", "category": "Comida",     "value": 200, "date": "2026-02-22T18:45:00"},
]


class TestGetUniqueCategories(unittest.TestCase):
    """Tests para get_unique_categories."""

    def test_returns_set_with_all_distinct_categories(self):
        """Verifica que devuelve exactamente las categorías únicas presentes."""
        result = get_unique_categories(SAMPLE_DATA)
        self.assertIn("Comida",     result)
        self.assertIn("Transporte", result)
        self.assertEqual(len(result), 2)

    def test_duplicate_category_counted_once(self):
        """Verifica que 'Comida' aparece dos veces en los datos pero solo una en el set."""
        result = get_unique_categories(SAMPLE_DATA)
        comida_count = list(result).count("Comida")
        self.assertEqual(comida_count, 1)

    def test_empty_data_returns_empty_list(self):
        """Verifica que con lista vacía retorna lista vacía."""
        result = get_unique_categories([])
        self.assertEqual(result, [])

    def test_single_entry_returns_single_category(self):
        """Verifica que con un solo gasto retorna el set con esa categoría."""
        single = [{"id": "x", "category": "Salud", "value": 100, "date": "2026-01-01T00:00:00"}]
        result = get_unique_categories(single)
        self.assertIn("Salud", result)
        self.assertEqual(len(result), 1)

    def test_all_same_category_returns_one_element(self):
        """Verifica que si todos los gastos son de la misma categoría retorna un set de tamaño 1."""
        same_cat = [
            {"id": "a", "category": "Comida", "value": 100, "date": "2026-01-01T00:00:00"},
            {"id": "b", "category": "Comida", "value": 200, "date": "2026-01-02T00:00:00"},
        ]
        result = get_unique_categories(same_cat)
        self.assertEqual(len(result), 1)


class TestFilterByCategory(unittest.TestCase):
    """Tests para filter_by_category."""

    def test_returns_only_matching_expenses(self):
        """Verifica que filtra correctamente y devuelve solo los gastos de 'Comida'."""
        result = filter_by_category(SAMPLE_DATA, "Comida")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(e["category"] == "Comida" for e in result))

    def test_returns_full_expense_objects(self):
        """Verifica que los objetos retornados son los originales completos."""
        result = filter_by_category(SAMPLE_DATA, "Transporte")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"],    "def456")
        self.assertEqual(result[0]["value"], 300)

    def test_nonexistent_category_returns_empty_list(self):
        """Verifica que filtrar por una categoría inexistente retorna lista vacía."""
        result = filter_by_category(SAMPLE_DATA, "Viajes")
        self.assertEqual(result, [])

    def test_empty_data_returns_empty_list(self):
        """Verifica que con lista vacía retorna lista vacía."""
        result = filter_by_category([], "Comida")
        self.assertEqual(result, [])

    def test_comparison_is_case_sensitive(self):
        """Verifica que la comparación distingue mayúsculas (comida != Comida)."""
        result = filter_by_category(SAMPLE_DATA, "comida")
        self.assertEqual(result, [])
