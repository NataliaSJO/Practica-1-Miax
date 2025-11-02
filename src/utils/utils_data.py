# utils_data.py
from datetime import datetime
from typing import List, Dict, Any
from src.data_classes import DailyPrice
import math
import pandas as pd

def safe_get(series: pd.Series, cast_type, field: str, date: str):
    if series is None or series.empty or series.iloc[0] is None:
        raise ValueError(f"Campo '{field}' vacío o inválido en la fecha {date}")
    return cast_type(series.iloc[0])

def standard_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convierte los datos obtenidos de las APIs en formato estandarizado."""
    return [{
        "date": entry["date"],
        "open": safe_get(entry["open"], float, "open", entry["date"]),
        "high": safe_get(entry["high"], float, "high", entry["date"]),
        "low": safe_get(entry["low"], float, "low", entry["date"]),
        "close": safe_get(entry["close"], float, "close", entry["date"]),
        "adj_close": safe_get(entry["adj_close"], float, "adj_close", entry["date"]),
        "volume": safe_get(entry["volume"], int, "volume", entry["date"]),
    } for entry in data]

#def standard_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#    """Convierte los datos obtenidos de las apis en formato estandarizado."""
#    return [{
#        "date": entry["date"],
#        "open": float(entry["open"].iloc[0]), #entry["open"] es un pd.Series con un solo valor. Con iloc[0] accedemos a ese valor por su posicion.
#        "high": float(entry["high"].iloc[0]),
#        "low": float(entry["low"].iloc[0]),
#        "close": float(entry["close"].iloc[0]),
#        "adj_close": float(entry["adj_close"].iloc[0]),
#        "volume": int(entry["volume"].iloc[0]),
#    } for entry in data]

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

    #print(f"Filtrados {len(data) - len(cleaned)} registros inválidos de {len(data)}.")
    return cleaned

