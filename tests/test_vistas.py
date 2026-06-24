"""Tests unitarios para vistas.py.

Cubre las funciones testeables de la capa de presentación usando unittest.mock
para simular input() y aislar las dependencias de I/O.
"""

import unittest
from unittest.mock import patch, MagicMock

from vistas import (
    process_expense_modification,
    show_history,
    show_top_expenses,
    show_summary_cat,
    show_week,
    show_percentage,
)


SAMPLE_EXPENSES = [
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
]


class TestProcessExpenseModification(unittest.TestCase):
    """Tests para process_expense_modification."""

    def _make_expenses(self) -> list:
        """Retorna una copia fresca de SAMPLE_EXPENSES para cada test."""
        return [expense.copy() for expense in SAMPLE_EXPENSES]

    def test_ignores_out_of_range_index(self):
        """Verifica que un índice fuera de rango no lanza excepción ni modifica datos."""
        gastos = self._make_expenses()
        # índice 99 es mayor que len(gastos), no debe hacer nada
        process_expense_modification(gastos, "99")
        self.assertEqual(gastos[0]["category"], "Comida")

    def test_ignores_non_digit_index(self):
        """Verifica que un índice no numérico no lanza excepción."""
        gastos = self._make_expenses()
        process_expense_modification(gastos, "abc")
        self.assertEqual(gastos[0]["value"], 500)

    def test_ignores_zero_index(self):
        """Verifica que el índice 0 (inválido, la UI usa base 1) no modifica nada."""
        gastos = self._make_expenses()
        process_expense_modification(gastos, "0")
        self.assertEqual(gastos[0]["category"], "Comida")

    @patch("vistas.modify_expense", return_value=True)
    @patch("builtins.input", side_effect=["Salud", "800", "Y"])
    def test_modifies_both_fields_on_confirmation(self, mock_input: MagicMock, mock_modify: MagicMock) -> None:
        """Verifica que con confirmación Y se llama modify_expense con los valores correctos."""
        gastos = self._make_expenses()
        process_expense_modification(gastos, "1")
        mock_modify.assert_called_once_with(gastos, 0, "Salud", 800)

    @patch("vistas.modify_expense", return_value=True)
    @patch("builtins.input", side_effect=["", "800", "Y"])
    def test_modifies_only_value_when_category_empty(self, mock_input: MagicMock, mock_modify: MagicMock) -> None:
        """Verifica que si la categoría queda vacía solo se actualiza el monto."""
        gastos = self._make_expenses()
        process_expense_modification(gastos, "1")
        mock_modify.assert_called_once_with(gastos, 0, None, 800)

    @patch("vistas.modify_expense", return_value=True)
    @patch("builtins.input", side_effect=["Salud", "", "Y"])
    def test_modifies_only_category_when_value_empty(self, mock_input: MagicMock, mock_modify: MagicMock) -> None:
        """Verifica que si el monto queda vacío solo se actualiza la categoría."""
        gastos = self._make_expenses()
        process_expense_modification(gastos, "1")
        mock_modify.assert_called_once_with(gastos, 0, "Salud", None)

    @patch("vistas.modify_expense")
    @patch("builtins.input", side_effect=["Salud", "800", "N"])
    def test_does_not_modify_when_confirmation_is_no(self, mock_input: MagicMock, mock_modify: MagicMock) -> None:
        """Verifica que con confirmación N no se llama modify_expense."""
        gastos = self._make_expenses()
        process_expense_modification(gastos, "1")
        mock_modify.assert_not_called()

    @patch("vistas.modify_expense")
    @patch("builtins.input", side_effect=["", ""])
    def test_does_not_modify_when_both_fields_empty(self, mock_input: MagicMock, mock_modify: MagicMock) -> None:
        """Verifica que si ambos campos quedan vacíos no se llama modify_expense."""
        gastos = self._make_expenses()
        process_expense_modification(gastos, "1")
        mock_modify.assert_not_called()


class TestShowFunctions(unittest.TestCase):
    """Tests para las funciones de visualización que imprimen en consola."""

    @patch("builtins.print")
    def test_show_history_prints_each_expense(self, mock_print: MagicMock) -> None:
        """Verifica que show_history imprime una línea por cada gasto."""
        show_history(SAMPLE_EXPENSES)
        self.assertEqual(mock_print.call_count, 2)

    @patch("builtins.print")
    def test_show_history_empty_data_prints_nothing(self, mock_print: MagicMock) -> None:
        """Verifica que con lista vacía show_history no imprime nada."""
        show_history([])
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_show_top_expenses_prints_result(self, mock_print: MagicMock) -> None:
        """Verifica que show_top_expenses imprime el día con mayor gasto."""
        show_top_expenses(SAMPLE_EXPENSES)
        mock_print.assert_called_once()
        output = mock_print.call_args[0][0]
        self.assertIn("2026-06-21", output)

    @patch("builtins.print")
    def test_show_top_expenses_empty_data_prints_warning(self, mock_print: MagicMock) -> None:
        """Verifica que con lista vacía show_top_expenses imprime el mensaje de aviso."""
        show_top_expenses([])
        mock_print.assert_called_once_with("No hay información para mostrar")

    @patch("builtins.print")
    def test_show_summary_cat_prints_each_category(self, mock_print: MagicMock) -> None:
        """Verifica que show_summary_cat imprime una línea por categoría."""
        show_summary_cat(SAMPLE_EXPENSES)
        printed_lines = [call[0][0] for call in mock_print.call_args_list]
        self.assertTrue(any("Comida" in line for line in printed_lines))
        self.assertTrue(any("Transporte" in line for line in printed_lines))

    @patch("builtins.print")
    def test_show_summary_cat_empty_data_prints_warning(self, mock_print: MagicMock) -> None:
        """Verifica que con lista vacía show_summary_cat imprime el mensaje de aviso."""
        show_summary_cat([])
        mock_print.assert_called_once_with("No hay información para mostrar")

    @patch("builtins.print")
    def test_show_percentage_empty_data_prints_warning(self, mock_print: MagicMock) -> None:
        """Verifica que con lista vacía show_percentage imprime el mensaje de aviso."""
        show_percentage([])
        mock_print.assert_called_once_with(
            "No hay información con la que calcualr los porcentajes"
        )
