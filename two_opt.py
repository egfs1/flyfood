def distancia(p1: tuple, p2: tuple) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def gerar_tour(ponto_inicial, pontos_de_entrega):
    pontos_restantes = list(pontos_de_entrega.keys())
    tour = []
    ponto_atual = ponto_inicial

    while pontos_restantes:
        proximo_ponto = min(pontos_restantes, key=lambda p: distancia(ponto_atual, pontos_de_entrega[p]))
        tour.append(proximo_ponto)
        ponto_atual = pontos_de_entrega[proximo_ponto]
        pontos_restantes.remove(proximo_ponto)

    return tour


def calcular_custo_total(ponto_inicial, tour, pontos_de_entrega): 
    if not tour:
        return 0

    custo = distancia(ponto_inicial, pontos_de_entrega[tour[0]])
    for i in range(len(tour) - 1):
        custo += distancia(pontos_de_entrega[tour[i]], pontos_de_entrega[tour[i + 1]])
    custo += distancia(pontos_de_entrega[tour[-1]], ponto_inicial)
    
    return custo


def two_opt(ponto_inicial, pontos_de_entrega, tour_inicial):
    tour = tour_inicial.copy()
    melhor_custo = calcular_custo_total(ponto_inicial, tour, pontos_de_entrega)
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(len(tour)):
            for j in range(i + 1, len(tour)):
                a = tour[i - 1] if i > 0 else None
                b = tour[i]
                c = tour[j]
                d = tour[j + 1] if j + 1 < len(tour) else None
                custo_original = 0
                if a is not None:
                    custo_original += distancia(pontos_de_entrega[a], pontos_de_entrega[b])
                else:
                    custo_original += distancia(ponto_inicial, pontos_de_entrega[b])
                if d is not None:
                    custo_original += distancia(pontos_de_entrega[c], pontos_de_entrega[d])
                else:
                    custo_original += distancia(pontos_de_entrega[c], ponto_inicial)
                custo_novo = 0
                if a is not None:
                    custo_novo += distancia(pontos_de_entrega[a], pontos_de_entrega[c])
                else:
                    custo_novo += distancia(ponto_inicial, pontos_de_entrega[c])
                if d is not None:
                    custo_novo += distancia(pontos_de_entrega[b], pontos_de_entrega[d])
                else:
                    custo_novo += distancia(pontos_de_entrega[b], ponto_inicial)
                if custo_novo < custo_original:
                    tour[i:j+1] = tour[i:j+1][::-1]  # Inverte o segmento
                    melhor_custo += (custo_novo - custo_original)
                    melhorou = True
                    break  
            if melhorou:
                break

    return tour, melhor_custo


def melhor_percurso(ponto_inicial, pontos_de_entrega):
    tour_inicial = gerar_tour(ponto_inicial, pontos_de_entrega)     
    tour_otimizado, custo = two_opt(ponto_inicial, pontos_de_entrega, tour_inicial)    
    return (custo, tour_otimizado)


if __name__ == '__main__':
    ponto_de_partida = None
    pontos_de_entrega = {}
    linhas, colunas = map(int, input().split())

    for i in range(linhas):
        valores = input().split()
        for j in range(colunas):
            valor_atual = valores[j]
            if valor_atual == 'R':
                ponto_de_partida = (i, j)
            elif valor_atual != '0':
                pontos_de_entrega[valor_atual] = (i, j)

    custo, percurso = melhor_percurso(ponto_de_partida, pontos_de_entrega)
    print(f"Minimo custo total entre os percursos: {custo}")
    print(f"Menor percurso: " + ' '.join(percurso))
