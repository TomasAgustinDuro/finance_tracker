import json
import os.path
import uuid
from datetime import datetime


def read_history():
    if os.path.isfile("historial.json"):
        with open("historial.json", "r") as f:
            data = json.load(f)

            for expense in data:
                expense["value"] = int(expense["value"])
        return data
    else:
        with open("historial.json", "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

        return []


# AGREGAR GASTO
def add_expense():
    start = ""

    expenses = read_history()

    while start.lower() != "q":
        category_expense = input("Ingrese la categoría de su gasto: ")
        value_expense = input("Ingrese el value del gasto: ")
        category_expense_formatted = category_expense.capitalize().strip()
        date = datetime.now()
        date_formatted = date.isoformat()

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

        value_expense_formateado = int(value_expense)

        new_expense = {
            "id": uuid.uuid4().hex,
            "category": category_expense_formatted,
            "value": value_expense_formateado,
            "date": date_formatted,
        }

        expenses.append(new_expense)

        print("Gasto registrado")

        start = input("Ingrese la Q si desea finalizar sino apriete ENTER para seguir ")

    with open("historial.json", "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=4, ensure_ascii=False)


def delete_expense():
    expenses = read_history()

    if len(expenses) == 0:
        print("La lista está vacia, es imposible borrar algo")
    else:
        for i, expense in enumerate(expenses, start=1):
            print(
                f"{i}. {expense['category']}: ${expense['value']} - {expense['date'][:10]}"
            )

        index_selection = input("Ingrese el numero del gasto que desea borrar: ")

        if index_selection.isdigit() and int(index_selection) <= len(expenses):
            indice = int(index_selection) - 1

            confirmation = input(
                f"¿Esta seguro que desea eliminar: {expenses[indice]['category']}: ${expenses[indice]['value']} - {expenses[indice]['date'][:10]} Y/N"
            )

            if confirmation.upper() == "Y":
                del expenses[indice]
                print("Gasto eliminado exitosamente")

                with open("historial.json", "w", encoding="utf-8") as f:
                    json.dump(expenses, f, indent=4, ensure_ascii=False)

            else:
                print("No eliminado")

        else:
            print("El value ingresado debe ser un numero")


def modify_expense():
    expenses = read_history()

    if len(expenses) == 0:
        print("La lista esta vacia por ende es imposible modificar gasto")
    else:
        for i, expense in enumerate(expenses, start=1):
            print(
                f"{i}. {expense['category']}: ${expense['value']} - {expense['date'][:10]}"
            )

        index_selection = input("Ingrese el numero del gasto que desea modificar: ")

        if index_selection.isdigit() and 1 <= int(index_selection) <= len(expenses):
            indice = int(index_selection) - 1

            print(
                f"Gasto actual: {expenses[indice]['category']}: ${expenses[indice]['value']}"
            )

            category = input(
                "Ingrese una nueva category (ENTER para mantener la category actual: "
            )
            formatted_category = category.capitalize().strip()
            value = input(
                "Ingrese un nuevo value (ENTER para mantener el value actual: "
            )

            current_expense = expenses[indice]

            new_category = (
                formatted_category if formatted_category != "" else current_expense["category"]
            )
            new_value = (
                int(value)
                if (value != "" and value.isdigit())
                else current_expense["value"]
            )

            print(
                f"\nCambio: [{current_expense['category']}: ${current_expense['value']}] → [{new_category}: ${new_value}]"
            )

            if formatted_category == "" and value == "":
                print("Sin cambios")
            else:
                confirmation = input("¿Confirmar cambio? [Y/N]: ")

                change = False

                if confirmation.upper() == "Y":
                    if (
                        formatted_category.replace(" ", "").isalpha()
                        and formatted_category != ""
                    ):
                        current_expense["category"] = formatted_category
                        change = True

                    if value.isdigit() and value != "":
                        current_expense["value"] = int(value)
                        change = True

                    if change:
                        with open("historial.json", "w", encoding="utf-8") as f:
                            json.dump(expenses, f, indent=4, ensure_ascii=False)

                        print("Gasto modificado exitosamente")

                else:
                    print("Modificación cancelada")

        else:
            print("El value ingresado debe ser un numero")
