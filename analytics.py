from datetime import datetime, timedelta

def calculate_expense_percentage(data):
    total_value = 0

    if len(data) == 0:
        return {}

    summary = {}

    for item in data:
        cat = item["category"]
        val = item["value"]
        total_value += item['value']
        summary[cat] = summary.get(cat, 0) + val

    percentages = {}

    for category, value in summary.items():
        percentages[category] = (value / total_value) * 100

    return percentages

def get_week_expenses(data):
    if len(data) == 0:
        return {}

    today = datetime.now()
    week = today - timedelta(days=7)

    last_expenses = [
        last
        for last in data
        if week <= datetime.fromisoformat(last["date"]) <= today
    ]

    if len(last_expenses) == 0:
        print("No hubo gastos los ultimos 7 dias")

    sorted_expenses = sorted(last_expenses, key=lambda item: item["date"], reverse=True)

    return sorted_expenses

def get_top_expense_day(data):
    if not data:
        return {}

    more_expenses = {}

    for item in data:
        more_expenses[item["date"][:10]] = (
            more_expenses.get(item["date"][:10], 0) + item["value"]
        )

    max_date = max(more_expenses, key=more_expenses.get)
    max_value = more_expenses[max_date]

    return {"date": max_date, "value": max_value}

def calculate_summary_by_category(data):
    if not data:
        return{}

    summary = {}
    for item in data:
        summary[item["category"]] = summary.get(item["category"], 0) + item["value"]

    return summary

# Helper
def calculate_daily_average(data):
    last_week = get_week_expenses(data)
    total_week = 0

    if not last_week:
        return 0

    for expense_value in last_week:
        total_week += expense_value["value"]

    return total_week / 7

# Helper
def calculate_historical_daily_average(data):
    days_with_expense = []
    value_expense = 0

    if not data:
        return 0

    for expense_date in data:
        days_with_expense.append(expense_date["date"][:10])

    unique_days = set(days_with_expense)

    for expense in data:
        value_expense += expense["value"]

    average = value_expense / len(unique_days)

    return average
