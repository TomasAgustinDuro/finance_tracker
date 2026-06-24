"""Helpers de filtrado sobre la lista de gastos.

Funciones puras stateless: no modifican los datos de entrada ni acceden a archivos.
"""

# Helper
def get_unique_categories(data: list) -> set:
    """Retorna el conjunto de categorías únicas presentes en el historial.

    Args:
        data (list[dict]): Lista de gastos con campo 'category'.

    Returns:
        set[str] | list: Set de categorías únicas, o lista vacía si no hay datos.
    """
    if len(data) == 0:
        return []
    else:
        return set(expense["category"] for expense in data)

# Helper
def filter_by_category(data: list, category: str) -> list:
    """Filtra y retorna solo los gastos que pertenecen a una categoría específica.

    La comparación es sensible a mayúsculas. Se espera que 'category' esté
    capitalizada de la misma forma que los registros almacenados.

    Args:
        data (list[dict]): Lista de gastos con campo 'category'.
        category (str): Categoría exacta a filtrar (ej: 'Comida').

    Returns:
        list[dict]: Lista de gastos que coinciden con la categoría. Lista vacía si no hay coincidencias.
    """
    if len(data) == 0:
        return []
    else:
        return [element for element in data if element["category"] == category]