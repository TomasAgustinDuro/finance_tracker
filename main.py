#Creación de menu y nueva lógica con dos archivos diferentes para diferentes informaciones

from datetime import datetime, timedelta
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
    6) Modificar un gasto
    7) Obtener todos los gastos de una categoria
    8) Salir

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


def borrar_gastos():
    gastos = leer_historial()

    if len(gastos) == 0:
        print('La lista está vacia, es imposible borrar algo')
    else:

        for i, gasto in enumerate(gastos, start=1):
            print(f"{i}. {gasto['categoria']}: ${gasto['valor']} - {gasto['fecha'][:10]}")


        index_seleccion = input('Ingrese el numero del gasto que desea borrar: ')

        if index_seleccion.isdigit() and int(index_seleccion) <= len(gastos):
    
            confirmacion = input(f"¿Esta seguro que desea eliminar: {gastos[int(index_seleccion) - 1]['categoria']}: ${gastos[int(index_seleccion) - 1]['valor']} - {gastos[int(index_seleccion)-1]['fecha'][:10]} Y/N" )

            if confirmacion.upper() == 'Y':
                del gastos[int(index_seleccion) - 1]
                print('Gasto eliminado exitosamente')


                with open('historial.json', 'w', encoding='utf-8') as f:
                    json.dump(gastos, f, indent=4, ensure_ascii=False)

                print(leer_historial())

            else: 
                print('No eliminado')

        else:
            print('El valor ingresado debe ser un numero')

def modificar_gasto():
    gastos = leer_historial()

    if len(gastos) == 0: 
        print('La lista esta vacia por ende es imposible modificar gasto')
    else: 
        for i, gasto in enumerate(gastos, start=1):
            print(f"{i}. {gasto['categoria']}: ${gasto['valor']} - {gasto['fecha'][:10]}")

        index_seleccion = input('Ingrese el numero del gasto que desea modificar: ')

        if index_seleccion.isdigit() and 1 <= int(index_seleccion) <= len(gastos):
            print(f"Gasto actual: {gastos[int(index_seleccion) - 1]['categoria']}: ${gastos[int(index_seleccion)-1]['valor']}")
            
            categoria = input('Ingrese una nueva categoria (ENTER para mantener la categoria actual: ')
            categoria_formateada = categoria.capitalize().strip()
            valor = input('Ingrese un nuevo valor (ENTER para mantener el valor actual: ')

            indice = int(index_seleccion) - 1
            gasto_actual = gastos[indice]

            nueva_categoria = categoria if categoria != '' else gasto_actual['categoria']
            nuevo_valor = int(valor) if (valor != '' and valor.isdigit()) else gasto_actual['valor']

            print(f"\nCambio: [{gasto_actual['categoria']}: ${gasto_actual['valor']}] → [{nueva_categoria}: ${nuevo_valor}]")
            
           
            if categoria_formateada == '' and valor == '':
                print('Sin cambios')
            else:
                confirmacion = input('¿Confirmar cambio? [Y/N]: ')

                hubo_cambio = False

                if confirmacion.upper() == 'Y':
                    if categoria_formateada.replace(" ", "").isalpha() and categoria_formateada != '':
                        gasto_actual['categoria'] = categoria_formateada
                        hubo_cambio = True


                    if valor.isdigit() and valor != '':
                        gasto_actual['valor'] = int(valor)
                        hubo_cambio = True            

                    if hubo_cambio:
                        with open('historial.json', 'w', encoding='utf-8') as f:
                            json.dump(gastos, f, indent=4, ensure_ascii=False)

                        print('Gasto modificado exitosamente')
                
                else: 
                    print('Modificación cancelada')

        
        else:
            print('El valor ingresado debe ser un numero')
            
    
def retornar_por_categoria():
    gastos = leer_historial()

    if len(gastos) == 0:
        print('La lista esta vacia')
    else: 
        categorias_unicas = set(gasto['categoria'] for gasto in gastos)

        print(categorias_unicas)

        categoria_buscada = input('Ingrese la categoria para filtrar: ')

        if categoria_buscada != '' and categoria_buscada != ' ':
            categoria_buscada_formateada = categoria_buscada.capitalize().strip()

            coincidencias = [elemento for elemento in gastos if elemento['categoria'] == categoria_buscada_formateada] 

            if len(coincidencias) > 0:
            

                print(coincidencias)

            else:
                print('No hubo coincidencias encontradas')
        else:
           print('Filtrado cancelado')

        


def porcentaje_gastos():
    data = resumen_general()
    valor_total= 0


    for gasto_valor in data.values():
        valor_total += gasto_valor

    for categoria, valor in data.items():
        print(f'{categoria} representa un {(valor / valor_total) * 100:.1f}% de los gastos totales registrados')

def gasto_7_dias():
    data = leer_historial()

    if len(data) == 0:
        print('No hay data que revisar')

    hoy = datetime.now()
    seven_days = hoy - timedelta(days=7)

    ultimos_gastos = [ultimo for ultimo in data if seven_days <= datetime.fromisoformat(ultimo['fecha']) <= hoy]

    if len(ultimos_gastos) == 0:
        print('No hubo gastos los ultimos 7 dias')

    ordenado = sorted(ultimos_gastos, key=lambda item: item['fecha'], reverse=True)

    print(ordenado)

def pico_gastos():
    data = leer_historial()

    if not data:
        print('No hay data que revisar')

    mas_gastos = {}

    for item in data:
        mas_gastos[item['fecha'][:10]] = mas_gastos.get(item['fecha'][:10], 0) + int(item['valor'])
    

    fecha_max = max(mas_gastos, key=mas_gastos.get)
    valor_max = mas_gastos[fecha_max]

    print(f"El dia con mayor gastos es {fecha_max} con un total de ${valor_max}")


    

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
        borrar_gastos()
    elif eleccion == '6':
        modificar_gasto()
    elif eleccion == '7':
        retornar_por_categoria()
    elif eleccion == '8':
        porcentaje_gastos()
    elif eleccion == '9':
        gasto_7_dias()
    elif eleccion== '10':
        pico_gastos()
        
    else:
        Salida = False
