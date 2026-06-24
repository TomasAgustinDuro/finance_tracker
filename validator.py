def validate_category(category: str) -> str | None:
    """Valida y normaliza una categoría de gasto ingresada por el usuario.

    Capitaliza y elimina espacios sobrantes. Rechaza strings vacíos o con números.

    Args:
        category (str): String ingresado por el usuario como categoría.

    Returns:
        str | None: Categoría formateada si es válida, None si es inválida o vacía.
    """
    formatted_category = category.capitalize().strip()

    if formatted_category.replace(" ", "").isalpha() and formatted_category != "":
        return formatted_category
    return None


def validate_mount(mount: str) -> int | None:
    """Valida que el monto ingresado sea un entero positivo mayor a cero.

    Args:
        mount (str): String ingresado por el usuario como monto.

    Returns:
        int | None: Monto como entero si es válido, None si es inválido, vacío o cero.
    """
    if mount.isdigit() and int(mount) > 0:
        return int(mount)
    return None