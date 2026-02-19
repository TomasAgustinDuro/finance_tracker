#Creación de menu y nueva lógica con dos archivos diferentes para diferentes informaciones

from crud import leer_historial, agregar_gasto, modificar_gasto, borrar_gastos
from menu import mostrar_menu
from exports import exportar_reporte_general, exportar_reporte_detallado
from analytics import pico_gastos, gasto_7_dias, porcentaje_gastos, calcular_resumen_categoria
from vistas import mostrar_historial
from filters import retornar_por_categoria

Salida = True
#Funciones

data = leer_historial()

#Flujo general

while Salida:

    eleccion = mostrar_menu()

    if eleccion == "1":
        agregar_gasto()
    elif eleccion == "2":
        calcular_resumen_categoria(data)
    elif eleccion == "3":
        exportar_reporte_detallado()
    elif eleccion == "4":
        exportar_reporte_general(data)
    elif eleccion == "5":
        borrar_gastos()
    elif eleccion == '6':
        modificar_gasto()
    elif eleccion == '7':
        retornar_por_categoria()
    elif eleccion == '8':
        porcentaje_gastos(data)
    elif eleccion == '9':
        gasto_7_dias(data)
    elif eleccion== '10':
        pico_gastos(data)
        
    else:        Salida = False
