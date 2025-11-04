import os
import pandas as pd
import matplotlib.pyplot as plt
from data_classes import DailyPrice
from monte_carlo_simulation import monte_carlo_simulation, plot_simulation



class Portfolio:
    def __init__(self, data, adjusted_prices: dict, weights: dict):
        self.data = data
        self.adjusted_prices = adjusted_prices
        self.weights = weights
    
    def logs_monte_carlo_sim(self, logs: list) -> str:
        """Genera un string en formato Markdown con los logs de la simulación Monte Carlo.
        Como argumento:
            - logs: lista de strings con los logs de la simulación
        Devuelve: string en formato Markdown."""
                
        markdown = ""
        for log in logs:
            markdown += f"- {log}\n"
        return markdown
    

    def report(self, symbols, data, include_warnings: bool = True, markdown: bool = True) -> str:
        lines = []
        
        # Title and description
        lines.append("# Resumen de la cartera\n")
        lines.append("**Este es el resultado de los valores que has introducido por teclado para generar una cartera**\n")
        lines.append("En la siguiente tabla se pueden ver los resultados de calcular la media, la deviación típica y el calculo de pesos de los valores introducidos por teclado:\n")
      
        # Header for the table
        lines.append("| Símbolo | Media    | Desviación típica  | Pesos riesgo-paridad |")
        lines.append("|---------|----------|--------------------|----------------------|")

        for symbol in symbols:   
            average = DailyPrice.average([symbol], data)[symbol]
            std_dev = DailyPrice.standard_deviation([symbol], data)[symbol]
            weight = self.weights.get(symbol, 0.0)
            
            lines.append("| {:<7} | {:>8} | {:>18} | {:>20} |".format(symbol, f"{average:.2f}", f"{std_dev:.2f}", f"{weight:.2f}"))

        lines.append("## Graficas de la cartera\n")   
        lines.append("\n")
        lines.append("En la siguiente grafica se muestra la media de los valores.\n")  
        lines.append("![Media](average.png)")

        lines.append("\n\n")
        lines.append("En la siguiente grafica se muestra la desviación típica de los valores introducidos.\n")  
        lines.append("![Desviación típica](standard_deviations.png)")

  
        sim_cartera = monte_carlo_simulation(self.adjusted_prices, self.weights, days=365, simulations=200)
        logs = sim_cartera[1]
        log = self.logs_monte_carlo_sim(logs)
        plot_simulation(sim_cartera[0], symbols + ["Cartera"])  

        # Insertar imagen en el Markdown
        lines.append("\n## Simulación Monte Carlo de la Cartera")
        lines.append("\n")        
        lines.append(log)
        lines.append("Se ha realizado una simulación a lo largo de 365 días.\n")
        lines.append("A continuación se muestra la simulación Monte Carlo de la cartera basada en los precios ajustados y los pesos calculados.\n")
     
        lines.append("![Simulación Monte Carlo](simulation.png)")

        return "\n".join(lines)

    def export_and_open_report(report:str, filename: str = "portfolio_report.md"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        os.startfile(filename)
