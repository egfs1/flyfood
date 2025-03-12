import random

def sample_hyperparameters():
    num_ants = int(random.lognormvariate(mu=3, sigma=0.5))
    num_ants = max(5, min(num_ants, 50))  # Garante que fique no intervalo correto

    gen = int(random.lognormvariate(mu=4, sigma=0.5))
    gen = max(50, min(gen, 500))  # Garante o limite de gerações

    rho = random.betavariate(alpha=2, beta=5) * 0.8 + 0.1  # Mantém no range [0.1, 0.9]

    alpha = random.expovariate(1.0)  # Corrigido: 1.0 é o equivalente ao `scale=1.0`
    alpha = max(0.5, min(alpha, 3.0))  # Limita alpha para valores razoáveis

    beta = random.normalvariate(mu=3, sigma=1.0)  # Corrigido: Adicionado sigma para controle da dispersão
    beta = max(1.0, min(beta, 5.0))  # Mantém beta dentro do intervalo recomendado

    return {
        "num_ants": num_ants,
        "gen": gen,
        "rho": rho,
        "alpha": alpha,
        "beta": beta
    }

# Teste para verificar a coerência dos valores gerados
for _ in range(5):
    print(sample_hyperparameters())