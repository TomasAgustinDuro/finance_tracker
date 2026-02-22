from analytics import calculate_summary_by_category


def export_general_report(data):

    summary = calculate_summary_by_category(data)

    if not summary:
        print('No hay información para escribir')

    total_value = 0

    with open("resumen_general.txt", "w") as f:
        for category, value in summary.items():
            normalized_category = category.strip()
            total_value += value
            f.write(f"\n{normalized_category} : {value}\n")
        f.write(f"\nTotal Gastado {total_value}")


def export_detailed_report(data):
    with open("resumen_detalado.txt", "w") as f:
        for item in data:
            category = item["category"]
            value = item["value"]
            date = item["date"]
            normalized_category = category.strip()
            f.write(f"\n{date} | {normalized_category} : {value}\n")
