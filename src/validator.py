"""Validación y normalización de inputs del usuario.

Funciones puras que reciben el input crudo del formulario y retornan
el valor normalizado o `None` si no es válido. Actúan como guard clause
antes de que los datos lleguen a la capa de persistencia.
"""


def validate_category(category: str) -> str | None:
    """Valida y normaliza una categoría de gasto.

    Capitaliza el primer carácter y elimina los espacios sobrantes al inicio
    y al final. Rechaza strings vacíos, que contengan dígitos o caracteres
    no alfabéticos (incluyendo guiones y signos de puntuación).

    Args:
        category (str): String ingresado por el usuario como categoría.

    Returns:
        str | None: Categoría capitalizada y sin espacios si es válida
            (ej: `"Comida"`, `"Servicios del hogar"`).
            `None` si el string está vacío, contiene números o caracteres especiales.
    """
    formatted_category = category.capitalize().strip()

    if formatted_category.replace(" ", "").isalpha() and formatted_category != "":
        return formatted_category
    return None


def validate_mount(mount: float | int | None) -> float | None:
    """Valida que el monto sea un número positivo mayor a cero.

    Recibe el valor ya parseado por `st.number_input` (float o int).
    Rechaza `None`, cero y valores negativos.

    Args:
        mount (float | int | None): Monto ingresado por el usuario desde el formulario.

    Returns:
        float | None: El mismo valor si es válido (positivo y mayor a cero).
            `None` si el valor es `None`, cero o negativo.
    """
    if mount and mount > 0:
        return mount
    return None
