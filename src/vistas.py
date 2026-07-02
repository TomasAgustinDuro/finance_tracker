"""Capa de presentación — componentes Streamlit de la aplicación.

Cada función renderiza una sección o flujo de la UI. Esta capa no contiene
lógica de negocio ni accede al storage directamente: delega cálculos a
`analytics.py` y persistencia a `crud.py`.
"""

from datetime import datetime

import pandas as pd
import streamlit as st

from src.analytics import (
    calculate_expense_percentage,
    calculate_summary_by_category,
    get_top_expense_day,
    get_week_expenses,
)
from src.crud import add_expense, delete_expense, modify_expense
from src.exports import export_detailed_report, export_general_report
from src.validator import validate_category, validate_mount


def show_history(data: list) -> None:
    """Renderiza el historial completo de gastos como tabla Streamlit.

    Mapea las fechas ISO a formato `DD/MM/YYYY` y capitaliza las categorías
    antes de pasarlos a `st.dataframe`. Los ítems sin campo `category` se
    filtran silenciosamente.

    Args:
        data (list[dict]): Lista de gastos con campos `date`, `category` y `value`.
    """
    if not data:
        st.warning("No hay datos para mostrar")
        return

    data_mapeada = [
        {
            "date": datetime.fromisoformat(gasto["date"]).strftime("%d/%m/%Y"),
            "category": gasto["category"].capitalize(),
            "value": gasto["value"],
        }
        for gasto in data
        if "category" in gasto
    ]

    st.dataframe(data_mapeada)


def show_filter_tab(data: list) -> None:
    """Renderiza el tab de filtrado por categoría.

    Muestra un selectbox con las categorías disponibles y una tabla con los
    gastos de la categoría seleccionada, junto con el conteo de registros.

    Args:
        data (list[dict]): Lista de gastos con campo `category`.
    """
    st.subheader("Filtrado por categoria")

    if not data:
        st.warning("No hay datos para mostrar")
        return

    categorias_disponibles = sorted(set(gasto["category"] for gasto in data))

    categoria_seleccionada = st.selectbox(
        "Selecciona la categoria que deseas analizar: ",
        categorias_disponibles,
        key="filtro_categorias_historial",
    )

    gastos_filtrados = [g for g in data if g["category"] == categoria_seleccionada]

    st.write(
    f"Se encontraron **{len(gastos_filtrados)}** registros "
        f"para la categoria **{categoria_seleccionada}**"
    )
    st.dataframe(gastos_filtrados, use_container_width=True)


def show_week_table(data: list) -> None:
    """Renderiza un gráfico de barras con los gastos de los últimos 7 días.

    Obtiene los gastos recientes con `get_week_expenses`, formatea las fechas
    a `DD/MM` para el eje X y muestra un expander con la tabla detallada.
    Si no hay gastos en el período, no renderiza nada.

    Args:
        data (list[dict]): Lista de gastos con campos `date`, `category` y `value`.
    """
    st.subheader("Gastos de la ultima semana")

    last_week = get_week_expenses(data)

    if not last_week:
        return

    df_last_week = pd.DataFrame(last_week)
    df_last_week["date"] = pd.to_datetime(df_last_week["date"]).dt.strftime("%d/%m")
    df_last_week = df_last_week.rename(
        columns={"date": "Fecha", "category": "Categoría", "value": "Monto ($)"}
    )

    st.bar_chart(data=df_last_week, x="Fecha", y="Monto ($)", color="#2E7D32")

    with st.expander("Ver valores detallados en tabla"):
        st.dataframe(df_last_week, use_container_width=True)


def show_complete_table(data: list) -> None:
    """Renderiza la tabla principal de gastos con métricas y acciones inline.

    Muestra el total histórico gastado y el día récord como métricas en la
    cabecera. La tabla tiene selección de fila única; al seleccionar un gasto
    aparecen los botones para eliminar y editar. La edición se gestiona con
    `show_menu_modify_expense` renderizado inline debajo de la tabla.

    Args:
        data (list[dict]): Lista de gastos con campos `date`, `category` y `value`.
    """
    if "mensaje_exito" in st.session_state:
        st.success(st.session_state.pop("mensaje_exito"))

    st.subheader("Todos tus movimientos")

    if not data:
        st.warning("No hay datos para mostrar")
        return

    record_gasto = get_top_expense_day(data)

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(
            label="Total Histórico Gastado",
            value=f"${sum(g['value'] for g in data):,.2f}",
        )
    with metric_col2:
        if record_gasto:
            fecha_limpia = pd.to_datetime(record_gasto["date"]).strftime("%d/%m/%Y")
            st.metric(
                label="🏆 Día con Mayor Gasto",
                value=f"${record_gasto['value']:.2f}",
                help=f"Récord alcanzado el día {fecha_limpia}",
            )

    st.divider()

    df_gastos = pd.DataFrame(data)
    seleccion = st.dataframe(
        df_gastos,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row",
    )

    if seleccion["selection"]["rows"]:
        indice_elegido = seleccion["selection"]["rows"][0]
        gasto_elegido = data[indice_elegido]

        st.write(f"Has elegido el gasto de: {gasto_elegido['category']}")

        action_col1, action_col2 = st.columns(2)

        with action_col1:
            if st.button("Eliminar gasto", use_container_width=True):
                if delete_expense(indice_elegido, data):
                    st.success("Gasto eliminado exitosamente")
                    st.rerun()

        with action_col2:
            if st.button("Editar gasto", use_container_width=True):
                st.session_state.editando = True

        if st.session_state.get("editando", False):
            st.divider()
            st.subheader("Modificar los campos del gasto")
            show_menu_modify_expense(data, indice_elegido)
    else:
        st.session_state.editando = False


def show_export_detail_table(data: list) -> None:
    """Renderiza la sección de exportación del historial detallado.

    Al presionar el botón, genera el reporte con `export_detailed_report` y
    muestra un `st.download_button` para que el usuario descargue el TXT.

    Args:
        data (list[dict]): Lista de gastos a exportar.
    """
    st.title("Exportar historial detallado")
    st.write("Presiona el botón para descargar tu reporte")

    if st.button("Generar reporte detallado"):
        with st.spinner("Compilando datos..."):
            archivo = export_detailed_report(data)

            if archivo:
                st.success("El reporte fue compilado exitosamente")
                st.download_button(
                    label="Descargar historial detallado",
                    data=archivo,
                    file_name="Historial_detallado.txt",
                    mime="text/plain",
                )
            else:
                st.warning("Algo ha salido mal")


def show_export_table(data: list) -> None:
    """Renderiza la sección de exportación del resumen general por categoría.

    Al presionar el botón, genera el reporte con `export_general_report` y
    muestra un `st.download_button` para que el usuario descargue el TXT.

    Args:
        data (list[dict]): Lista de gastos a exportar.
    """
    st.title("Exportar historial completo")
    st.write("Presiona el botón para descargar tu reporte")

    if st.button("Generar reporte"):
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


def show_percentages_table(data: list) -> None:
    """Renderiza un gráfico de barras con el porcentaje de gasto por categoría.

    Calcula los porcentajes con `calculate_expense_percentage` y los muestra
    en un gráfico de barras rojo. Incluye un expander con la tabla de valores
    exactos. Si no hay datos, muestra un aviso.

    Args:
        data (list[dict]): Lista de gastos con campos `category` y `value`.
    """
    st.subheader("Porcentaje de gastos por categoria")

    information = calculate_expense_percentage(data)

    if not information:
        st.warning("No hay datos suficientes para calcular porcentajes")
        return

    df_porcentajes = pd.DataFrame(
        information.items(), columns=["Categoria", "Porcentaje (%)"]
    )

    st.bar_chart(data=df_porcentajes, x="Categoria", y="Porcentaje (%)", color="#FF4B4B")

    with st.expander("Ver valores detallados en tabla"):
        st.dataframe(df_porcentajes, use_container_width=True)


def show_menu_add_expenses() -> None:
    """Renderiza el formulario para agregar un nuevo gasto.

    Valida la categoría con `validate_category` y el monto con `validate_mount`
    antes de llamar a `add_expense`. Si alguno de los dos es inválido, muestra
    un warning y no persiste nada. El formulario se limpia automáticamente
    al enviar (`clear_on_submit=True`).
    """
    with st.form("Carga de gasto", clear_on_submit=True):
        category_expense = st.text_input("Categoria")
        value_expense = st.number_input("Valor ($): ", min_value=0.0, format="%.2f")

        boton_guardar = st.form_submit_button("Guardar gasto")

        if boton_guardar:
            category_expense_formatted = validate_category(category_expense)
            value_expense_formatted = validate_mount(value_expense)

            if not category_expense_formatted or not value_expense_formatted:
                st.warning("Por favor, ingresa un monto o categoria valida")
            else:
                cargado = add_expense(category_expense_formatted, value_expense_formatted)
                if cargado:
                    st.success("Gasto cargado exitosamente")
                else:
                    st.warning("Error al guardar. Intentalo nuevamente.")


def show_menu_modify_expense(data: list, indice: int) -> None:
    """Renderiza el formulario para editar un gasto existente.

    Pre-rellena los campos con los valores actuales del gasto en `indice`.
    Valida ambos campos antes de llamar a `modify_expense`. Si la operación
    es exitosa, guarda el mensaje de confirmación en `session_state` y hace
    `st.rerun()` para que `show_complete_table` lo muestre en el próximo ciclo.

    Args:
        data (list[dict]): Lista completa de gastos.
        indice (int): Índice base-0 del gasto a modificar.
    """
    with st.form("Editar gasto", clear_on_submit=True):
        category_expense = st.text_input("Categoria", value=data[indice]["category"])
        value_expense = st.number_input(
            "Valor ($): ",
            min_value=0.0,
            format="%.2f",
            value=data[indice]["value"],
        )

        boton_guardar = st.form_submit_button("Guardar cambios")

        if boton_guardar:
            category_expense_formatted = validate_category(category_expense)
            value_expense_formatted = validate_mount(value_expense)

            if not category_expense_formatted or not value_expense_formatted:
                st.warning("Valor inválido")
            else:
                modificado = modify_expense(
                    data, indice, category_expense_formatted, value_expense_formatted
                )

                if modificado:
                    st.session_state["mensaje_exito"] = (
                        f"¡Éxito! Se modificó el gasto a '{category_expense_formatted}'"
                        f" por ${value_expense_formatted:.2f}"
                    )
                    st.rerun()
                else:
                    st.warning("Algo ha salido mal, intentalo nuevamente")


def show_summary_cat(data: list) -> dict | None:
    """Calcula y retorna el resumen de gastos por categoría.

    Delega el cálculo a `calculate_summary_by_category`. Si no hay datos,
    muestra un `st.warning` y retorna `None`. El llamador (`main.py`) es
    responsable de renderizar el dict retornado con `st.dataframe`.

    Args:
        data (list[dict]): Lista de gastos con campos `category` y `value`.

    Returns:
        dict[str, float] | None: Diccionario `{categoria: total}` si hay datos,
            `None` si el historial está vacío.
    """
    summary = calculate_summary_by_category(data)

    if not summary:
        st.warning("No hay información para mostrar")
        return None

    return summary
