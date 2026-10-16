"""Tests unitarios para vistas.py.

Todas las funciones usan Streamlit, por lo que se mockea el módulo completo
antes de importar vistas. Se testean únicamente los retornos y la lógica pura,
no el renderizado visual.
"""

import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ---------------------------------------------------------------------------
# Patch global de Streamlit: evita que cualquier llamada a st.* falle
# ya que en tests no existe un servidor Streamlit corriendo.
# ---------------------------------------------------------------------------
_mock_st = MagicMock()
sys.modules["streamlit"] = _mock_st

# Importaciones después del patch
from src.vistas import show_summary_cat, show_history


SAMPLE_DATA = [
    {"id": "abc123", "category": "Comida",     "value": 500, "date": "2026-06-20T10:00:00"},
    {"id": "def456", "category": "Transporte", "value": 300, "date": "2026-06-21T15:30:00"},
]


class TestShowSummaryCat(unittest.TestCase):
    """Tests para show_summary_cat.

    La función delega el cálculo a calculate_summary_by_category y retorna el dict.
    Con lista vacía llama a st.warning y retorna None.
    """

    def setUp(self):
        _mock_st.reset_mock()

    def test_returns_dict_with_category_totals(self):
        """Verifica que retorna un dict con el total acumulado por categoría."""
        result = show_summary_cat(SAMPLE_DATA)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("Comida"),     500)
        self.assertEqual(result.get("Transporte"), 300)

    def test_empty_data_returns_none_and_warns(self):
        """Verifica que con lista vacía retorna None y llama a st.warning."""
        result = show_summary_cat([])
        self.assertIsNone(result)
        _mock_st.warning.assert_called_once()

    def test_multiple_expenses_same_category_are_accumulated(self):
        """Verifica que varios gastos de la misma categoría se acumulan."""
        data = [
            {"id": "a", "category": "Comida", "value": 200, "date": "2026-01-01T00:00:00"},
            {"id": "b", "category": "Comida", "value": 300, "date": "2026-01-02T00:00:00"},
        ]
        result = show_summary_cat(data)
        self.assertEqual(result["Comida"], 500)


class TestShowHistory(unittest.TestCase):
    """Tests para show_history.

    La función mapea los datos y llama a st.dataframe.
    Con lista vacía llama a st.warning.
    """

    def setUp(self):
        _mock_st.reset_mock()

    def test_calls_st_dataframe_with_data(self):
        """Verifica que st.dataframe es invocado cuando hay gastos."""
        show_history(SAMPLE_DATA)
        _mock_st.dataframe.assert_called_once()

    def test_empty_data_calls_st_warning(self):
        """Verifica que con lista vacía se llama a st.warning."""
        show_history([])
        _mock_st.warning.assert_called_once()

    def test_maps_date_to_dd_mm_yyyy_format(self):
        """Verifica que la fecha ISO se convierte al formato DD/MM/YYYY en el payload enviado a st.dataframe."""
        show_history(SAMPLE_DATA)
        call_args = _mock_st.dataframe.call_args[0][0]
        dates = [row["date"] for row in call_args]
        self.assertIn("20/06/2026", dates)
        self.assertIn("21/06/2026", dates)

    def test_maps_category_to_capitalized(self):
        """Verifica que la categoría se presenta capitalizada en el payload."""
        lowercase_data = [
            {"id": "x", "category": "comida", "value": 100, "date": "2026-01-01T00:00:00"}
        ]
        show_history(lowercase_data)
        call_args = _mock_st.dataframe.call_args[0][0]
        self.assertEqual(call_args[0]["category"], "Comida")

    def test_excludes_entries_without_category(self):
        """Verifica que los gastos sin campo 'category' son ignorados silenciosamente."""
        mixed_data = [
            {"id": "a", "category": "Comida", "value": 100, "date": "2026-01-01T00:00:00"},
            {"id": "b", "value": 200, "date": "2026-01-02T00:00:00"},  # sin category
        ]
        show_history(mixed_data)
        call_args = _mock_st.dataframe.call_args[0][0]
        self.assertEqual(len(call_args), 1)
