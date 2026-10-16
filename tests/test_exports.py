"""Tests unitarios para exports.py.

Las funciones retornan strings en lugar de escribir archivos.
Streamlit se mockea a nivel de módulo para aislar st.warning.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Mockear streamlit antes de importar exports para evitar errores de entorno
sys.modules["streamlit"] = MagicMock()

from src.exports import export_general_report, export_detailed_report  # noqa: E402


class TestExportGeneralReport(unittest.TestCase):
    """Tests para export_general_report."""

    test_data = [
        {"id": "abc123", "category": "Comida",     "value": 500, "date": "2026-06-20T10:00:00"},
        {"id": "def456", "category": "Transporte", "value": 300, "date": "2026-06-21T15:30:00"},
        {"id": "ghi789", "category": "Comida",     "value": 200, "date": "2026-06-22T18:45:00"},
    ]

    def test_returns_string_with_categories(self):
        """Verifica que el reporte contiene las categorías presentes en los datos."""
        result = export_general_report(self.test_data)
        self.assertIn("Comida",     result)
        self.assertIn("Transporte", result)

    def test_returns_correct_category_totals(self):
        """Verifica que los totales acumulados por categoría son correctos."""
        result = export_general_report(self.test_data)
        self.assertIn("Comida : 700",     result)
        self.assertIn("Transporte : 300", result)

    def test_returns_grand_total(self):
        """Verifica que el gran total acumulado (1000) aparece en el reporte."""
        result = export_general_report(self.test_data)
        self.assertIn("Total Gastado 1000", result)

    def test_empty_data_returns_none_and_shows_warning(self):
        """Verifica que con lista vacía retorna None y llama a st.warning."""
        result = export_general_report([])
        self.assertIsNone(result)

    def test_single_category_report(self):
        """Verifica que con una sola categoría el reporte es coherente."""
        single = [{"id": "x", "category": "Salud", "value": 150, "date": "2026-01-01T00:00:00"}]
        result = export_general_report(single)
        self.assertIn("Salud",             result)
        self.assertIn("Total Gastado 150", result)

    def test_returns_plain_string(self):
        """Verifica que el tipo de retorno es str."""
        result = export_general_report(self.test_data)
        self.assertIsInstance(result, str)


class TestExportDetailedReport(unittest.TestCase):
    """Tests para export_detailed_report."""

    test_data = [
        {"id": "abc123", "category": "Comida",     "value": 500, "date": "2026-06-20T10:00:00"},
        {"id": "def456", "category": "Transporte", "value": 300, "date": "2026-06-21T15:30:00"},
        {"id": "ghi789", "category": "Comida",     "value": 200, "date": "2026-06-22T18:45:00"},
    ]

    def test_returns_string_with_all_entries(self):
        """Verifica que el reporte detallado contiene todos los gastos."""
        result = export_detailed_report(self.test_data)
        self.assertIn("Comida : 500",     result)
        self.assertIn("Transporte : 300", result)
        self.assertIn("Comida : 200",     result)

    def test_dates_are_formatted_as_dd_mm_yyyy(self):
        """Verifica que las fechas ISO se formatean como DD-MM-YYYY HH:MM."""
        result = export_detailed_report(self.test_data)
        self.assertIn("20-06-2026", result)
        self.assertIn("21-06-2026", result)
        self.assertIn("22-06-2026", result)

    def test_empty_data_returns_empty_string(self):
        """Verifica que con lista vacía retorna un string vacío."""
        result = export_detailed_report([])
        self.assertEqual(result, "")

    def test_returns_plain_string(self):
        """Verifica que el tipo de retorno es str."""
        result = export_detailed_report(self.test_data)
        self.assertIsInstance(result, str)

    def test_invalid_date_falls_back_to_raw_string(self):
        """Verifica que una fecha inválida no lanza excepción y usa el valor raw."""
        bad_date_data = [{"id": "x", "category": "Comida", "value": 100, "date": "FECHA-INVALIDA"}]
        result = export_detailed_report(bad_date_data)
        self.assertIn("FECHA-INVALIDA", result)

    def test_each_entry_uses_pipe_separator(self):
        """Verifica que cada línea usa el separador '|' entre fecha y categoría."""
        result = export_detailed_report(self.test_data)
        lines = result.strip().split("\n")
        for line in lines:
            self.assertIn("|", line)
