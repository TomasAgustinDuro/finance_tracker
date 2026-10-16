"""Helpers de filtrado sobre la lista de gastos.

Funciones puras y stateless: no modifican los datos de entrada ni acceden
a archivos o servicios externos. Diseñadas para ser usadas tanto desde
`vistas.py` como directamente en tests sin ninguna dependencia adicional.
"""


def get_unique_categories(data: list) -> set | list:
    """Retorna el conjunto de categorías únicas presentes en el historial.

    Itera sobre todos los gastos y extrae los valores del campo `category`,
    eliminando duplicados mediante un set.

    Args:
        data (list[dict]): Lista de gastos con campo `category` (str).

    Returns:
        set[str]: Set de categorías únicas (ej: `{"Comida", "Transporte"}`).
            Retorna `[]` si `data` está vacía.
    """
    if len(data) == 0:
        return []
    return set(expense["category"] for expense in data)


def filter_by_category(data: list, category: str) -> list:
    """Filtra y retorna solo los gastos que pertenecen a una categoría específica.

    La comparación es case-sensitive: `"comida"` y `"Comida"` son categorías
    distintas. Se espera que tanto los datos almacenados como el parámetro
    `category` estén capitalizados de forma consistente (ver `validate_category`).

    Args:
        data (list[dict]): Lista de gastos con campo `category` (str).
        category (str): Categoría exacta a filtrar (ej: `"Comida"`).

    Returns:
        list[dict]: Subconjunto de `data` donde `expense["category"] == category`.
            Retorna `[]` si no hay coincidencias o si `data` está vacía.
    """
    if len(data) == 0:
        return []
    return [expense for expense in data if expense["category"] == category]
