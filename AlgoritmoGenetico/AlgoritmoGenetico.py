
from re import M
from types import MethodType
import random
import matplotlib.pyplot as plt
import numpy as np

matriz = [
   (25.0, 185.0), (345.0, 750.0), (945.0, 685.0), (845.0, 655.0),
    (880.0, 660.0), (25.0, 230.0), (525.0, 1000.0), (580.0, 1175.0), (650.0, 1130.0),
    (1605.0, 620.0), (1220.0, 580.0), (1465.0, 200.0), (1530.0, 5.0), (845.0, 680.0),
    (725.0, 370.0), (145.0, 665.0), (415.0, 635.0), (510.0, 875.0), (560.0, 365.0),
    (300.0, 465.0), (520.0, 585.0), (480.0, 415.0), (835.0, 625.0), (975.0, 580.0),
    (1215.0, 245.0), (1320.0, 315.0), (1250.0, 400.0), (660.0, 180.0), (410.0, 250.0),
    (420.0, 555.0), (575.0, 665.0), (1150.0, 1160.0), (700.0, 580.0), (685.0, 595.0),
    (685.0, 610.0), (770.0, 610.0), (795.0, 645.0), (720.0, 635.0), (760.0, 650.0),
    (475.0, 960.0), (95.0, 260.0), (875.0, 920.0), (700.0, 500.0), (555.0, 815.0),
    (830.0, 485.0), (1170.0, 65.0), (830.0, 610.0), (605.0, 625.0), (595.0, 360.0),
    (1340.0, 725.0), (1740.0, 245.0)
]


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

def Fitness(array_dots,init_dot):
    Aptidao = []
    for array_dot in array_dots:
      distance = abs(init_dot[0]-array_dot[0][0]) + abs(init_dot[1]-array_dot[0][1])

      for i in range(len(array_dot)-1):
          distance += abs(array_dot[i][0]-array_dot[i+1][0]) + abs(array_dot[i][1]-array_dot[i+1][1])

      distance += abs(init_dot[0]-array_dot[-1][0]) + abs(init_dot[1]-array_dot[-1][1]) # Use -1 to access the last element of array_dot

      Aptidao.append((array_dot,distance))

    Aptidao.sort(key=lambda x: x[1])
    return Aptidao

def CrossOver(parent1, parent2,cross_over_rate):
   if random.random() * 100 < cross_over_rate:
      size = len(parent1)
      child1, child2 = [-1] * size, [-1] * size

      ponto1, ponto2 = sorted(random.sample(range(size), 2))
      child1[ponto1:ponto2] = parent1[ponto1:ponto2]
      child2[ponto1:ponto2] = parent2[ponto1:ponto2]

      def preencher(child, parent):
          usados = set(child[ponto1:ponto2])
          for i in range(size):
              if child[i] == -1:
                  for gene in parent:
                      if gene not in usados:
                          child[i] = gene
                          usados.add(gene)
                          break
          return child

      return preencher(child1, parent2), preencher(child2, parent1)

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
  
def Roleta(fitness_list):
    # Calcula o total das aptidões (inverso da distância para minimizar)
    total_fitness = sum(1 / individuo[1] for individuo in fitness_list)

    # Gera um número aleatório entre 0 e o total de fitness
    pick = random.uniform(0, total_fitness)

    current = 0
    for individuo in fitness_list:
        current += 1 / individuo[1]  # Quanto menor a distância, maior a chance de ser escolhido
        if current >= pick:
            return individuo[0]  # Retorna o caminho do indivíduo selecionado
        


def Filhos(parent_list_initial,cross_over_rate,cross_over_method,mutation_rate,mutation_method,initial_point):
  new_population = []
  parent_fitness = Fitness(parent_list_initial,initial_point)
  while len(new_population) < len(parent_list_initial):
    parent1, parent2 = None, None
    while parent1 == parent2:
      parent1 = Roleta(parent_fitness)
      parent2 = Roleta(parent_fitness)
    child1, child2 = cross_over_method(parent1, parent2, cross_over_rate)
    child1 = mutation_method(child1, mutation_rate)
    child2 = mutation_method(child2, mutation_rate)
    new_population.append(child1)
    if len(new_population) < len(parent_list_initial):
            new_population.append(child2)
  return new_population

def Elitismo(children_apts,parent_apts):
  final_population = []
  taixa = len(parent_apts)*(30/100)
  taixa2= len(parent_apts)*(70/100)
  for i in range(int(taixa)):
    final_population.append(parent_apts[i][0])
  for i in range(int(taixa2)):
    final_population.append(children_apts[i][0])
  return final_population


def Main(generations,population_size,cross_over_rate,cross_over_method,mutation_rate,mutation_method,make_random_permute_method,selection_method,fitness_method,initial_point):
  population_initial = MakePopulation(population_size,make_random_permute_method,matriz)
  parents_apts = Fitness(population_initial,initial_point)
  for i in range(generations):
    children = Filhos(population_initial,cross_over_rate,cross_over_method,mutation_rate,mutation_method,initial_point)
    children_apts = Fitness(children,initial_point)
    population_initial = selection_method(children_apts,parents_apts)
    parents_apts = Fitness(population_initial,initial_point)
  return fitness_method(population_initial,initial_point)


#instancia dos metodos
fitness_method = Fitness
makerandompermute = MakeRandomPermute
cross_over_method = CrossOver
mutation_method = MutacaoSwap
selection_method = Elitismo
make_random_permute_method = MakeRandomPermute
#variaveis
generations = 200
population_size = 400
cross_over_rate = 95
mutation_rate = 2
initial_point = (565.0, 575.0)

arr = Main(generations,population_size,cross_over_rate,cross_over_method,mutation_rate,mutation_method,make_random_permute_method,selection_method,fitness_method,initial_point)
print(arr[0])