from analytics import calcular_resumen_categoria
from crud import leer_historial

def exportar_reporte_general(data):

    resumen = calcular_resumen_categoria(data)
    valor_total = 0

    with open('resumen_general.txt', "w") as f:
        for categoria, valor in resumen.items():
            categoria_normalizada = categoria.strip()
            valor_total += valor
            f.write(f"\n{categoria_normalizada} : {valor}\n")
        f.write(f"\nTotal Gastado {valor_total}")

def exportar_reporte_detallado():
    data = leer_historial()

    with open('resumen_detalado.txt', 'w') as f:
        for item in data: 
            categoria = item['categoria']
            valor = item['valor']
            fecha = item['fecha']
            categoria_normalizada= categoria.strip()
            f.write(f"\n{fecha} | {categoria_normalizada} : {valor}\n")




