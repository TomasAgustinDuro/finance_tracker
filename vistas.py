"""Capa de presentación y coordinación de flujos de usuario.

Recibe datos ya cargados y procesados, los muestra en consola, y gestiona
los inputs interactivos para agregar, borrar y modificar gastos.
No accede a archivos directamente — delega toda persistencia a crud.py.
"""

from analytics import (
    calculate_expense_percentage,
    get_top_expense_day,
    calculate_summary_by_category,
    get_week_expenses,
)

from crud import add_expense, delete_expense, modify_expense

from filters import get_unique_categories, filter_by_category

from validator import validate_category, validate_mount


def show_history(data: list) -> None:
    """Imprime en consola el historial completo de gastos.

    Formato de cada línea: 'YYYY-MM-DD - CATEGORIA: $MONTO'

    Args:
        data (list[dict]): Lista de gastos con campos 'date', 'category' y 'value'.

    Returns:
        None
    """
    for expense in data:
        print(f"{expense['date'][:10]} - {expense['category']}: ${expense['value']}")


def show_percentage(data: list) -> None:
    """Imprime en consola el porcentaje que representa cada categoría sobre el total gastado.

    Args:
        data (list[dict]): Lista de gastos con campos 'category' y 'value'.

    Returns:
        None
    """
    information = calculate_expense_percentage(data)

    if not information:
        print("No hay información con la que calcualr los porcentajes")

    for category, value in information.items():
        print(
            f"{category} representa un {value:.1f}% de los expenses totales registrados"
        )

def show_top_expenses(data: list) -> None:
    """Imprime en consola el día con mayor gasto acumulado del historial.

    Args:
        data (list[dict]): Lista de gastos con campos 'date' y 'value'.

    Returns:
        None
    """
    values = get_top_expense_day(data)

    if not values:
        print("No hay información para mostrar")
        return

    print(
        f"El dia con mayor expenses es {values['date']} con un total de ${values['value']}"
    )


def show_menu_add_expenses() -> None:
    """Flujo interactivo para agregar uno o más gastos nuevos.

    Solicita al usuario categoría y monto, valida ambos campos y llama a add_expense.
    El loop continúa hasta que el usuario ingresa 'Q' para salir.

    Returns:
        None
    """
    start = ""

    while start.lower() != "q":
        category_expense = input("Ingrese la categoría de su gasto: ")
        value_expense = input("Ingrese el value del gasto: ")
        category_expense_formatted = category_expense.capitalize().strip()

        category_expense_formatted = validate_category(category_expense)
        value_expense_formatted = validate_mount(value_expense)

        cargado = add_expense(category_expense_formatted, value_expense_formatted)

        if cargado:
            print("Gasto cargado correctamente")
        else:
            print("Hubo un error al cargar su gasto")

        start = input("Ingrese Q para salir o ENTER para continuar: ")


def show_menu_delete_expense(data: list) -> None:
    """Flujo interactivo para eliminar un gasto existente del historial.

    Lista los gastos numerados, solicita al usuario el número del gasto a eliminar
    y pide confirmación antes de ejecutar el borrado.

    Args:
        data (list[dict]): Lista de gastos cargada previamente desde el historial.

    Returns:
        None
    """
    if len(data) == 0:
        return print("No hay información para mostrar")
    else:
        for i, expense in enumerate(data, start=1):
            print(
                f"{i}. {expense['category']}: ${expense['value']} - {expense['date'][:10]}"
            )

    index_selection = input("Ingrese el numero del gasto que desea borrar: ")

    if index_selection.isdigit() and int(index_selection) <= len(data):
        indice = int(index_selection) - 1

        confirmation = input(
            f"¿Esta seguro que desea eliminar: {data[indice]['category']}: ${data[indice]['value']} - {data[indice]['date'][:10]} Y/N"
        )

        if confirmation.upper() == "Y":
            success = delete_expense(indice, data)

            if success:
                print("Gasto eliminado exitosamente")
            else:
                print("Error al eliminar")
        else:
            print("Gasto no eliminado")
    else:
        print("El valor ingresado, debe ser un numero")

def process_expense_modification(gastos: list, indice: str) -> None:
     if indice.isdigit() and 1 <= int(indice) <= len(gastos):
            indice = int(indice) - 1
            
            print(f"Gasto actual: {gastos[indice]['category']}: ${gastos[indice]['value']}")

            category = input(
                "Ingrese una nueva categoria (ENTER para mantener la category actual: "
            )
           
            value = input(
                "Ingrese un nuevo value (ENTER para mantener el value actual: "
            )

            new_cat = validate_category(category)

            new_val = validate_mount(value)

            if not new_cat and not new_val:
                print("No hubo cambios validos")
                return

            preview_cat = new_cat if new_cat else gastos[indice]["category"]
            preview_value = new_val if new_val else gastos[indice]["value"]

            print(
                f"\nCambio: [{gastos[indice]['category']}: ${gastos[indice]['value']}] → [{preview_cat}: ${preview_value}]"
            )

            confirmation = input("¿Confirmar cambio? [Y/N]: ")

            if confirmation.upper() == "Y":
                success = modify_expense(gastos, indice, new_cat, new_val)

                if success:
                    print("Cambio realizado satisfactoriamente")
                else:
                    print("Error al hacer el cambio")
            else:
                return


def show_menu_modify_expense(data: list) -> None:
    """Flujo interactivo para modificar la categoría y/o el monto de un gasto existente.

    Lista los gastos numerados, solicita el número del ítem a modificar, permite cambiar
    uno o ambos campos, muestra un preview del cambio y pide confirmación antes de persistir.

    Args:
        data (list[dict]): Lista de gastos cargada previamente desde el historial.

    Returns:
        None
    """
    if len(data) == 0:
        print("La lista esta vacia, es imposible modificar gasto")
    else:
        #Muestra los gastos
        for i, expense in enumerate(data, start=1):
            print(
                f"{i}. {expense['category']}: ${expense['value']} - {expense['date'][:10]}"
            )

        #Pide indicar el gasto a modificar
        index_selection = input("Ingrese el numero del gasto que desea modificar: ")

        #Valida la integridad del index-selection   
        process_expense_modification(data, index_selection)

        


def show_summary_cat(data: list) -> None:
    """Imprime en consola el total gastado agrupado por categoría.

    Args:
        data (list[dict]): Lista de gastos con campos 'category' y 'value'.

    Returns:
        None
    """
    summary = calculate_summary_by_category(data)

    if not summary:
        print("No hay información para mostrar")

    for category, value in summary.items():
        print(f"{category}: {value}")


def show_week(data: list) -> None:
    """Imprime en consola los gastos de los últimos 7 días, del más reciente al más antiguo.

    Args:
        data (list[dict]): Lista de gastos con campos 'date', 'category' y 'value'.

    Returns:
        None
    """
    week = get_week_expenses(data)

    if not week:
        print("No hubo gastos en los últimos dias")
    else:
        for expense in week:
            print(
                f"{expense['date'][:10]} - {expense['category']}: ${expense['value']}"
            )


def show_filter_cat(data: list) -> None:
    """Flujo interactivo para filtrar y mostrar gastos de una categoría específica.

    Lista las categorías disponibles, solicita al usuario que elija una y muestra
    todos los gastos que pertenecen a esa categoría.

    Args:
        data (list[dict]): Lista de gastos con campos 'date', 'category' y 'value'.

    Returns:
        None
    """
    categories = get_unique_categories(data)

    for category in categories:
        print(category)

    category = input("Ingrese la category para filtrar: ")

    formatted_category = validate_category(category)

    result = filter_by_category(data, formatted_category)

    if len(result) > 0:
        for expense in result:
            print(
                f"{expense['date'][:10]} - {expense['category']}: ${expense['value']}"
            )
    else:
        print("No hubo coincidencias encontradas")
