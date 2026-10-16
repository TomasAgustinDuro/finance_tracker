"""Tests unitarios para validator.py.

validate_category recibe un str.
validate_mount recibe un número (int/float) — la UI de Streamlit ya hace el parsing.
"""

import unittest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.validator import validate_category, validate_mount


class TestValidateCategory(unittest.TestCase):
    """Tests para validate_category."""

    # --- Happy path ---

    def test_returns_capitalized_string(self):
        """Verifica que una categoría minúscula válida se retorna capitalizada."""
        self.assertEqual(validate_category("comida"), "Comida")

    def test_strips_surrounding_spaces(self):
        """Verifica que los espacios al inicio y final se eliminan."""
        self.assertEqual(validate_category("  transporte  "), "Transporte")

    def test_accepts_multiword_category(self):
        """Verifica que una categoría con espacios internos es válida."""
        result = validate_category("servicios del hogar")
        self.assertEqual(result, "Servicios del hogar")

    def test_already_capitalized_stays_the_same(self):
        """Verifica que una categoría ya capitalizada se retorna sin cambios."""
        self.assertEqual(validate_category("Salud"), "Salud")

    # --- Casos borde ---

    def test_empty_string_returns_none(self):
        """Verifica que un string vacío retorna None."""
        self.assertIsNone(validate_category(""))

    def test_only_spaces_returns_none(self):
        """Verifica que un string de solo espacios retorna None."""
        self.assertIsNone(validate_category("   "))

    def test_string_with_digits_returns_none(self):
        """Verifica que una categoría que contiene números retorna None."""
        self.assertIsNone(validate_category("Comida1"))

    def test_only_digits_returns_none(self):
        """Verifica que un string solo numérico retorna None."""
        self.assertIsNone(validate_category("123"))

    def test_special_characters_return_none(self):
        """Verifica que caracteres especiales hacen que retorne None."""
        self.assertIsNone(validate_category("comida!"))

    def test_hyphen_returns_none(self):
        """Verifica que un guión en la categoría retorna None."""
        self.assertIsNone(validate_category("super-mercado"))


class TestValidateMount(unittest.TestCase):
    """Tests para validate_mount.

    La función recibe un número (int o float) ya parseado por Streamlit's st.number_input.
    """

    # --- Happy path ---

    def test_positive_integer_is_returned_as_is(self):
        """Verifica que un entero positivo se retorna sin modificaciones."""
        result = validate_mount(500)
        self.assertEqual(result, 500)

    def test_positive_float_is_returned_as_is(self):
        """Verifica que un float positivo (ej: 9.99) se retorna sin modificaciones."""
        result = validate_mount(9.99)
        self.assertAlmostEqual(result, 9.99)

    def test_minimum_valid_value_is_accepted(self):
        """Verifica que 0.01 (mínimo positivo) es aceptado."""
        result = validate_mount(0.01)
        self.assertAlmostEqual(result, 0.01)

    # --- Casos borde ---

    def test_zero_returns_none(self):
        """Verifica que el valor 0 retorna None."""
        self.assertIsNone(validate_mount(0))

    def test_zero_float_returns_none(self):
        """Verifica que 0.0 retorna None."""
        self.assertIsNone(validate_mount(0.0))

    def test_negative_number_returns_none(self):
        """Verifica que un número negativo retorna None."""
        self.assertIsNone(validate_mount(-10))

    def test_none_input_returns_none(self):
        """Verifica que pasar None retorna None sin lanzar excepción."""
        self.assertIsNone(validate_mount(None))
