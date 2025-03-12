import matplotlib.pyplot as plt

def plot_snapshot(generation, graph, num_ants, best_cost):
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    for i in range(graph.n):
        for j in range(i + 1, graph.n):
            intensity = graph.feromone[i][j]
            if intensity > 0.01:
                ax.plot([graph.cities[i][0], graph.cities[j][0]],
                        [graph.cities[i][1], graph.cities[j][1]],
                        'b-', linewidth=intensity * 3, alpha=0.6)
    
    for i, (x, y) in enumerate(graph.cities):
        ax.scatter(x, y, c='red', s=20)
        ax.text(x, y, str(i), fontsize=10, ha='right')
    
    ax.set_title(f"Geração {generation}: Intensidade do Feromônio")

    ax.text(0.5, 1.06,
            f"Formigas: {num_ants} | Melhor Custo: {best_cost:.2f}",
            transform=ax.transAxes,
            ha='center', va='bottom',
            fontsize=11)

    plt.savefig(f"snapshot_generation_{generation}.png")
    plt.close(fig)

def plot_best_route(graph, best_cost, best_route, generation):
    
    fig, ax = plt.subplots(figsize=(8, 8))

    for i in range(len(best_route) - 1):
        city_a, city_b = best_route[i], best_route[i + 1]
        ax.plot([graph.cities[city_a][0], graph.cities[city_b][0]],
                [graph.cities[city_a][1], graph.cities[city_b][1]],
                'r-', linewidth=2.5, alpha=0.9)

    city_a, city_b = best_route[-1], best_route[0]
    ax.plot([graph.cities[city_a][0], graph.cities[city_b][0]],
            [graph.cities[city_a][1], graph.cities[city_b][1]],
            'r-', linewidth=2.5, alpha=0.9)

    for i, (x, y) in enumerate(graph.cities):
        ax.scatter(x, y, c='red', s=30)
        ax.text(x, y, str(i), fontsize=10, ha='right')

    ax.set_title(f"Melhor Rota Encontrada - Geração {generation}")

    ax.text(0.5, 1.06,
            f"Melhor Custo: {best_cost:.2f}",
            transform=ax.transAxes,
            ha='center', va='bottom',
            fontsize=11)

    plt.savefig(f"best_route_generation_{generation}.png")
    plt.close(fig)
