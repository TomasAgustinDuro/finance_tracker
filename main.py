import streamlit as st
from src.crud import read_history
from src.vistas import (
    show_menu_add_expenses,
    show_summary_cat,
    show_history
)


data = read_history()

st.set_page_config(page_title="Finance tracker", page_icon="💰", layout="centered")

st.sidebar.title("Menu Principal")
opcion = st.sidebar.radio(
    "Selecciona una opción: ", [
        "1. Agregar un gasto nuevo",
        "2. Ver resumen por categoria",
        "3. Ver historial completo",
        "4. Exportar historial detallado a TXT (con fechas)",
        "5. Exportar resumen general a TXT",
        "6. Borrar un gasto",
        "7. Modificar un gasto",
        "8. Obtener todos los gastos de una categoria",
        "9. Ver porcentaje de gastos por categoría",
        "10. Ver gastos de los últimos 7 dias",
        "11. Ver día con mayor gasto",
        "12. Salir"
    ]
)

if "1. " in opcion:
    st.title("Agregue su gasto")

    show_menu_add_expenses()

elif "2. " in opcion:
    st.title("Resumen por categoria")

    resumen = show_summary_cat(data)
    st.dataframe(resumen)

elif "3. " in opcion: 
    st.title("Ver historial completo")

    resumen = show_history(data)

    st.dataframe(resumen)
# # Creación de menu y nueva lógica con dos archivos diferentes para diferentes informaciones

# from crud import read_history
# from menu import show_menu
# from exports import export_detailed_report, export_general_report
# from vistas import (
#     show_history,
#     show_menu_add_expenses,
#     show_menu_delete_expense,
#     show_menu_modify_expense,
#     show_top_expenses,
#     show_percentage,
#     show_week,
#     show_summary_cat,
#     show_filter_cat,
# )

# out = True

# # Flujo general

# while out:
#     data = read_history()
#     menu_option = show_menu()

#     if menu_option == "1":
#         show_menu_add_expenses()
#     elif menu_option == "2":
#         show_summary_cat(data)
#     elif menu_option == "3":
#         show_history(data)
#     elif menu_option == "4":
#         export_detailed_report(data)
#     elif menu_option == "5":
#         export_general_report(data)
#     elif menu_option == "6":
#         show_menu_delete_expense(data)
#     elif menu_option == "7":
#         show_menu_modify_expense(data)
#     elif menu_option == "8":
#         show_filter_cat(data)
#     elif menu_option == "9":
#         show_percentage(data)
#     elif menu_option == "10":
#         show_week(data)
#     elif menu_option == "11":
#         show_top_expenses(data)

#     else:
#         out = False
