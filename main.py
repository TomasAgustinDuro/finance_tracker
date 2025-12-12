#Primera versión de prueba
''''
gastostos = []
gasto_total = 0

start = input('¿Desea agregar gastos a su cuenta? SI o NO ')

while start.lower() != "no":
    gasto = int(input('Por favor ingrese su gasto solamente numerico: '))
    if gasto > 0:
        gastos.append(gasto)
    start = input('Si desea finalizar escriba NO, sino utilice ENTER para seguir ')


for gastito in gastos:
    print(gastito)
    gasto_total += gastito
    print('Gasto total',gasto_total)
    
'''
#Segunda prueba

'''

gastos:dict = {}

start = input ('Aprete ENTER para agregar un nuevo gasto')

while start.lower() == '':
    gasto_categoria = input ('Ingrese la categoria de su gasto:  ')
    gasto_valor = int( input('Ingrese el valor del gasto: '))
    if gasto_categoria in gastos:
        if gasto_valor > 0:
            gastos[gasto_categoria] += gasto_valor
    else:
        gastos[gasto_categoria] = gasto_valor
    print('Gasto registrado ✔')
    print(gastos[gasto_categoria])
    start = input('Si desea finalizar ingrese Q o ENTER para seguir')

print('A continuación tu resumen final')
print('Gastos', dict(sorted(gastos.items(), key=lambda item:item[1], reverse=True)))

'''

#Tercera versión

'''
gastos: dict = {}

start = input ('Aprete ENTER para agregar un nuevo gasto.')

while start.lower() == '':
    gasto_categoria = input('Ingrese la categoria de su gasto: ')
    gasto_valor = int(input('Ingrese el valor del gasto: '))
    gasto_categoria_capi=gasto_categoria.capitalize()
    if gasto_categoria_capi in gastos:
        if gasto_valor > 0:
            gastos[gasto_categoria_capi] += gasto_valor
    else:
        gastos[gasto_categoria_capi] = gasto_valor
    print('Gasto registrado')
    start = input('Si desea finalizar ingrese Q o presione ENTER si desea continuar')

print('A continuación tu resumen final')
for clave, valor in gastos.items():
    print(f"\nCategoria:  {clave} | Valor: $ {valor}" )
print(f"\nTotal gastado hasta ahora:$ {sum(gastos.values())}")
'''

#Cuarta versión / Tiene ingreso de categoria, valores y además creacion de un txt mostrando este mismo
from re import S
from typing import Text

'''
Gastos: dict = {}

Start = input ('Apriete ENTER para agregar un nuevo gasto. ')

while Start.lower() == '':
    gasto_categoria = input('Ingrese la categoría de su gasto: ')
    gasto_valor = int(input('Ingrese el valor del gasto: '))
    gasto_categoria_formateado = gasto_categoria.capitalize()

    if gasto_categoria_formateado in Gastos:
        if gasto_valor > 0:
            Gastos[gasto_categoria_formateado] += gasto_valor
    else:
        Gastos[gasto_categoria_formateado] = gasto_valor
    print('Gasto registrado')
    Start = input('Si desea finalizar ingrese Q o presione ENTER si desea continuar')

print('A continuación crearemos un .txt con su resumen')

with open('resumen.txt', 'w', encoding='utf-8') as f:
    for clave, valor in Gastos.items():
        f.write(f"\nCategoria: {clave} | Valor: $ {valor}\n")
    f.write(f"\nTotal Gastado: $ {sum(Gastos.values())}")
'''

#Quinta versión / Lectura del txt antes creado 

'''

Gastos = []

print('Primero cargaremos los gastos ingresados anteriormente')

with open('resumen.txt', 'r') as file:
    for linea in file:
        primero= linea.split('|')
        for elemento in primero:
            elemento_limpio = elemento.strip()
            if ":" in elemento_limpio:               
                categoria, valor = elemento_limpio.split(':', 1)
                categoria = categoria.strip()
                valor = valor.strip()
                if categoria.lower() != 'total gastado':
                    Gastos.append({"categoria": categoria, 'valor': int(valor)})
                else:
                    continue

print(Gastos)

Start = input('Apriete ENTER para agregar un nuevo gasto')

while Start.lower() == '':
    gasto_categoria = input('Ingrese la categoría de su gasto: ')
    gasto_valor = int(input('Ingrese el valor del gasto: '))
    gasto_categoria_formateado = gasto_categoria.capitalize()
    encontrado = False

    for gasto in Gastos:
        if gasto["categoria"] == gasto_categoria_formateado:
            gasto["valor"] += gasto_valor
            encontrado = True

    if encontrado == False:
        Gastos.append({'categoria': gasto_categoria_formateado, 'valor': gasto_valor})

    print('Gasto registrado')
    Start = input('Ingrese la Q si desea finalizar sino apriete ENTER para seguir ')


print('Actualizando documento de texto llamado Resumen.txt')

with open('resumen.txt', "w") as f:
    for gasto in Gastos:
        categoria = gasto['categoria'].strip()
        f.write(f"\n {categoria} : {gasto['valor']}\n")
    f.write(f"\nTotal Gastado: {sum(gasto['valor'] for gasto in Gastos)}")

'''

#Creación de menu y nueva lógica con dos archivos diferentes para diferentes informaciones

Salida = True
Gastos = []

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

#LEER HISTORIAL DETALLADO
def leer_detalle():
    with open('historial.txt', "w") as f:
        for gasto in Gastos:
            categoria = gasto['categoria'].strip()
            f.write(f"\n {categoria} : {gasto['valor']}\n")
    print(Gastos)

#AGREGAR GASTO
def agregar_gasto():
    Start = ''

    while Start.lower() != "q":
        gasto_categoria = input('Ingrese la categoría de su gasto: ')
        gasto_valor = int(input('Ingrese el valor del gasto: '))
        gasto_categoria_formateado = gasto_categoria.capitalize()

        Gastos.append({'categoria': gasto_categoria_formateado, 'valor': gasto_valor})

        print('Gasto registrado')
        print(Gastos)
        Start = input('Ingrese la Q si desea finalizar sino apriete ENTER para seguir ')

    with open('historial.txt', "w") as f:
        for gasto in Gastos:
            categoria = gasto['categoria'].strip()
            f.write(f"\n {categoria} : {gasto['valor']}\n")


def resumen_general():
    resumen = {}
    
    with open('historial.txt', 'r') as file:
        for linea in file:
            primero= linea.split('|')
            for elemento in primero:
                elemento_limpio = elemento.strip()
                if ":" in elemento_limpio:               
                    categoria, valor = elemento_limpio.split(':', 1)
                    categoria = categoria.strip().capitalize()
                    valor = int(valor.strip())
                    resumen[categoria] = resumen.get(categoria, 0) + valor
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
        leer_detalle()
    elif eleccion == "4":
        exportar_reporte()
    elif eleccion == "5":
        continue
        #Borrar gastos
    else:
        Salida = False
