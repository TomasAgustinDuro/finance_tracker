from datetime import datetime, timedelta


def porcentaje_gastos(data):
    valor_total = 0

    if len(data) == 0:
        print("No hay data que revisar")
        return {}

    resumen = {}

    for item in data:
        cat = item["categoria"]
        val = item["valor"]
        valor_total += item['valor']
        resumen[cat] = resumen.get(cat, 0) + val

    porcentajes = {}

    for categoria, valor in resumen.items():
        porcentajes[categoria] = (valor / valor_total) * 100

    return porcentajes


def gasto_7_dias(data):
    if len(data) == 0:
        print("No hay data que revisar")

    hoy = datetime.now()
    seven_days = hoy - timedelta(days=7)

    ultimos_gastos = [
        ultimo
        for ultimo in data
        if seven_days <= datetime.fromisoformat(ultimo["fecha"]) <= hoy
    ]

    if len(ultimos_gastos) == 0:
        print("No hubo gastos los ultimos 7 dias")

    ordenado = sorted(ultimos_gastos, key=lambda item: item["fecha"], reverse=True)

    return ordenado


def pico_gastos(data):
    if not data:
        print("No hay data que revisar")

    mas_gastos = {}

    for item in data:
        mas_gastos[item["fecha"][:10]] = (
            mas_gastos.get(item["fecha"][:10], 0) + item["valor"]
        )

    fecha_max = max(mas_gastos, key=mas_gastos.get)
    valor_max = mas_gastos[fecha_max]

    return {"fecha": fecha_max, "valor": valor_max}


def calcular_resumen_categoria(data):
    resumen = {}
    for item in data:
        resumen[item["categoria"]] = resumen.get(item["categoria"], 0) + item["valor"]

    return resumen


def promedio_diario(data):
    ultimos_siete = gasto_7_dias(data)
    total_siete_dias = 0

    if not ultimos_siete:
        return 0

    for gasto_valor in ultimos_siete:
        total_siete_dias += gasto_valor["valor"]

    return total_siete_dias / 7


def promedio_historico_diario(data):
    dias_con_gasto = []
    gastos_valor = 0

    if not data:
        return 0

    for gasto_fecha in data:
        dias_con_gasto.append(gasto_fecha["fecha"][:10])

    dias_unicos = set(dias_con_gasto)

    for gasto in data:
        gastos_valor += gasto["valor"]

    promedio = gastos_valor / len(dias_unicos)

    return promedio
