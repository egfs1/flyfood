import math
import random
import time


class Graph:
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
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
            distance = (1.0 / self.graph.distance_matrix[self.current_city][city]) ** self.beta
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
    def __init__(self, graph, num_ants=10, gen=100, rho=0.5, q=100):
        self.graph = graph
        self.num_ants = num_ants
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

        for gen in range(self.gen):
            ants = [Ant(self.graph) for _ in range(self.num_ants)]
            for ant in ants:
                ant.trace_route()
                if ant.cost < best_cost:
                    best_cost = ant.cost
                    best_route = ant.route
            self._evaporate()
            self._deposit_feromone(ants)
            print(f"Geração {gen + 1}/{self.gen}: Melhor custo = {best_cost}")
        
        return best_route, best_cost
    
def load_tsp(file):
    cities = []
    with open(file, 'r') as f:
        for row in f:
            if row.strip() == "NODE_COORD_SECTION":
                break
        
        for row in f:
            if row.strip() == "EOF":
                break
            parts = row.strip().split()
            if parts[0].isdigit():

                x = float(parts[1])
                y = float(parts[2])
                cities.append((x, y))

    return cities

def euclidean_dist(cities):
    n = len(cities)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = cities[i][0] - cities[j][0]
                dy = cities[i][1] - cities[j][1]
                matrix[i][j] = math.sqrt(dx*dx + dy*dy)
    return matrix

def main():

    random.seed(42)
    
    cities = load_tsp("flyfood/berlin52.tsp")
    distance_matrix = euclidean_dist(cities)
    graph = Graph(distance_matrix)
    antc = AntC(graph, num_ants=52, gen=10000, rho=0.5, q=100)
    best_route, best_cost = antc.solve()

    print(f"Melhor rota: {best_route}")
    print(f"Melhor custo: {best_cost}")

if __name__ == "__main__":
    main()