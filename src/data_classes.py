import numpy as np
import matplotlib.pyplot as plt
import statistics
from dataclasses import dataclass
from datetime import date

@dataclass
class DailyPrice:
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int
    
    @staticmethod
    def extract_adj_close_prices(data: dict) -> dict:
        """Extrae los precios de cierre ajustado desde un dict anidado por fuente y símbolo.
        Espera formato: {fuente: {symbol: [DailyPrice, DailyPrice, ...]}}
        Devuelve: {symbol: [adj_close, ...]}. Los datos de la primera fuente encontrada."""
        first_source = next(iter(data))
        symbol_dict = data[first_source]


        price_adj_close = {
                symbol: [dp.adj_close for dp in daily_prices]
                for symbol, daily_prices in symbol_dict.items()
            }

        return price_adj_close

    @staticmethod
    def average(symbols:list , data: list):
        """
        Calcula la media de precios ajustados por símbolo usando la primera fuente.
        Devuelve: {symbol: media}
        """
        adj_close_prices = DailyPrice.extract_adj_close_prices(data)


        average = {}

        for symbol in symbols:
            prices = adj_close_prices.get(symbol, [])
            calculate_average = sum(prices) / len(prices) if prices else 0
            average[symbol] = calculate_average
            print(f"El precio medio de cierre ajustado para el valor {symbol} es: {calculate_average:.2f}")
        
        return average
    
    @staticmethod
    def standard_deviation(symbols: list, data: list) -> float:
        """Calcula la desviación típica por símbolo usando la primera fuente.
        Devuelve: {symbol: desviación}"""

        adj_close_prices = DailyPrice.extract_adj_close_prices(data)

        deviation = {}
        for symbol in symbols:
            prices = adj_close_prices.get(symbol, [])    # extraer la lista de precios ajustados por cada símbolo
            if len(prices) > 1:
                deviation[symbol] = statistics.stdev(prices)
            else:
                deviation[symbol] = 0.0
            print(f"Desviación típica del precio de cierre ajustado para el valor {symbol} es: {deviation[symbol]:.2f}")
        
        return deviation
    
    @staticmethod
    def calculate_risk_parity_weights(symbols: list, data: list) -> dict:
        """Calcula los pesos de risk parity a partir de precios ajustados.
            Entrada: {symbol: [adj_close, adj_close, ...]}
            Salida: {symbol: peso} """
        
        adj_close_prices = DailyPrice.extract_adj_close_prices(data)

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
