import random
import matplotlib.pyplot as plt
import numpy as np
from funcoes_auxiliares.read_tsp import load_tsp
from funcoes_auxiliares.plotting import plot_best_route, plot_snapshot

def sample_parameters(graph, num_trials=30):
    """
    Busca aleatória para otimizar os hiperparâmetros do Algoritmo de Colônia de Formigas.

    :param graph: Objeto do grafo do problema.
    :param num_trials: Número de tentativas da busca aleatória.
    :return: Melhor conjunto de hiperparâmetros e o menor custo encontrado.
    """
    best_params = None
    best_cost = float('inf')

    for i in range(num_trials):

        num_ants = int(random.lognormvariate(mu=3, sigma=0.5))
        num_ants = max(5, min(num_ants, 50))  

        gen = int(random.lognormvariate(mu=4, sigma=0.5))
        gen = max(50, min(gen, 500))  

        rho = random.betavariate(alpha=2, beta=5) * 0.8 + 0.1  

        alpha = random.expovariate(1.0)  
        alpha = max(0.5, min(alpha, 3.0))  

        beta = random.normalvariate(mu=3, sigma=1.0)  
        beta = max(1.0, min(beta, 5.0)) 

        aco = AntC(graph, num_ants=num_ants, gen=gen, rho=rho, alpha=alpha, beta=beta)
        _, cost = aco.solve()

        if cost < best_cost:
            best_cost = cost
            best_params = {
                "num_ants": num_ants,
                "gen": gen,
                "rho": rho,
                "alpha": alpha,
                "beta": beta
            }

        print(f"Tentativa {i+1}/{num_trials}: Custo = {cost} | Parâmetros: {best_params}")

    print("\nMelhores hiperparâmetros encontrados:", best_params)
    print("Melhor custo obtido:", best_cost)
    
    return best_params, best_cost

class Graph:
    def __init__(self, distance_matrix, cities):
        self.distance_matrix = distance_matrix
        self.cities = cities
        self.n = len(distance_matrix)
        self.feromone = [[1.0 / (self.n * self.n) for _ in range(self.n)] for _ in range(self.n)]

class Ant:
    def __init__(self, graph, alpha=1.0, beta=2.0):
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.route = []
        self.cost = 0.0
        self.current_city = random.randint(0, self.graph.n - 1)
        self.route.append(self.current_city)
        self.unvisited_cities = set(range(self.graph.n)) - {self.current_city}

    def _select_next_city(self):
        probabilities = []
        total = 0.0

        for city in self.unvisited_cities:
            feromone = self.graph.feromone[self.current_city][city] ** self.alpha
            dist = self.graph.distance_matrix[self.current_city][city]
            if dist <= 1e-9: 
                dist = 1e-6   
            distance = (1.0 / dist) ** self.beta
            probability = feromone * distance
            probabilities.append((city, probability))
            total += probability

        if total == 0.0:
            return random.choice(list(self.unvisited_cities))

        rand = random.uniform(0, total)
        prob_ac = 0.0
        for city, prob in probabilities:
            prob_ac += prob
            if prob_ac >= rand:
                return city
            
        return probabilities[0][0]
    
    def trace_route(self):
        while self.unvisited_cities:
            next_city = self._select_next_city()
            self.unvisited_cities.remove(next_city)
            self.cost += self.graph.distance_matrix[self.current_city][next_city]
            self.current_city = next_city
            self.route.append(next_city)
        self.cost += self.graph.distance_matrix[self.route[-1]][self.route[0]]


class AntC:
    def __init__(self, graph, num_ants=10, gen=100, rho=0.5, q=100, alpha=1.0, beta=2.0):
        self.graph = graph
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.gen = gen
        self.rho = rho
        self.q = q
    
    def _evaporate(self):
        for i in range(self.graph.n):
            for j in range(self.graph.n):
                self.graph.feromone[i][j] *= (1.0 - self.rho)
    
    def _deposit_feromone(self, ants):
        for ant in ants:
            deposit = self.q / ant.cost
            for i in range(len(ant.route) - 1):
                current_city = ant.route[i]
                next_city = ant.route[i + 1]
                self.graph.feromone[current_city][next_city] += deposit
                self.graph.feromone[next_city][current_city] += deposit

    def solve(self):
        best_cost = float('inf')
        best_route = []

        snapshot_gens = {1, self.gen}
        if self.gen >= 30:
            snapshot_gens.add(30)
        snapshot_gens.add(self.gen // 2)

        for gen in range(1, self.gen + 1):
            ants = [Ant(self.graph) for _ in range(self.num_ants)]
            for ant in ants:
                ant.trace_route()
                if ant.cost < best_cost:
                    best_cost = ant.cost
                    best_route = ant.route
            self._evaporate()
            self._deposit_feromone(ants)
            print(f"Geração {gen}/{self.gen}: Melhor custo = {best_cost}")
            if gen in snapshot_gens:
                print(f"Salvando snapshots da geração {gen}.")
                plot_snapshot(gen, self.graph, self.num_ants, best_cost)
                plot_best_route(self.graph, best_cost, best_route, gen)
        
        return best_route, best_cost

def main():

    random.seed(42)
    
    cities, distance_matrix = load_tsp("testFiles/berlin52.tsp")

    graph = Graph(distance_matrix, cities)
    antc = AntC(graph, num_ants=10, gen=97, rho=0.30, q=100, alpha=0.72, beta=2.86)
    best_route, best_cost = antc.solve()

    print(f"Melhor rota: {best_route}")
    print(f"Melhor custo: {best_cost}")

def random_search():

    cities, distance_matrix = load_tsp("testFiles/brazil58.tsp")
    graph = Graph(distance_matrix, cities)

    best_params, best_cost = sample_parameters(graph=graph, num_trials=30)
if __name__ == "__main__":
    main()