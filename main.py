R = (3,0)
A = (1,1)
B = (3,2)
C = (2,4)
D = (0, 4)
P = [B, D, A, C]

def distancia(ponto1: tuple, ponto2: tuple):
    return abs(ponto1[0] - ponto2[0]) + abs(ponto1[1] - ponto2[1])

def custo_do_percurso(ponto_atual, proximo_ponto, pontos_faltantes):
    if len(pontos_faltantes) == 0:
        return distancia(ponto_atual, proximo_ponto) + distancia(proximo_ponto, R)
    
    novo_proximo_ponto = pontos_faltantes[0]
    novo_pontos_faltantes = pontos_faltantes[1:]
    return distancia(ponto_atual, proximo_ponto) + custo_do_percurso(proximo_ponto, novo_proximo_ponto, novo_pontos_faltantes)

def permutacao_dos_pontos(pontos):
    if len(pontos) == 1:
        return [pontos]
    permutacoes = []
    for i in range(len(pontos)):
        ponto = pontos[i]
        pontos_restantes = pontos[:i] + pontos[i+1:]
        for permutacao in permutacao_dos_pontos(pontos_restantes):
            permutacoes.append([ponto] + permutacao)
    return permutacoes

def melhor_percurso(ponto_inicial, lista_de_pontos):
    custo_menor_percurso = None
    menor_percurso = None
    for percurso in permutacao_dos_pontos(lista_de_pontos):
        custo = custo_do_percurso(ponto_inicial, percurso[0], percurso[1:])
        if custo_menor_percurso is None or custo < custo_menor_percurso:
            custo_menor_percurso = custo
            menor_percurso = percurso

    return (custo_menor_percurso, menor_percurso)


print(melhor_percurso(R, P)) 



