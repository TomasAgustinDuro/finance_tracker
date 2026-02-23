from analytics import (
    calculate_expense_percentage,
    get_top_expense_day,
    calculate_summary_by_category,
    get_week_expenses,
)

from crud import add_expense, delete_expense, modify_expense

from filters import get_unique_categories, filter_by_category


def show_history(data):
    for expense in data:
        print(f"{expense['date'][:10]} - {expense['category']}: ${expense['value']}")


def show_percentage(data):
    information = calculate_expense_percentage(data)

    if not information:
        print("No hay información con la que calcualr los porcentajes")

    for category, value in information.items():
        print(
            f"{category} representa un {value:.1f}% de los expenses totales registrados"
        )

def show_top_expenses(data):
    values = get_top_expense_day(data)

    if not values:
        print("No hay información para mostrar")

    print(
        f"El dia con mayor expenses es {values['date']} con un total de ${values['value']}"
    )


def show_menu_add_expenses():
    start = ""

    while start.lower() != "q":
        category_expense = input("Ingrese la categoría de su gasto: ")
        value_expense = input("Ingrese el value del gasto: ")
        category_expense_formatted = category_expense.capitalize().strip()

        if (
            category_expense_formatted == ""
            or not category_expense_formatted.replace(" ", "").isalpha()
        ):
            print("category tiene que tener un value y no puede contener numeros")
            continue
        if value_expense == "" or not value_expense.isdigit():
            print(
                "value del gasto tiene que tener contenido y no puede contener letras"
            )
            continue

        value_expense_formatted = int(value_expense)

        cargado = add_expense(category_expense_formatted, value_expense_formatted)

        if cargado:
            print("Gasto cargado correctamente")
        else:
            print("Hubo un error al cargar su gasto")

        start = input("Ingrese Q para salir o ENTER para continuar: ")


def show_menu_delete_expense(data):
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


def show_menu_modify_expense(data):
    if len(data) == 0:
        print("La lista esta vacia, es imposible modificar gasto")
    else:
        for i, expense in enumerate(data, start=1):
            print(
                f"{i}. {expense['category']}: ${expense['value']} - {expense['date'][:10]}"
            )

        index_selection = input("Ingrese el numero del gasto que desea modificar: ")

        if index_selection.isdigit() and 1 <= int(index_selection) <= len(data):
            indice = int(index_selection) - 1

            print(f"Gasto actual: {data[indice]['category']}: ${data[indice]['value']}")

            category = input(
                "Ingrese una nueva categoria (ENTER para mantener la category actual: "
            )
            formatted_category = category.capitalize().strip()
            value = input(
                "Ingrese un nuevo value (ENTER para mantener el value actual: "
            )

            new_cat = (
                formatted_category
                if (
                    formatted_category.replace(" ", "").isalpha()
                    and formatted_category != ""
                )
                else None
            )

            new_val = int(value) if value.isdigit() and value != "" else None

            if not new_cat and not new_val:
                print("No hubo cambios validos")
                return

            preview_cat = new_cat if new_cat else data[indice]["category"]
            preview_value = new_val if new_val else data[indice]["value"]

            print(
                f"\nCambio: [{data[indice]['category']}: ${data[indice]['value']}] → [{preview_cat}: ${preview_value}]"
            )

            confirmation = input("¿Confirmar cambio? [Y/N]: ")

            if confirmation.upper() == "Y":
                success = modify_expense(data, indice, new_cat, new_val)

                if success:
                    print("Cambio realizado satisfactoriamente")
                else:
                    print("Error al hacer el cambio")

        else:
            print("Debe ingresar un valor númerico")


def show_summary_cat(data):
    summary = calculate_summary_by_category(data)

    if not summary:
        print("No hay información para mostrar")

    for category, value in summary.items():
        print(f"{category}: {value}")


def show_week(data):
    week = get_week_expenses(data)

    if not week:
        print("No hubo gastos en los últimos dias")
    else:
        for expense in week:
            print(
                f"{expense['date'][:10]} - {expense['category']}: ${expense['value']}"
            )


def show_filter_cat(data):
    categories = get_unique_categories(data)

    for category in categories:
        print(category)

    category = input("Ingrese la category para filtrar: ")

    if category.strip() == "":
        print("Campo category vacio")
        return

    formatted_category = category.capitalize().strip()

    result = filter_by_category(data, formatted_category)

    if len(result) > 0:
        for expense in result:
            print(
                f"{expense['date'][:10]} - {expense['category']}: ${expense['value']}"
            )
    else:
        print("No hubo coincidencias encontradas")
