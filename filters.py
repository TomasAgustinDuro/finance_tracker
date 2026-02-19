from crud import leer_historial

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


