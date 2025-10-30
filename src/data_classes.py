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

    def to_dict(self) -> dict: 
        print(asdict(self))
        return asdict(self)
    
    def average(symbols:list , data: list) -> float:
        print(f"SIMBOLOS: {symbols}")
        for symbol in symbols:
            data_per_symbol = data[symbol]  # Obtener los datos para cada símbolo
            prices= data_per_symbol[0]  #lista de DailyPrice
       
            total = sum(dp.adj_close for dp in prices)
            average = total / len(prices) if prices else 0
            print(f"El precio medio de cierre ajustado para {symbol} es: {average:.2f}")

    def standard_deviation(symbols: list, data: list) -> float:
        """ Calcula la desviación típica de los precios de cierre por cada symbol."""
        print(f"SIMBOLOS: {symbols}")
        deviation = {}
        for symbol in symbols:
            data_per_symbol = data[symbol]  # lista anidada: [[DailyPrice, ...]]
            precios = data_per_symbol[0]    # extraer la lista real
            adj_close = [dp.adj_close for dp in precios]

            if len(adj_close) > 1:
                deviation[symbol] = statistics.stdev(adj_close)
            else:
                deviation[symbol] = 0.0

            print(f"Desviación típica del precio de cierre ajsutado para {symbol}: {deviation[symbol]:.2f}")

