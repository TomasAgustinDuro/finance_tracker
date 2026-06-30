"""Capa de presentación y coordinación de flujos de usuario.

Recibe datos ya cargados y procesados, los muestra en consola, y gestiona
los inputs interactivos para agregar, borrar y modificar gastos.
No accede a archivos directamente — delega toda persistencia a crud.py.
"""

from src.analytics import (
    calculate_expense_percentage,
    get_top_expense_day,
    calculate_summary_by_category,
    get_week_expenses,
)
from datetime import datetime

from src.crud import add_expense, delete_expense, modify_expense

from src.filters import get_unique_categories, filter_by_category

from src.validator import validate_category, validate_mount

import streamlit as st


def show_history(data: list) -> None:
    """Imprime en consola el historial completo de gastos.

    Formato de cada línea: 'YYYY-MM-DD - CATEGORIA: $MONTO'

    Args:
        data (list[dict]): Lista de gastos con campos 'date', 'category' y 'value'.

    Returns:
        None
    """
    if not data:
        st.warning("No hay datos para mostrar")

    data_mapeada = [
        {'date': datetime.fromisoformat(gasto['date']).strftime('%d/%m/%Y'),
        'category':gasto['category'].capitalize(),
        'value': gasto['value']
        }
        for gasto in data
        if 'category' in gasto
    ]
    

    st.dataframe(data_mapeada)


def show_menu_add_expenses() -> None:
    """Flujo interactivo para agregar uno o más gastos nuevos.

    Solicita al usuario categoría y monto, valida ambos campos y llama a add_expense.
    El loop continúa hasta que el usuario ingresa 'Q' para salir.

    Returns:
        None
    """

    with st.form("Carga de gasto", clear_on_submit=True):
        category_expense = st.text_input("Categoria")
        value_expense = st.number_input("Valor ($): ", min_value=0, format="%.2f")

        boton_guardar = st.form_submit_button("Guardar gasto")

    category_expense_formatted = category_expense.capitalize().strip()

    if boton_guardar:
        category_expense_formatted = validate_category(category_expense)
        value_expense_formatted = validate_mount(value_expense)

        cargado = add_expense(category_expense_formatted, value_expense_formatted)

        if cargado:
            st.success(
                f"¡Éxito! Se registraron ${value_expense_formatted:.2f} en la categoría '{category_expense}'."
            )
        else:
            st.warning("Por favor, ingresa un monto o categoria valida")


def show_menu_modify_expense(data: list, indice: int) -> None:
    """Flujo interactivo para modificar la categoría y/o el monto de un gasto existente.

    Lista los gastos numerados, solicita el número del ítem a modificar, permite cambiar
    uno o ambos campos, muestra un preview del cambio y pide confirmación antes de persistir.

    Args:
        data (list[dict]): Lista de gastos cargada previamente desde el historial.

    Returns:
        None
    """
    with st.form("Editar gasto", clear_on_submit=True):
        category_expense = st.text_input("Categoria", value=data[indice]['category'])
        value_expense = st.number_input("Valor ($): ", min_value=0, format="%.2f", value=data[indice]['value'])
        
        boton_guardar = st.form_submit_button("Guardar cambios")

        if boton_guardar: 
            category_expense_formatted = validate_category(category_expense)
            value_expense_formatted = validate_mount(value_expense)

            modificado = modify_expense(data, indice, category_expense_formatted, value_expense_formatted)

            if modificado: 
                st.success(f"¡Exito! Se modificó el gasto {category_expense_formatted}, con valor ${value_expense_formatted}")
                st.rerun()
            else: 
                st.warning("Algo ha salido mal, intentalo nuevamente")
            

def show_summary_cat(data: list) -> None:
    """Imprime en consola el total gastado agrupado por categoría.

    Args:
        data (list[dict]): Lista de gastos con campos 'category' y 'value'.

    Returns:
        None
    """
    summary = calculate_summary_by_category(data)

    if not summary:
        st.warning("No hay información para mostrar")
        return

    return summary


