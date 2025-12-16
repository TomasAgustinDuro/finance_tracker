#Creación de menu y nueva lógica con dos archivos diferentes para diferentes informaciones

from datetime import datetime
import json
import os.path
import uuid

Salida = True
#Funciones

def mostrar_menu():
    return input("""
    =====================================
         GESTOR DE GASTOS 🧾
    =====================================

    Elija una opción:

    1) Agregar un nuevo gasto
    2) Ver resumen general de gastos
    3) Ver historial detallado (con fechas)
    4) Exportar reporte a TXT
    5) Borrar un gasto
    6) Salir

    =====================================
    """)

#LEER HISTORIAL
def leer_historial():

    if os.path.isfile('historial.json'):
        with open('historial.json', "r") as f:
            data = json.load(f)
        return data
    else:
        
       with open('historial.json', 'w', encoding='utf-8') as f:
        json.dump([], f, indent=4, ensure_ascii=False)

        return []

 

#MOSTRAR HISTORIAL DETALLADO
def mostrar_historial():
    data = leer_historial()
    print(data)

#AGREGAR GASTO
def agregar_gasto():
    Start = ''

    gastos = leer_historial()

    while Start.lower() != "q":
        gasto_categoria = input('Ingrese la categoría de su gasto: ')
        gasto_valor = input('Ingrese el valor del gasto: ')
        gasto_categoria_formateado = gasto_categoria.capitalize().strip()
        fecha = datetime.now()
        fecha_formateada = fecha.isoformat()

        if gasto_categoria_formateado == '' or not gasto_categoria_formateado.replace(" ", "").isalpha():
            print('Categoria tiene que tener un valor y no puede contener numeros')
            break
        if gasto_valor == '' or not gasto_valor.isdigit():
            print('Valor del gasto tiene que tener contenido y no puede contener letras')
            break

        gasto_valor_formateado = int(gasto_valor)

        nuevo_gasto = {'id': uuid.uuid4().hex,'categoria': gasto_categoria_formateado, 'valor': gasto_valor_formateado, 'fecha': fecha_formateada}

        gastos.append(nuevo_gasto)

        print('Gasto registrado')

        Start = input('Ingrese la Q si desea finalizar sino apriete ENTER para seguir ')

    with open('historial.json', 'w', encoding='utf-8') as f:
        json.dump(gastos, f, indent=4, ensure_ascii=False)


def resumen_general():
    resumen = {}
    
    data = leer_historial()

    for item in data:
        resumen[item['categoria']] = resumen.get(item['categoria'], 0) + int(item['valor'])

    print(resumen)

    return resumen


def exportar_reporte():
    Resumen = resumen_general()


    with open('resumen.txt', "w") as f:
        for categoria, valor in Resumen.items():
            categoria_normalizada = categoria.strip()
            f.write(f"\n {categoria_normalizada} : {valor}\n")
        f.write(f"\nTotal Gastado: {sum(Resumen.values())}")


#Flujo general

while Salida:


    eleccion = mostrar_menu()

    if eleccion == "1":
        agregar_gasto()
    elif eleccion == "2":
        resumen_general()
    elif eleccion == "3":
        mostrar_historial()
    elif eleccion == "4":
        exportar_reporte()
    elif eleccion == "5":
        continue
        #Borrar gastos
    else:
        Salida = False
