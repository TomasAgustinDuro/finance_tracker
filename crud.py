import json
import os.path
import uuid
from datetime import datetime


def read_history():
    if os.path.isfile("historial.json"):
        try:
            with open("historial.json", "r") as f:
                data = json.load(f)

                for expense in data:
                    expense["value"] = int(expense["value"])
            return data
        except (json.JSONDecodeError, ValueError):
            return []
    else:
        with open("historial.json", "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

        return []

# AGREGAR GASTO
def add_expense(category_expense_formatted, value_expense_formatted):

    expenses = read_history()

    new_expense = {
        "id": uuid.uuid4().hex,
        "category": category_expense_formatted,
        "value": value_expense_formatted,
        "date": datetime.now().isoformat(),
    }

    try:
        expenses.append(new_expense)

        with open("historial.json", "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=4, ensure_ascii=False)

        return True

    except Exception:
        return False


def delete_expense(indice, data):
    try:
        del data[indice]
        with open("historial.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return True
    except Exception:
        return False

def modify_expense(data, indice, new_category=None, new_value=None):
    current_expense = data[indice]

    if new_category:
        current_expense['category'] = new_category

    if new_value:
        current_expense['value'] = new_value
    
    try:
        with open("historial.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False

   

    