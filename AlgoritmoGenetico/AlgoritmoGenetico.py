from re import M
from types import MethodType
import random
import matplotlib.pyplot as plt
import numpy as np


matriz = [["L" , 0 , 0 , 0 , 0],
          [0, "H", "G" , "F", "E"],
          [0, 0, 0 , 0 , "D"],
          [0 , 0 , 0 , 0 , "C"],
          [0 , "A" , 0 , 0 , "B"]]



def PontosCouter(array):
  ArrayValues = []
  Dots = []
  for i in range(len(array)):
    for j in range(len(array[i])):
            if array[i][j] != 0:
                name = array[i][j]
                Dots.append(name)
                coordenadas = (i, j)
                ArrayValues.append(coordenadas)
  return ArrayValues

def MakeRandomPermute(arr):
    # Cria uma cópia do array para não modificar o original
    new_permute = arr.copy()
    # Embaralha a cópia
    random.shuffle(new_permute)
    return new_permute



def MakePopulation(population_size,random_permute_method,dot_list):
  population = []
  for i in range(population_size):
    dots_copy = dot_list.copy()
    population.append(random_permute_method(dots_copy))

  return population


def Fitness(array_base,array_dots):
  linhas = len(array_base)
  colunas = len(array_base[0])
  solucao = []
  A=(linhas - 1, 0)#Começo
  B=(0, colunas - 1)#Fim
  Aptidao = []
  menor = 9999999999999999999999
  for caminho in array_dots:
    x = abs(caminho[0][0] - A[0]) + abs(caminho[0][1] - A[1])
    y = 0
    for j in range(len(caminho)-1):
       y += abs(caminho[j+1][0] - caminho[j][0]) + abs(caminho[j+1][1] - caminho[j][1])

    z = y + x + abs(caminho[-1][0] - B[0]) + abs(caminho[-1][1] - B[1])

    Aptidao.append((caminho,z))

  Aptidao.sort(key=lambda x: x[1])

  return Aptidao


def CrossOver(parent1, parent2, cross_over_rate):
    if random.random() * 100 < cross_over_rate:
        size = len(parent1)
        ponto1, ponto2 = sorted(random.sample(range(size), 2))

        filho1 = [-1] * size
        filho2 = [-1] * size

        filho1[ponto1:ponto2] = parent1[ponto1:ponto2]
        filho2[ponto1:ponto2] = parent2[ponto1:ponto2]

        def preencher_filho(filho, parent):
            usados = set(filho[ponto1:ponto2])  # Coleta os valores já presentes
            for i in range(size):
                if i < ponto1 or i >= ponto2:
                    for gene in parent:
                        if gene not in usados:
                            filho[i] = gene
                            usados.add(gene)
                            break
            return filho

        filho1 = preencher_filho(filho1, parent2)
        filho2 = preencher_filho(filho2, parent1)

        return filho1, filho2

    return parent1, parent2



def MutacaoSwap(rota, taxa_mutacao):
    if random.random() * 100 < taxa_mutacao:
        # Escolhe dois índices aleatórios para trocar
        rota = list(rota)

        idx1, idx2 = random.sample(range(len(rota)), 2)

        # Troca as tuplas nos índices escolhidos
        rota[idx1], rota[idx2] = rota[idx2], rota[idx1]

    return rota



def Torneio(fitness_list):
  firstidx = random.randint(0,len(fitness_list)-1)
  secondidx = random.randint(0,len(fitness_list)-1)
  if fitness_list[firstidx][1] < fitness_list[secondidx][1]:
    return fitness_list[firstidx][0]
  else:
    return fitness_list[secondidx][0]

def Filhos(parent_list_initial,cross_over_rate,cross_over_method,taxa_mutacao,mutation_method):
  new_population = []
  while len(new_population) < len(parent_list_initial):
    parent1 = Torneio(Fitness(matriz,parent_list_initial))
    parent2 = Torneio(Fitness(matriz,parent_list_initial))
    child1, child2 = cross_over_method(parent1, parent2,cross_over_rate)
    child1 = mutation_method(child1,taxa_mutacao)
    child2 = mutation_method(child2,taxa_mutacao)
    new_population.append(child1)
    new_population.append(child2)
  return new_population


def Elitismo(filhos_aptos,pais_aptos):
  final_population = []
  taixa = len(pais_aptos)*(10/100)
  taixa2= len(pais_aptos)*(90/100)
  for i in range(int(taixa)):
    final_population.append(pais_aptos[i][0])
  for i in range(int(taixa2)):
    final_population.append(filhos_aptos[i][0])
  return final_population


#----------Make generations---------

#Fazendo uma geração

pais = MakePopulation(Tamanho_Populacao,makePermute,dotList)
pais_mais_aptos = Fitness(matriz_base,pais)

filhos = Filhos(pais,cross_over_rate,cross_over_method,mutation_rate,mutation_method)
filhos_mais_aptos = Fitness(matriz_base,filhos)



def Main(generations,population_size,cross_over_rate,mutation_rate,cross_over_method,mutation_method,fitness_method,selection_method,make_population_method,make_permutations_method,make_childs_method,dot_list,matriz_base):
  population_initial = make_population_method(population_size,make_permutations_method,dot_list)
  for i in range(generations):
    pais_aptos = fitness_method(matriz_base,population_initial)
    filhos = make_childs_method(population_initial,cross_over_rate,cross_over_method,mutation_rate,mutation_method)
    flhos_aptos = fitness_method(matriz_base,filhos)
    population_initial = selection_method(flhos_aptos,pais_aptos)
  return fitness_method(matriz_base,population_initial)



#instancia dos metodos por causa do desaclopamento
makePermute = MakeRandomPermute
makePopulation = MakePopulation
cross_over_method = CrossOver
make_childs_method = Filhos
fitness_method = Fitness
mutation_method = MutacaoSwap
selection_method = Elitismo
#variaveis
matriz_base = matriz
dotList = PontosCouter(matriz)
population_size = 50 
cross_over_rate = 90
mutation_rate = 10
generations = 400


Main(generations,population_size,cross_over_rate,mutation_rate,cross_over_method,mutation_method,fitness_method,selection_method,makePopulation,makePermute,make_childs_method,dotList,matriz_base)





