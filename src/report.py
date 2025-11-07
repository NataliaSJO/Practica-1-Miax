import os
from datetime import date
from data_classes import DailyPrice

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
        lines.append("|---------|----------|--------------------|-------------------|")

        # crear una instancia de DailyPrice para usar los métodos de instancia
        dp = DailyPrice(date.today(), 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        # Preparar los pesos que se mostrarán en la tabla. Usar self.weights si está disponible,
        # en caso contrario calcular un fallback por símbolo.
        weights_used = {}
        for symbol in symbols:
            weight = dp.calculate_risk_parity_weights([symbol], data)[symbol]
            weights_used[symbol] = float(weight)

        total_weights = sum(weights_used.values()) if len(weights_used) > 0 else 0.0
       
        for symbol in symbols:
            average = dp.average([symbol], data)[symbol]
            std_dev = dp.standard_deviation([symbol], data)[symbol]
            weight = weights_used.get(symbol, 0.0)
            pct = (weight / total_weights) * 100 if total_weights != 0 else 0.0

            lines.append("| {:<7} | {:>8} | {:>18} | {:>25} |".format(symbol, f"{average:.2f}", f"{std_dev:.2f}", f"{pct:.2f}%"))


        lines.append("## Graficas de la cartera\n")   
        lines.append("\n")
        lines.append("En la siguiente gráfica se muestra la media de los valores.\n")  
        lines.append("![Media](plot_average.png)")
        

        lines.append("\n\n")
        lines.append("En la siguiente gráfica se muestra la desviación típica de los valores introducidos.\n")  
        lines.append("![Desviación típica](plot_standard_deviations.png)")
       

        lines.append("\n\n")
        lines.append("En la siguiente gráfica se muestran los pesos de los valores introducidos.\n")  
        lines.append("![Pesos de la símbolos](plot_weights.png)")
      
    

        # Insertar imagen en el Markdown (la simulación se ejecuta en main y se pasa un resumen opcional)
        lines.append("\n## Simulación Monte Carlo de la Cartera")
        lines.append("\n La simulación se ha calcula con los siguientes parámetros: ")

        # `sim_logs` puede ser pasado por el llamador (main). Si no existe, dejamos un texto genérico.
        # El llamador puede pasar la lista de logs o un string ya formateado.
        first_line = ""
        # report espera que el llamador establezca self._sim_logs temporalmente si quiere que aparezca
        sim_logs = getattr(self, "_sim_logs", None)
        if sim_logs:
            if isinstance(sim_logs, list):
                formatted = self.logs_monte_carlo_sim(sim_logs)
                first_line = formatted.splitlines()[0] if formatted else ""
            elif isinstance(sim_logs, str):
                first_line = sim_logs.splitlines()[0] if sim_logs else ""

        if first_line:
            lines.append(first_line)
        else:
            lines.append("- No hay resumen de la simulación disponible. Ejecuta la simulación desde 'main' para incluirlo.")

        lines.append("- Se ha realizado una simulación a lo largo de 365 días.\n")
        lines.append("A continuación, se muestra la simulación Monte Carlo de la cartera basada en los precios ajustados y los pesos calculados.\n")

        lines.append("![Simulación Monte Carlo](simulation.png)")

        return "\n".join(lines)

    def export_and_open_report(report:str, filename: str = "portfolio_report.md"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        os.startfile(filename)
