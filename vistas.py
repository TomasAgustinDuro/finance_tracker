from analytics import (
    porcentaje_gastos,
    pico_gastos,
    calcular_resumen_categoria,
    gasto_7_dias,
)

from filters import obtener_categorias, filtrar_por_categoria


def mostrar_historial(data):
    for gasto in data:
        print(f"{gasto['fecha'][:10]} - {gasto['categoria']}: ${gasto['valor']}")


def mostrar_porcentajes(data):
    informacion = porcentaje_gastos(data)

    for categoria, valor in informacion.items():
        print(
            f"{categoria} representa un {valor:.1f}% de los gastos totales registrados"
        )


def mostrar_pico_gastos(data):
    values = pico_gastos(data)

    print(
        f"El dia con mayor gastos es {values['fecha']} con un total de ${values['valor']}"
    )


def mostrar_resumen_categoria(data):
    summary = calcular_resumen_categoria(data)

    for categoria, valor in summary.items():
        print(f"{categoria}: {valor}")


def mostrar_semana(data):
    week = gasto_7_dias(data)

    if not week:
        print("No hubo gastos en los últimos dias")
    else:
        for gasto in week:
            print(f"{gasto['fecha'][:10]} - {gasto['categoria']}: ${gasto['valor']}")


def mostrar_filtro_categoria(data):
    categorias = obtener_categorias(data)

    for categoria in categorias:
        print(categoria)

    categoria = input("Ingrese la categoria para filtrar: ")

    if categoria.strip() == "":
        print("Campo categoria vacio")
        return

    categoria_formateada = categoria.capitalize().strip()

    resultado = filtrar_por_categoria(data, categoria_formateada)

    if len(resultado) > 0:
        for gasto in resultado:
            print(f"{gasto['fecha'][:10]} - {gasto['categoria']}: ${gasto['valor']}")
    else:
        print("No hubo coincidencias encontradas")
