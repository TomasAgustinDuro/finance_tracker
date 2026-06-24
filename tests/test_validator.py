"""Tests unitarios para validator.py.

Cubre el happy path y casos borde de validate_category y validate_mount.
"""

import unittest

from validator import validate_category, validate_mount


class TestValidator(unittest.TestCase):

    # --- validate_category: happy path ---

    def test_validate_category_returns_capitalized_string(self):
        """Verifica que una categoría válida se retorna capitalizada y sin espacios."""
        result = validate_category("comida")
        self.assertEqual(result, "Comida")

    def test_validate_category_strips_surrounding_spaces(self):
        """Verifica que los espacios sobrantes al inicio y final se eliminan."""
        result = validate_category("  transporte  ")
        self.assertEqual(result, "Transporte")

    def test_validate_category_accepts_multiword(self):
        """Verifica que una categoría con espacios internos es válida."""
        result = validate_category("servicios del hogar")
        self.assertEqual(result, "Servicios del hogar")

    # --- validate_category: casos borde ---

    def test_validate_category_rejects_empty_string(self):
        """Verifica que un string vacío retorna None."""
        result = validate_category("")
        self.assertIsNone(result)

    def test_validate_category_rejects_only_spaces(self):
        """Verifica que un string de solo espacios retorna None."""
        result = validate_category("   ")
        self.assertIsNone(result)

    def test_validate_category_rejects_string_with_digits(self):
        """Verifica que una categoría con números retorna None."""
        result = validate_category("Comida1")
        self.assertIsNone(result)

    def test_validate_category_rejects_only_digits(self):
        """Verifica que un string solo numérico retorna None."""
        result = validate_category("123")
        self.assertIsNone(result)

    def test_validate_category_rejects_special_characters(self):
        """Verifica que una categoría con caracteres especiales retorna None."""
        result = validate_category("comida!")
        self.assertIsNone(result)

    # --- validate_mount: happy path ---

    def test_validate_mount_returns_integer_for_valid_input(self):
        """Verifica que un monto válido se retorna como entero."""
        result = validate_mount("500")
        self.assertEqual(result, 500)
        self.assertIsInstance(result, int)

    def test_validate_mount_accepts_single_digit(self):
        """Verifica que el mínimo válido (1) es aceptado."""
        result = validate_mount("1")
        self.assertEqual(result, 1)

    # --- validate_mount: casos borde ---

    def test_validate_mount_rejects_zero(self):
        """Verifica que el valor 0 retorna None."""
        result = validate_mount("0")
        self.assertIsNone(result)

    def test_validate_mount_rejects_empty_string(self):
        """Verifica que un string vacío retorna None."""
        result = validate_mount("")
        self.assertIsNone(result)

    def test_validate_mount_rejects_float_string(self):
        """Verifica que un decimal como string retorna None."""
        result = validate_mount("3.14")
        self.assertIsNone(result)

    def test_validate_mount_rejects_negative_number(self):
        """Verifica que un número negativo retorna None."""
        result = validate_mount("-5")
        self.assertIsNone(result)

    def test_validate_mount_rejects_text(self):
        """Verifica que un string no numérico retorna None."""
        result = validate_mount("abc")
        self.assertIsNone(result)

    def test_validate_mount_rejects_number_with_spaces(self):
        """Verifica que un número con espacios retorna None."""
        result = validate_mount(" 100 ")
        self.assertIsNone(result)
