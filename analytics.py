from datetime import datetime, timedelta


def porcentaje_gastos(data):
    valor_total= 0
    print(data)
    resumen = {}
    for item in data:
        valor_total += item["valor"]
    
    for item in data: 
        cat = item['categoria']
        val = item['valor']
        
        if cat in resumen:
            resumen[cat] += val
        else: 
            resumen[cat] = val

    for categoria, valor in resumen.items():
        print(f'{categoria} representa un {(valor / valor_total) * 100:.1f}% de los gastos totales registrados')
    
def gasto_7_dias(data):
    if len(data) == 0:
        print('No hay data que revisar')

    hoy = datetime.now()
    seven_days = hoy - timedelta(days=7)

    ultimos_gastos = [ultimo for ultimo in data if seven_days <= datetime.fromisoformat(ultimo['fecha']) <= hoy]

    if len(ultimos_gastos) == 0:
        print('No hubo gastos los ultimos 7 dias')

    ordenado = sorted(ultimos_gastos, key=lambda item: item['fecha'], reverse=True)

    return ordenado

def pico_gastos(data):
    if not data:
        print('No hay data que revisar')

    mas_gastos = {}

    for item in data:
        mas_gastos[item['fecha'][:10]] = mas_gastos.get(item['fecha'][:10], 0) + int(item['valor'])
    

    fecha_max = max(mas_gastos, key=mas_gastos.get)
    valor_max = mas_gastos[fecha_max]

    print(f"El dia con mayor gastos es {fecha_max} con un total de ${valor_max}")


def calcular_resumen_categoria(data):
    resumen = {}
    for item in data:
        resumen[item['categoria']] = resumen.get(item['categoria'], 0) + int(item['valor']) 
    print(resumen)
    return resumen

def promedio_diario(data):
    ultimos_siete = gasto_7_dias(data)
    total_siete_dias = 0

    if not ultimos_siete:
        return 0

    for gasto_valor in ultimos_siete:
        total_siete_dias += gasto_valor['valor'] 

    return total_siete_dias/7

def promedio_historico_diario(data):
    dias_con_gasto=[]
    gastos_valor = 0

    if not data: 
        return 0

    for gasto_fecha in data:
        dias_con_gasto.append(gasto_fecha['fecha'][:10])
        
    dias_unicos = set(dias_con_gasto)
    
    for gasto in data:
        gastos_valor += gasto['valor']

    promedio = gastos_valor / len(dias_unicos)

    return promedio

    
    
