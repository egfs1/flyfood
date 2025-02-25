import math

def _euclidean_dist(cities):
    n = len(cities)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = cities[i][0] - cities[j][0]
                dy = cities[i][1] - cities[j][1]
                matrix[i][j] = math.sqrt(dx*dx + dy*dy)
    return matrix

def load_tsp(file):
    """
    Lê um arquivo TSPLIB e retorna uma tupla (cities, distance_matrix).

    - Se o arquivo contiver NODE_COORD_SECTION, lê as coordenadas (x,y)
      e calcula a matriz de distâncias euclidianas (EUC_2D).
    - Se o arquivo for EXPLICIT (EDGE_WEIGHT_TYPE: EXPLICIT), lê a matriz de distâncias
      do arquivo e gera um layout circular para as cidades (apenas para visualização).
    """
    with open(file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    dimension = None
    edge_weight_type = None

    # Lê metadados
    for line in lines:
        if line.startswith("DIMENSION"):
            dimension = int(line.split(":")[1].strip())
        elif line.startswith("EDGE_WEIGHT_TYPE"):
            edge_weight_type = line.split(":")[1].strip().upper()

    # Caso 1: Verificar se há NODE_COORD_SECTION
    if any("NODE_COORD_SECTION" in line for line in lines):
        # Lê as coordenadas
        cities = []
        start_idx = lines.index("NODE_COORD_SECTION") + 1
        for line in lines[start_idx:]:
            if line.upper().startswith("EOF"):
                break
            parts = line.split()
            if len(parts) >= 3 and parts[0].isdigit():
                x = float(parts[1])
                y = float(parts[2])
                cities.append((x, y))
        # Calcula a matriz de distâncias
        distance_matrix = _euclidean_dist(cities)
        return cities, distance_matrix

    # Caso 2: Se for EXPLICIT (por exemplo, brazil58)
    if edge_weight_type == "EXPLICIT":
        if dimension is None:
            raise ValueError("DIMENSION não especificada no arquivo.")
        
        # Localiza EDGE_WEIGHT_SECTION
        try:
            start_idx = next(i for i, line in enumerate(lines) if "EDGE_WEIGHT_SECTION" in line) + 1
        except StopIteration:
            raise ValueError("Não foi encontrada a seção EDGE_WEIGHT_SECTION.")

        weight_lines = []
        for line in lines[start_idx:]:
            if line.upper().startswith("EOF"):
                break
            weight_lines.append(line)
        numbers = []
        for line in weight_lines:
            numbers.extend(line.split())
        numbers = [float(num) for num in numbers]

        # Reconstrói a matriz (assumindo UPPER_ROW)
        expected = dimension * (dimension - 1) // 2
        if len(numbers) < expected:
            raise ValueError(f"Número de pesos insuficiente. Esperava {expected} e obteve {len(numbers)}.")

        matrix = [[0.0 for _ in range(dimension)] for _ in range(dimension)]
        index = 0
        for i in range(dimension):
            for j in range(i + 1, dimension):
                matrix[i][j] = numbers[index]
                matrix[j][i] = numbers[index]
                index += 1
        
        # Gera layout circular para visualização
        cities = []
        radius = 100.0
        for i in range(dimension):
            theta = 2 * math.pi * i / dimension
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            cities.append((x, y))
        
        return cities, matrix

    # Caso 3: Outros formatos não implementados
    raise ValueError("Formato de arquivo não reconhecido ou não suportado.")