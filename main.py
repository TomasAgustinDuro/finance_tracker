import streamlit as st
from src.crud import read_history
from src.vistas import (
    show_menu_add_expenses,
    show_summary_cat,
    show_history,
)
from src.filters import filter_by_category
import pandas as pd
from src.analytics import calculate_expense_percentage, get_week_expenses, get_top_expense_day
from src.exports import export_general_report, export_detailed_report


data = read_history()

st.set_page_config(page_title="Finance tracker", page_icon="💰", layout="centered")

st.sidebar.title("Menu Principal")
opcion = st.sidebar.radio(
    "Selecciona una opción: ",
    [
        "1. Agregar un gasto nuevo",
        "2. Ver resumen por categoria",
        "3. Ver historial completo",
        "4. Exportar historial detallado a TXT (con fechas)",
        "5. Exportar resumen general a TXT9. Ver porcentaje de gastos por categoría",
        "10. Ver gastos de los últimos 7 dias",
        "11. Ver día con mayor gasto",
        "12. Salir",
    ],
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


        st.dataframe(data, use_container_width=True)

    with tab_filtrado:
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

    with tab_porcentajes:
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

    with tab_week: 
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

elif "4. " in opcion:
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

elif "5. " in opcion:
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

# La idea es filtrar por categoria y poder eliminar y editar desde acá
elif "6. " in opcion:
    st.title("Ver gastos")


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

#     elif menu_option == "6":
#         show_menu_delete_expense(data)
#     elif menu_option == "7":
#         show_menu_modify_expense(data)

#     elif menu_option == "11":
#         show_top_expenses(data)

#     else:
#         out = False
