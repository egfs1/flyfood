def distancia(p1: tuple, p2: tuple) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def custo_do_percurso(ponto_inicial, index_atual, percurso, pontos_de_entrega):
    ponto_atual = ponto_inicial if index_atual == -1 else pontos_de_entrega[percurso[index_atual]]
    
    if index_atual == len(percurso) - 1:
        return distancia(ponto_atual, ponto_inicial)
    
    return distancia(ponto_atual, pontos_de_entrega[percurso[index_atual + 1]]) + custo_do_percurso(ponto_inicial, index_atual + 1, percurso, pontos_de_entrega)
    
def permutacao_dos_pontos(pontos):
    def backtrack(inicio, fim):
        if inicio == fim:
            permutacoes.append(pontos[:])
        else:
            for i in range(inicio, fim):
                pontos[inicio], pontos[i] = pontos[i], pontos[inicio]
                backtrack(inicio + 1, fim)
                pontos[inicio], pontos[i] = pontos[i], pontos[inicio]

    permutacoes = []
    backtrack(0, len(pontos))
    return permutacoes


def melhor_percurso(ponto_inicial, pontos_de_entrega):
    custo_menor_percurso = None
    menor_percurso = None
    todos_os_percursos = permutacao_dos_pontos(list(pontos_de_entrega.keys()))
    for percurso in todos_os_percursos:
        custo = custo_do_percurso(ponto_inicial, -1, percurso, pontos_de_entrega)
        if custo_menor_percurso is None or custo < custo_menor_percurso:
            custo_menor_percurso = custo
            menor_percurso = percurso

    return (custo_menor_percurso, menor_percurso)


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
