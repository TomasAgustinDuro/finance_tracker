import json
import os.path
import uuid
from datetime import datetime, timedelta

def leer_historial():

    if os.path.isfile('historial.json'):
        with open('historial.json', "r") as f:
            data = json.load(f)
        return data
    else:
        
       with open('historial.json', 'w', encoding='utf-8') as f:
        json.dump([], f, indent=4, ensure_ascii=False)

        return []

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
 


