import numpy as np
from sklearn.manifold import MDS

def load_upper_row_tsp(file_path):
    """Carrega um arquivo .tsp no formato UPPER_ROW e retorna a matriz de distâncias."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    reading_weights = False
    dist_values = []
    n = 0

    for line in lines:
        line = line.strip()
        if line.startswith("DIMENSION"):
            n = int(line.split(":")[1].strip())  # Obtém o número de cidades
        elif line.startswith("EDGE_WEIGHT_SECTION"):
            reading_weights = True
            continue
        elif line.startswith("EOF"):
            break
        elif reading_weights:
            dist_values.extend(map(int, line.split()))

    # Construir matriz de distâncias (simétrica)
    dist_matrix = np.zeros((n, n))
    idx = 0
    for i in range(n):
        for j in range(i + 1, n):
            dist_matrix[i, j] = dist_values[idx]
            dist_matrix[j, i] = dist_values[idx]
            idx += 1

    return dist_matrix

def generate_coordinates(dist_matrix, seed=42):
    """Gera coordenadas 2D aproximadas usando MDS a partir da matriz de distâncias."""
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=seed)
    coords = mds.fit_transform(dist_matrix)

    # Pequena variação para evitar pontos idênticos (se necessário)
    noise = np.random.normal(scale=0.01, size=coords.shape)
    coords += noise

    return coords

def save_tsp_node_coord(file_path, coords):
    """Salva as coordenadas geradas no formato NODE_COORD_SECTION em um novo arquivo .tsp"""
    n = len(coords)
    output_file = file_path.replace(".tsp", "_node_coord.tsp")

    with open(output_file, "w") as f:
        f.write(f"NAME : {output_file}\n")
        f.write("TYPE : TSP\n")
        f.write(f"DIMENSION : {n}\n")
        f.write("EDGE_WEIGHT_TYPE : EUC_2D\n")
        f.write("NODE_COORD_SECTION\n")

        for i, (x, y) in enumerate(coords, start=1):
            f.write(f"{i} {x:.6f} {y:.6f}\n")

        f.write("EOF\n")

    print(f"Arquivo salvo como {output_file}")

# Caminho do arquivo original
file_path = "flyfood/brazil58.tsp"

# Executa a conversão
dist_matrix = load_upper_row_tsp(file_path)
coordinates = generate_coordinates(dist_matrix)
save_tsp_node_coord(file_path, coordinates)
