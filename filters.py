def obtener_categorias(data):

    if len(data) == 0:
        return []
    else:
        return set(gasto["categoria"] for gasto in data)


def filtrar_por_categoria(data, categoria):
    if len(data) == 0:
        return []
    else:
        return [elemento for elemento in data if elemento["categoria"] == categoria]
