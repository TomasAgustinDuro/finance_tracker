
def show_menu() -> str:
    """Muestra el menú principal de la aplicación y captura la opción del usuario.

    Returns:
        str: Opción seleccionada por el usuario como string (ej: '1', '2', ..., '12').
    """
    menu_option = input("""
    =====================================
         GESTOR DE GASTOS 🧾
    =====================================

    Elija una opción:

    1) Agregar un nuevo gasto
    2) Ver resumen por categoría
    3) Ver historial completo en consola
    4) Exportar historial detallado a TXT (con fechas)
    5) Exportar resumen general a TXT
    6) Borrar un gasto
    7) Modificar un gasto
    8) Obtener todos los gastos de una categoria
    9) Ver porcentaje de gastos por categoria
    10) Ver gastos de los ultimos 7 dias
    11) Ver dia con mayor gasto
    12) Salir

    =====================================
    """)

    return menu_option

