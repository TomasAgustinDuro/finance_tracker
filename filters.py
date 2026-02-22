def get_unique_categories(data):
    if len(data) == 0:
        return []
    else:
        return set(expense["category"] for expense in data)


def filter_by_category(data, category):
    if len(data) == 0:
        return []
    else:
        return [element for element in data if element["category"] == category]