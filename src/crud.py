"""Capa de persistencia del historial de gastos.

Responsable exclusivamente de leer y escribir a través de S3StorageService.
Ninguna otra capa debe acceder al storage directamente.
Usa lazy initialization para no instanciar el cliente S3 al momento del import,
lo que facilita el testing y evita fallos por variables de entorno ausentes.
"""

import json
import uuid
import logging
from datetime import datetime
from src.storage.s3_storage import S3StorageService


_storage_instance = None


def get_storage() -> S3StorageService:
    """Retorna la instancia singleton de S3StorageService (lazy initialization).

    Crea la instancia la primera vez que se llama y la reutiliza en las
    siguientes. Esto evita conectar con AWS al momento del import del módulo,
    lo que permite mockear el cliente en tests sin parchear a nivel de módulo.

    Returns:
        S3StorageService: Instancia activa del cliente de S3.
    """
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = S3StorageService()
    return _storage_instance


def read_history() -> list:
    """Lee y retorna el historial completo de gastos desde S3.

    Convierte el campo `value` de cada gasto a `float` para garantizar
    consistencia de tipos independientemente del formato almacenado en S3.
    En caso de cualquier error (red, credenciales, JSON inválido), retorna
    una lista vacía sin propagar la excepción hacia la UI.

    Returns:
        list[dict]: Lista de gastos. Cada gasto contiene los campos
            `id` (str), `category` (str), `value` (float) y `date` (str ISO 8601).
            Retorna `[]` si el historial está vacío o si ocurre un error.
    """
    try:
        storage = get_storage()
        file = storage.read_file()

        if file:
            for expense in file:
                expense["value"] = float(expense["value"])
            return file
    except Exception as e:
        logging.error(f"Error al leer el historial desde S3: {e}")
        return []

    return []


def add_expense(category_expense_formatted: str, value_expense_formatted: float) -> bool:
    """Agrega un nuevo gasto al historial y lo persiste en S3.

    Genera automáticamente un `id` único (UUID hex) y la `date` con la
    fecha/hora actual en formato ISO 8601. Lee el historial existente,
    agrega el nuevo ítem al final y sobreescribe el objeto en S3.

    Args:
        category_expense_formatted (str): Categoría ya validada, capitalizada
            y sin espacios sobrantes (ej: `"Comida"`).
        value_expense_formatted (float): Monto del gasto, positivo y mayor a cero.

    Returns:
        bool: `True` si el gasto se guardó correctamente en S3,
            `False` si hubo un error de I/O.
    """
    expenses = read_history()

    new_expense = {
        "id": uuid.uuid4().hex,
        "category": category_expense_formatted,
        "value": value_expense_formatted,
        "date": datetime.now().isoformat(),
    }

    try:
        storage = get_storage()
        expenses.append(new_expense)
        response = storage.save_file(expenses)
        return bool(response)
    except Exception as e:
        logging.error(f"Error al agregar gasto en S3: {e}")
        return False


def delete_expense(indice: int, data: list) -> bool:
    """Elimina un gasto del historial por su índice y persiste el resultado en S3.

    Modifica `data` in-place eliminando el elemento en `indice` y luego
    sobreescribe el historial completo en S3.

    Args:
        indice (int): Índice base-0 del gasto a eliminar dentro de `data`.
        data (list[dict]): Lista completa de gastos cargada previamente.

    Returns:
        bool: `True` si se eliminó y guardó correctamente, `False` si el índice
            está fuera de rango o si hubo un error de I/O.
    """
    try:
        del data[indice]
        storage = get_storage()
        response = storage.save_file(data)
        return bool(response)
    except Exception as e:
        logging.error(f"Error al eliminar gasto en S3: {e}")
        return False


def modify_expense(
    data: list,
    indice: int,
    new_category: str | None = None,
    new_value: float | None = None,
) -> bool:
    """Modifica la categoría y/o el monto de un gasto existente y persiste el cambio.

    Solo actualiza los campos que reciben un valor distinto de `None`.
    Si ambos parámetros son `None`, el gasto queda sin cambios pero
    igual se persiste (no-op útil para forzar una re-escritura en S3).

    Args:
        data (list[dict]): Lista completa de gastos cargada previamente.
        indice (int): Índice base-0 del gasto a modificar.
        new_category (str | None): Nueva categoría. Si es `None`, se mantiene la actual.
        new_value (float | None): Nuevo monto. Si es `None`, se mantiene el actual.

    Returns:
        bool: `True` si se guardó correctamente en S3, `False` si hubo un error de I/O.
    """
    current_expense = data[indice]

    if new_category:
        current_expense["category"] = new_category

    if new_value:
        current_expense["value"] = new_value

    try:
        storage = get_storage()
        response = storage.save_file(data)
        return bool(response)
    except Exception as e:
        logging.error(f"Error al modificar gasto en S3: {e}")
        return False
