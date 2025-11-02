# utils_data.py
from datetime import datetime
from typing import List, Dict, Any
from data_classes import DailyPrice
import math

def standard_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convierte los datos crudos en formato estandarizado."""
    return [{
        "date": entry["date"],
        "open": float(entry["open"]),
        "high": float(entry["high"]),
        "low": float(entry["low"]),
        "close": float(entry["close"]),
        "adj_close": float(entry["adj_close"]),
        "volume": int(entry["volume"]),
    } for entry in data]

def convert_to_dailyprice(data: List[Dict[str, Any]]) -> List[DailyPrice]:
    """Convierte los datos estandarizados en objetos DailyPrice."""
    list_price = []
    for data in data:
        fecha = datetime.strptime(data["date"], "%Y-%m-%d").date()
        list_price.append(
            DailyPrice(
                date=fecha,
                open=data["open"],
                high=data["high"],
                low=data["low"],
                close=data["close"],
                adj_close=data["adj_close"],
                volume=data["volume"]
            )
        )
    return sorted(list_price, key=lambda p: p.date)



def clean_daily_prices(data: List[DailyPrice]) -> List[DailyPrice]:
    """
    Limpia una lista de objetos DailyPrice eliminando entradas inválidas:
    - Valores nulos o NaN
    - Precios o volumen negativos o cero
    - Fechas duplicadas
    """
    cleaned = []
    seen_dates = set()

    for daily_prices in data:
        if (
            daily_prices.date in seen_dates or
            daily_prices.open is None or daily_prices.high is None or daily_prices.low is None or
            daily_prices.close is None or daily_prices.adj_close is None or daily_prices.volume is None or
            any(map(lambda x: isinstance(x, float) and math.isnan(x), 
                    [daily_prices.open, daily_prices.high, daily_prices.low, daily_prices.close, daily_prices.adj_close])) or
            daily_prices.volume <= 0 or
            daily_prices.close <= 0 or daily_prices.adj_close <= 0
        ):
            continue
        seen_dates.add(daily_prices.date)
        cleaned.append(daily_prices)

    print(f"Filtrados {len(data) - len(cleaned)} registros inválidos de {len(data)}.")
    return cleaned

