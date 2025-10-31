import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_simulation(prices: dict, weights: dict , days: int, simulations: int ):
    """Simula la evolución de una cartera o activo usando Monte Carlo.
    
        - prices: dict con {symbol: [close1, close2, ...]}
        - weights: dict con {symbol: peso} (solo si es cartera)
        - days: horizonte temporal en días
        - simulations: número de trayectorias simuladas
    Retorna: dict con {symbol: matriz de simulaciones (simulations x days)}. 
        - Trayectorias simuladas por símbolo
        - Trayectoria de la cartera si se usaron pesos."""
    
    
    results = {}
    for symbol, series in prices.items():
        log_returns = np.log(np.array(series[1:]) / np.array(series[:-1])) # Calcula los retornos logarítmicos diarios
        mu = np.mean(log_returns) #Calcula la media de los retornos logarítmicos
        sigma = np.std(log_returns) #Calcula la desviación estándar de los retornos logarítmicos
     
        # Simulaciones de Monte Carlo
        simulations_matrix = np.zeros((simulations, days)) #Crea una matriz vacia para almacenar las simulaciones
        for i in range(simulations):
            daily_returns = np.random.normal(mu, sigma, days) #Genera retornos diarios aleatorios con distribución normal
            price_path = [series[-1]]
            for r in daily_returns:
                price_path.append(price_path[-1] * np.exp(r)) #Simula la evolución del precio partiendo del último precio conocido
            simulations_matrix[i] = price_path[1:] #Almacena la simulación en la matriz

        results[symbol] = simulations_matrix

    # Si hay pesos, calcular evolución de la cartera
    if weights:
        portfolio_simulations = np.zeros((simulations, days)) #Matriz para almacenar las simulaciones de la cartera
        for symbol, sim_matrix in results.items():
            portfolio_simulations += sim_matrix * weights[symbol] #Suma ponderada de las simulaciones individuales de cada valor de la cartera
        results["Cartera"] = portfolio_simulations
    
    return results

def plot_simulation(sim_dict: dict, symbols: list):
    """ Grafica múltiples activos simulados en una sola figura.
        - sim_dict: dict con {symbol: np.array(simulaciones)}
        - symbols: lista de símbolos a graficar"""
    
    plt.figure(figsize=(12, 6))
    
    for symbol in symbols:
        sim_matrix = sim_dict.get(symbol)
        if sim_matrix is None:
            print(f"No hay simulaciones para {symbol}")
            continue
        # Promedio de las trayectorias simuladas
        mean_path = sim_matrix.mean(axis=0)
        plt.plot(mean_path, label=symbol)

    plt.title("Simulación Monte Carlo")
    plt.xlabel("Días")
    plt.ylabel("Precio promedio simulado")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
