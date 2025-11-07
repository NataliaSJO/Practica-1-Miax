from datetime import date
import os
from dotenv import load_dotenv

import argparse

import extractor
from monte_carlo_simulation import monte_carlo_simulation, plot_simulation
from report import Portfolio
from src.data_classes import DailyPrice
from utils.utils_grafic import UtilsGrafic

def main():
    load_dotenv() # Carga las variables de entorno desde el archivo .env

    parser = argparse.ArgumentParser(description="Consulta los datos historicos de una accion o un indece desde la terminal")
    parser.add_argument("--source", nargs='+', type=str, default=["yaho_finance"], help="Fuente de datos disponibles (ej: yahoo_finance, tiingo)")
    parser.add_argument("--symbol", nargs='+', type=str, default=["^IBEX"], help="Símbolo del activo (ej. AAPL, SAN.MC)")
    parser.add_argument("--interval", type=str, default="1d", help="Intervalo de datos (ej. 1d, 1wk)")
    parser.add_argument("--range", type=str, default="5y", help="Rango de tiempo (ej. 5d, 1m, 1y)")
    parser.add_argument("--format", type=str, default="json", help="Hay dos formatos disponibles (ej: json, csv)")
    args = parser.parse_args()
   
    api_key_tiingo = os.getenv("TIINGO_KEY")
 
    my_extractor = extractor.Extractor(tiingo_key = api_key_tiingo)
    my_extractor.get_multiple_outputs(args.symbol, args.source, args.format, args.range)    
    results = my_extractor.get_multiple_outputs(args.symbol, args.source, args.format, args.range)
    
    dp = DailyPrice(date.today(), 0.0, 0.0, 0.0, 0.0, 0.0, 0)

   #Usar la instancia `dp` para llamar a los métodos de instancia (antes eran estáticos)
    average = dp.average(args.symbol, results)
    UtilsGrafic.plot_averages(average)

    standars_deviation = dp.standard_deviation(args.symbol, results)
    UtilsGrafic.plot_standard_deviations(standars_deviation)

    weights = dp.calculate_risk_parity_weights(args.symbol, results)
    UtilsGrafic.plot_weights(weights)

    adjusted_prices = dp.extract_adj_close_prices(results)
    
    results_portfolio = [results[source][symbol] for source in results for symbol in results[source]]
    portfolio = Portfolio(results_portfolio, adjusted_prices, weights)
   
    sim_cartera = monte_carlo_simulation(adjusted_prices, weights, days=365, simulations=200)
    logs = sim_cartera[1]
    plot_simulation(sim_cartera[0], args.symbol + ["Cartera"])
    portfolio._sim_logs = logs


    report_md = portfolio.report(args.symbol, results, include_warnings=True, markdown=True)
    Portfolio.export_and_open_report(report_md, filename="portfolio_report.md")
    
if __name__ == "__main__":
    main()
   

