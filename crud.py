"""Capa de persistencia del historial de gastos.

Responsable exclusivamente de leer y escribir sobre historial.json.
Ninguna otra capa debe acceder al archivo directamente.
"""

import json
import os.path
import uuid
from datetime import datetime

HISTORY_FILE = "historial.json"


def read_history() -> list:
    """Lee y retorna el historial de gastos desde historial.json.

    Si el archivo no existe, lo crea vacío y retorna una lista vacía.
    Si el contenido es inválido, retorna una lista vacía sin lanzar excepción.

    Returns:
        list[dict]: Lista de gastos. Cada gasto contiene 'id', 'category', 'value' y 'date'.
    """
    if os.path.isfile(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)

                for expense in data:
                    expense["value"] = int(expense["value"])
            return data
        except (json.JSONDecodeError, ValueError):
            return []
    else:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

        return []


# AGREGAR GASTO
def add_expense(category_expense_formatted: str, value_expense_formatted: int) -> bool:
    """Agrega un nuevo gasto al historial persistido en HISTORY_FILE.

    Genera automáticamente un id único (UUID hex) y la fecha/hora actual.
    Lee el historial existente, agrega el nuevo ítem y sobreescribe el archivo.

    Args:
        category_expense_formatted (str): Categoría del gasto ya capitalizada y sin espacios sobrantes.
        value_expense_formatted (int): Monto del gasto como entero positivo.

    Returns:
        bool: True si el gasto se guardó correctamente, False si hubo un error de I/O.
    """

    expenses = read_history()

    new_expense = {
        "id": uuid.uuid4().hex,
        "category": category_expense_formatted,
        "value": value_expense_formatted,
        "date": datetime.now().isoformat(),
    }

    try:
        expenses.append(new_expense)

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=4, ensure_ascii=False)

        return True

    except (IOError, PermissionError) :
        return False


def delete_expense(indice: int, data: list) -> bool:
    """Elimina un gasto del historial por su índice y persiste el resultado.

    Args:
        indice (int): Índice (base 0) del gasto a eliminar dentro de la lista.
        data (list[dict]): Lista completa de gastos cargada previamente.

    Returns:
        bool: True si se eliminó y guardó correctamente, False si hubo un error de I/O.
    """
    try:
        del data[indice]
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return True
    except (IOError, PermissionError) :
        return False


def modify_expense(data: list, indice: int, new_category: str | None = None, new_value: int | None = None) -> bool:
    """Modifica la categoría y/o el monto de un gasto existente y persiste el cambio.

    Solo actualiza los campos que reciben un valor distinto de None.
    Si ambos parámetros son None, el gasto queda sin cambios pero igual se persiste.

    Args:
        data (list[dict]): Lista completa de gastos cargada previamente.
        indice (int): Índice (base 0) del gasto a modificar.
        new_category (str | None): Nueva categoría. Si es None, se mantiene la actual.
        new_value (int | None): Nuevo monto. Si es None, se mantiene el actual.

    Returns:
        bool: True si se guardó correctamente, False si hubo un error de I/O.
    """
    current_expense = data[indice]

    if new_category:
        current_expense["category"] = new_category

    if new_value:
        current_expense["value"] = new_value

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except (IOError, PermissionError) :
        return False
