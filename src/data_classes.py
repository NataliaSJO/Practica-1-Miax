import numpy as np
import matplotlib.pyplot as plt
import statistics
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Any


@dataclass
class DailyPrice:
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

    def extract_adj_close_prices(self, data: Dict[str, Dict[str, List['DailyPrice']]]) -> Dict[str, List[float]]:
        """Extrae los precios de cierre ajustado desde un dict anidado por fuente y símbolo, cogiendo solo la primera fuente.
        Como argumento:
            - data: el resultado devuelto por el extractor. Su formato es: [source: [symbol: [DailyPrice, DailyPrice, ...]]]
        Devuelve: {symbol: [adj_close, ...]}. Los datos de la primera fuente encontrada."""

        first_source = next(iter(data))
        symbol_dict = data[first_source]

        price_adj_close: Dict[str, List[float]] = {
            symbol: [dp.adj_close for dp in daily_prices]
            for symbol, daily_prices in symbol_dict.items()
        }

        return price_adj_close

    def average(self, symbols: List[str], data: Dict[str, Dict[str, List['DailyPrice']]]) -> Dict[str, float]:
        """Calcula la media de precios ajustados por símbolo usando la primera fuente.
        Como argumentos:
            - symbols: lista de símbolos
            - data: datos devueltos por el extractor
        Devuelve: media por cada simbolo
        """
        adj_close_prices = self.extract_adj_close_prices(data)

        average: Dict[str, float] = {}
        for symbol in symbols:
            prices = adj_close_prices.get(symbol, [])
            calculate_average = sum(prices) / len(prices) if prices else 0.0
            average[symbol] = calculate_average

        return average

    def standard_deviation(self, symbols: List[str], data: Dict[str, Dict[str, List['DailyPrice']]]) -> Dict[str, float]:
        """Calcula la desviación típica por símbolo usando la primera fuente.
        Como argumentos:
            - symbols: lista de símbolos
            - data: datos devueltos por el extractor
        Devuelve: desviación por cada simbolo"""

        adj_close_prices = self.extract_adj_close_prices(data)

        deviation: Dict[str, float] = {}
        for symbol in symbols:
            prices = adj_close_prices.get(symbol, [])    # extraer la lista de precios ajustados por cada símbolo
            if len(prices) > 1:
                deviation[symbol] = statistics.stdev(prices)
            else:
                deviation[symbol] = 0.0

        return deviation

    def calculate_risk_parity_weights(self, symbols: List[str], data: Dict[str, Dict[str, List['DailyPrice']]]) -> Dict[str, float]:
        """Calcula los pesos de risk parity a partir de precios ajustados.
        Como argumentos:
            - symbols: lista de símbolos
            - data: lista de datos devueltos por el extractor. Dict[str, Dict[str, List[DailyPrice]]]
        Devuelve {symbol: peso}"""
        
        adj_close_prices = self.extract_adj_close_prices(data)

        volatilities: Dict[str, float] = {}
        for symbol, prices in adj_close_prices.items():
            if len(prices) < 2:
                volatilities[symbol] = float('inf')  # penaliza series muy cortas
                continue
            # retornos logarítmicos
            log_returns = np.diff(np.log(prices))
            vol = float(np.std(log_returns))
            volatilities[symbol] = vol if vol > 0 else float('inf') # evita división por cero

        # inverso de la volatilidad (si vol == inf -> inv = 0)
        inv_vol: Dict[str, float] = {symbol: (0.0 if vol == float('inf') else 1.0 / vol) for symbol, vol in volatilities.items()}
        total = sum(inv_vol.values())
        weights = {symbol: inv_vol[symbol] / total for symbol in inv_vol}

        return weights
