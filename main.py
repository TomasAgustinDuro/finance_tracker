# Creación de menu y nueva lógica con dos archivos diferentes para diferentes informaciones

from crud import leer_historial, agregar_gasto, modificar_gasto, borrar_gastos
from menu import mostrar_menu
from exports import exportar_reporte_general, exportar_reporte_detallado
from vistas import (
    mostrar_pico_gastos,
    mostrar_porcentajes,
    mostrar_semana,
    mostrar_resumen_categoria,
    mostrar_filtro_categoria
)

Salida = True

# Flujo general

while Salida:
    data = leer_historial()
    eleccion = mostrar_menu()

    if eleccion == "1":
        agregar_gasto()
    elif eleccion == "2":
        mostrar_resumen_categoria(data)
    elif eleccion == "3":
        exportar_reporte_detallado(data)
    elif eleccion == "4":
        exportar_reporte_general(data)
    elif eleccion == "5":
        borrar_gastos()
    elif eleccion == "6":
        modificar_gasto()
    elif eleccion == "7":
        mostrar_filtro_categoria(data)
    elif eleccion == "8":
        mostrar_porcentajes(data)
    elif eleccion == "9":
        mostrar_semana(data)
    elif eleccion == "10":
        mostrar_pico_gastos(data)

    else:
        Salida = False
