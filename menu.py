
def show_menu():
    menu_option = input("""
    =====================================
         GESTOR DE GASTOS 🧾
    =====================================

    Elija una opción:

    1) Agregar un nuevo gasto
    2) Ver resumen general de gastos
    3) Ver historial detallado (con fechas)
    4) Exportar reporte a TXT
    5) Borrar un gasto
    6) Modificar un gasto
    7) Obtener todos los gastos de una categoria
    8) Ver porcentaje de gastos por categoria
    9) Ver gastos de los ultimos 7 dias
    10) Ver dia con mayor gasto
    11) Salir

    =====================================
    """)

    return menu_option

