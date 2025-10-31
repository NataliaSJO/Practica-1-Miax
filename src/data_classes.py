import numpy as np
import matplotlib.pyplot as plt
import statistics
from dataclasses import dataclass,asdict
from datetime import date

from typing import Iterable, List, Optional

@dataclass
class DailyPrice:
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

    def extract_adj_close_prices(symbols: list, data: dict) -> dict:
        """Extrae los precios de cierre ajustado desde un dict anidado por fuente y símbolo.
        Espera formato: {fuente: {symbol: [[DailyPrice, DailyPrice, ...]]}}
        Retorna: {fuente: {symbol: [adj_close, ...]}}"""
        price_adj_close = {}
        for source, symbol_dict in data.items():
            price_adj_close[source] = {}
            for symbol in symbol_dict:
                list_with_symbol = symbol_dict.get(symbol, [])
                if list_with_symbol:
                    daily_prices = list_with_symbol[0]  # acceder a la lista en funcion del symbol
                    price_adj_close[source][symbol] = [dp.adj_close for dp in daily_prices]
                else:
                    price_adj_close[source][symbol] = []   
        first_source = next(iter(price_adj_close)) # Se coje la primera fuente disponible para hacer los calculos
        symbol_dict = price_adj_close[first_source]
        return symbol_dict

    
    def average(symbols:list , data: list):
        """Calcula la media de precios ajustados por símbolo y fuente.
            Retorna: {fuente: {symbol: promedio}}"""

        adj_close_prices = DailyPrice.extract_adj_close_prices(symbols, data)

        average = {}

        for symbol in symbols:
            prices = adj_close_prices.get(symbol, [])
            calcule_average = sum(prices) / len(prices) if prices else 0
            average[symbol] = calcule_average
            print(f"El precio medio de cierre ajustado para el valor {symbol} es: {calcule_average:.2f}")

    def standard_deviation(symbols: list, data: list) -> float:
        """ Calcula la desviación típica de los precios de cierre por cada fuente de datos y cada simbolo."""
    
        adj_close_prices = DailyPrice.extract_adj_close_prices(symbols, data)

        deviation = {}
        for symbol in symbols:
            prices = adj_close_prices.get(symbol, [])    # extraer la lista de precios ajustados por cada símbolo
            if len(prices) > 1:
                deviation[symbol] = statistics.stdev(prices)
            else:
                deviation[symbol] = 0.0
            print(f"Desviación típica del precio de cierre ajustado para el valor {symbol} es: {deviation[symbol]:.2f}")

    def calculate_risk_parity_weights(symbols: list, data: list) -> dict:
        """Calcula los pesos de risk parity a partir de precios ajustados.
            Entrada: {symbol: [adj_close, adj_close, ...]}
            Salida: {symbol: peso} """
        
        print("CALCULO DE RISK PARITY WEIGHTS")
        adj_close_prices = DailyPrice.extract_adj_close_prices(symbols, data)

        volatilities = {}

        for symbol, prices in adj_close_prices.items():
            if len(prices) < 2:
                volatilities[symbol] = np.inf  # penaliza series muy cortas
                continue
            log_returns = np.diff(np.log(prices))
            vol = np.std(log_returns)
            volatilities[symbol] = vol if vol > 0 else np.inf  # evita división por cero

        # Inverso de la volatilidad
        inv_vol = {symbol: 1 / vol for symbol, vol in volatilities.items()}
        total = sum(inv_vol.values())
        weights = {symbol: inv_vol[symbol] / total for symbol in inv_vol}

        print("Pesos de risk parity:")
        for symbol, weight in weights.items():
            print(f"  {symbol}: {weight:.4f}")

        return weights
