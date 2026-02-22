from analytics import calculate_expense_percentage, get_top_expense_day, calculate_summary_by_category, get_week_expenses

from filters import get_unique_categories, filter_by_category


def show_history(data):
    for expense in data:
        print(f"{expense['date'][:10]} - {expense['category']}: ${expense['value']}")


def show_percentage(data):
    information = calculate_expense_percentage(data)

    for category, value in information.items():
        print(
            f"{category} representa un {value:.1f}% de los expenses totales registrados"
        )


def show_top_expenses(data):
    values = get_top_expense_day(data)

    print(
        f"El dia con mayor expenses es {values['date']} con un total de ${values['value']}"
    )


def show_summary_cat(data):
    summary = calculate_summary_by_category(data)

    for category, value in summary.items():
        print(f"{category}: {value}")


def show_week(data):
    week = get_week_expenses(data)

    if not week:
        print("No hubo expenses en los últimos dias")
    else:
        for expense in week:
            print(f"{expense['date'][:10]} - {expense['category']}: ${expense['value']}")


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
            print(f"{expense['date'][:10]} - {expense['category']}: ${expense['value']}")
    else:
        print("No hubo coincidencias encontradas")
