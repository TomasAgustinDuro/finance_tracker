"""Tests unitarios para exports.py.

Cubre el happy path y casos borde de export_general_report
y export_detailed_report.
"""

import unittest
import os

from exports import export_general_report, export_detailed_report


GENERAL_REPORT_FILE = "resumen_general.txt"
DETAILED_REPORT_FILE = "resumen_detalado.txt"


class TestExports(unittest.TestCase):
    test_data = [
        {
            "id": "abc123",
            "category": "Comida",
            "value": 500,
            "date": "2026-06-20T10:00:00",
        },
        {
            "id": "def456",
            "category": "Transporte",
            "value": 300,
            "date": "2026-06-21T15:30:00",
        },
        {
            "id": "ghi789",
            "category": "Comida",
            "value": 200,
            "date": "2026-06-22T18:45:00",
        },
    ]

    def tearDown(self):
        """Limpia los archivos generados después de cada test."""
        for file_path in [GENERAL_REPORT_FILE, DETAILED_REPORT_FILE]:
            if os.path.isfile(file_path):
                os.remove(file_path)

    # --- export_general_report ---

    def test_export_general_report_creates_file(self):
        """Verifica que se crea el archivo resumen_general.txt."""
        export_general_report(self.test_data)
        self.assertTrue(os.path.isfile(GENERAL_REPORT_FILE))

    def test_export_general_report_contains_categories(self):
        """Verifica que el reporte contiene todas las categorías."""
        export_general_report(self.test_data)
        with open(GENERAL_REPORT_FILE, "r") as report_file:
            content = report_file.read()
        self.assertIn("Comida", content)
        self.assertIn("Transporte", content)

    def test_export_general_report_correct_totals(self):
        """Verifica que los totales por categoría son correctos (Comida=700, Transporte=300)."""
        export_general_report(self.test_data)
        with open(GENERAL_REPORT_FILE, "r") as report_file:
            content = report_file.read()
        self.assertIn("Comida : 700", content)
        self.assertIn("Transporte : 300", content)

    def test_export_general_report_grand_total(self):
        """Verifica que el total general acumulado es correcto."""
        export_general_report(self.test_data)
        with open(GENERAL_REPORT_FILE, "r") as report_file:
            content = report_file.read()
        self.assertIn("Total Gastado 1000", content)

    def test_export_general_report_empty_data(self):
        """Verifica que con lista vacía no se crea el archivo."""
        export_general_report([])
        self.assertFalse(os.path.isfile(GENERAL_REPORT_FILE))

    # --- export_detailed_report ---

    def test_export_detailed_report_creates_file(self):
        """Verifica que se crea el archivo resumen_detalado.txt."""
        export_detailed_report(self.test_data)
        self.assertTrue(os.path.isfile(DETAILED_REPORT_FILE))

    def test_export_detailed_report_contains_all_entries(self):
        """Verifica que el reporte detallado incluye todos los gastos."""
        export_detailed_report(self.test_data)
        with open(DETAILED_REPORT_FILE, "r") as report_file:
            content = report_file.read()
        self.assertIn("Comida : 500", content)
        self.assertIn("Transporte : 300", content)
        self.assertIn("Comida : 200", content)

    def test_export_detailed_report_contains_dates(self):
        """Verifica que el reporte detallado incluye las fechas de cada gasto."""
        export_detailed_report(self.test_data)
        with open(DETAILED_REPORT_FILE, "r") as report_file:
            content = report_file.read()
        self.assertIn("2026-06-20T10:00:00", content)
        self.assertIn("2026-06-21T15:30:00", content)
        self.assertIn("2026-06-22T18:45:00", content)

    def test_export_detailed_report_empty_data(self):
        """Verifica que con lista vacía se crea un archivo vacío sin errores."""
        export_detailed_report([])
        self.assertTrue(os.path.isfile(DETAILED_REPORT_FILE))
        with open(DETAILED_REPORT_FILE, "r") as report_file:
            content = report_file.read()
        self.assertEqual(content, "")
