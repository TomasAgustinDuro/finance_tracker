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

from src.exports import export_detailed_report, export_general_report

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

def show_filter_tab(data: list) -> None : 
        st.subheader("Filtrado por categoria")

        categorias_disponibles = sorted(list(set(gasto["category"] for gasto in data)))

        categoria_seleccionada = st.selectbox(
            "Selecciona la categoria que deseas analizar: ",
            categorias_disponibles,
            key="filtro_categorias_historial",
        )

        gastos_filtrado = [g for g in data if g["category"] == categoria_seleccionada]

        st.write(
            f"Se encontraron **{len(gastos_filtrado)}** registros para la categoria **{categoria_seleccionada}**"
        )
        st.dataframe(gastos_filtrado, use_container_width=True)

def show_week_table(data:list) -> None:
    st.subheader("Gastos de la ultima semana")

    last_week = get_week_expenses(data)

    if last_week:
            df_last_week = pd.DataFrame(last_week)

            df_last_week['date'] = pd.to_datetime(df_last_week['date']).dt.strftime('%d/%m')
            
            df_last_week = df_last_week.rename(columns={
                "date": "Fecha",
                "category": "Categoría",
                "value": "Monto ($)"
            })

            st.bar_chart(
                data=df_last_week,
                x="Fecha",
                y="Monto ($)",
                color="#2E7D32"
            )

            with st.expander("Ver valores detallados en tabla"):
                st.dataframe(df_last_week, use_container_width=True)

def show_complete_table(data: list) -> None:
        if "mensaje_exito" in st.session_state:
                    st.success(st.session_state.pop("mensaje_exito"))

        st.subheader("Todos tus movimientos")

        record_gasto = get_top_expense_day(data)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="Total Histórico Gastado", value=f"${sum(g['value'] for g in data):,.2f}")
        with col2: 
            if record_gasto:
                fecha_limpia = pd.to_datetime(record_gasto['date']).strftime('%d/%m/%Y')
                st.metric(
                    label="🏆 Día con Mayor Gasto", 
                    value=f"${record_gasto['value']:.2f}",
                    help=f"Récord alcanzado el día {fecha_limpia}" # Un cartelito flotante al pasar el mouse
                )

        st.divider()

        df_gastos = pd.DataFrame(data)
        
        seleccion = st.dataframe(df_gastos, use_container_width=True, on_select="rerun", selection_mode="single-row")

        if seleccion['selection']['rows']:
            indice_elegido = seleccion["selection"]["rows"][0]

            gasto_elegido = data[indice_elegido]

            st.write(f"Has elegido el gasto de: {gasto_elegido["category"]}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Eliminar gasto", use_container_width=True):
                    if delete_expense(indice_elegido, data):
                        st.success("Gasto eliminado exitosamente")
                        st.rerun()
            
            with col2:
                if st.button("Editar gasto", use_container_width=True):
                    st.session_state.editando = True

            if st.session_state.get("editando", False):
                st.divider()
                st.subheader("Modificar los campos del gasto")

                show_menu_modify_expense(data, indice_elegido)   
        else: 
            st.session_state.editando = False

def show_export_detail_table(data:list) -> None:
    st.title("Exportar historial detallado")
    st.write("Presiona el botón para descargar tu reporte")

    if st.button("Generar Reporte"):
        with st.spinner("Compilando datos..."):
            archivo = export_detailed_report(data)

            if archivo:
                st.success("El reporte fue compilado exitosamente")
                st.download_button(
                    label="Descargar historial general",
                    data=archivo,
                    file_name="Historial_general.txt",
                    mime="text/plain",
                )
            else:
                st.warning("Algo ha salido mal")

def show_export_table(data:list) -> None:
    st.title("Exportar historial detallado")
    st.write("Presiona el botón para descargar tu reporte")

    if st.button("Generar Reporte"):
        with st.spinner("Compilando datos..."):
            archivo = export_general_report(data)

            if archivo:
                st.success("El reporte fue compilado exitosamente")
                st.download_button(
                    label="Descargar historial general",
                    data=archivo,
                    file_name="Historial_general.txt",
                    mime="text/plain",
                )
            else:
                st.warning("Algo ha salido mal")

def show_percentages_table(data) -> None:
    st.subheader("Porcentaje de gastos por categoria")

    information = calculate_expense_percentage(data)

    if not information:
            st.warning("No hay datos suficientes para calcular porcentajes")
    else:
            df_porcentajes = pd.DataFrame(
                information.items(), columns=["Categoria", "Porcentaje (%)"]
            )

            st.bar_chart(
                data=df_porcentajes, x="Categoria", y="Porcentaje (%)", color="#FF4B4B"
            )

            with st.expander("Ver valores detallados en tabla"):
                st.dataframe(df_porcentajes, use_container_width=True)

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
                st.session_state["mensaje_exito"] = f"¡Éxito! Se modificó el gasto a '{category_expense_formatted}' por ${value_expense_formatted:.2f}"
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


