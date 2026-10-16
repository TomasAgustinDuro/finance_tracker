"""Punto de entrada de la aplicación Finance Tracker.

Inicializa la configuración de Streamlit, carga el historial desde S3
y enruta cada opción del menú lateral a la vista correspondiente.
"""

import streamlit as st
from src.crud import read_history
from src.vistas import (
    show_menu_add_expenses,
    show_summary_cat,
    show_percentages_table,
    show_week_table,
    show_complete_table,
    show_export_detail_table,
    show_export_table,
    show_filter_tab,
)


data = read_history()

st.set_page_config(page_title="Finance tracker", page_icon="💰", layout="centered")

st.sidebar.title("Menu Principal")
opcion = st.sidebar.radio(
    "Selecciona una opción: ",
    [
        "Agregar un gasto nuevo",
        "Ver resumen por categoria",
        "Ver historial completo",
        "Exportar historial detallado a TXT (con fechas)",
        "Exportar resumen general a TXT"
    ],
)

if "Agregar un gasto nuevo" in opcion:
    st.title("Agregue su gasto")

    show_menu_add_expenses()

elif "Ver resumen por categoria" in opcion:
    st.title("Resumen por categoria")

    resumen = show_summary_cat(data)
    st.dataframe(resumen)

elif "Ver historial completo" in opcion:
    st.title("Ver historial completo")

    if not data:
        st.warning("No hay nada que mostrar")

    tab_completo, tab_filtrado, tab_porcentajes, tab_week = st.tabs(
        [
            "Historial completo",
            "Filtrar por categoria",
            "Porcentaje por categoria",
            "Gastos de la ultima semana",
        ]
    )

    with tab_completo:
        show_complete_table(data)

    with tab_filtrado:
        show_filter_tab(data)

    with tab_porcentajes:
        show_percentages_table(data)

    with tab_week:
        show_week_table(data)

elif "Exportar historial detallado a TXT (con fechas)" in opcion:
    show_export_detail_table(data)

elif "Exportar resumen general a TXT" in opcion:
    show_export_table(data)
