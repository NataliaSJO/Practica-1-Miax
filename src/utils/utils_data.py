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

def extract_value(value: Any) -> Any:
    """Extrae el valor numérico si es un objeto tipo pandas Series (Ticker)."""
    try:
        # Si es un objeto tipo Series, extrae el primer valor
        if hasattr(value, "values"):
            return value.values[0]
        return value
    except Exception as e:
        print(f"Error extrayendo valor: {e}")
        return None


def standard_data(source, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convierte los datos obtenidos de las APIs en formato estandarizado.
    Como argumentos:
    - data: lista de diccionarios con los datos originales.
    Devuelve una lista de diccionarios con los datos estandarizados.
    """
    standard_data = []
    if source == "yahoo_finance":
        for entry in data:
            standard_data.append({
               "date": entry["date"],
               "open": float(entry["open"].iloc[0]), #entry["open"] es un pd.Series con un solo valor. Con iloc[0] accedemos a ese valor por su posicion.
                "high": float(entry["high"].iloc[0]),
                "low": float(entry["low"].iloc[0]),
                "close": float(entry["close"].iloc[0]),
                "adj_close": float(entry["adj_close"].iloc[0]),
                "volume": int(entry["volume"].iloc[0]),
            })
        return standard_data
    
    if source == "tiingo":     
        for entry in data:
            standard_data.append({
                "date": entry["date"],
                "open": float(entry["open"]),
                "high": float(entry["high"]),
                "low": float(entry["low"]),
                "close": float(entry["close"]),
                "adj_close": float(entry.get("adj_close", entry["close"])),
                "volume": int(entry["volume"]),
            })        
        return standard_data

def convert_to_dailyprice(data: List[Dict[str, Any]]) -> List[DailyPrice]:
    """Convierte los datos estandarizados en objetos DailyPrice.
    Como argumentos:
    - data: lista de diccionarios con los datos estandarizados.
    Devuelve una lista de objetos DailyPrice ordenados por fecha."""

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
    """Limpia una lista de objetos DailyPrice eliminando entradas inválidas en los siguientes casos:
        - Valores nulos o NaN
        - Precios o volumen negativos o cero
        - Fechas duplicadas
    Como argumentos:
        - data: lista de objetos DailyPrice
    Devuelve una lista de objetos DailyPrice limpios."""

    cleaned = []
    seen_dates = set()

    for daily_prices in data:
        if (
            daily_prices.date in seen_dates or # Si la fecha ya esta en seen_dates, se considera duplicada y el valore se considera inválido
            daily_prices.open is None or daily_prices.high is None or daily_prices.low is None or
            daily_prices.close is None or daily_prices.adj_close is None or daily_prices.volume is None or #Si alguno de los valores para open, high, low, close, adj_close o volume es None, se considera inválido
            any(map(lambda x: isinstance(x, float) and math.isnan(x), #Si alguno de los valores es NaN, se considera inválido
                    [daily_prices.open, daily_prices.high, daily_prices.low, daily_prices.close, daily_prices.adj_close])) or
            daily_prices.volume <= 0 or
            daily_prices.close <= 0 or daily_prices.adj_close <= 0 #Si alguno de los campos volume, close o adj_close es menor o igual a 0, se considera inválido
        ):
            continue 
        seen_dates.add(daily_prices.date)  #Si pasa todas las validaciones, se añade la fecha al conjunto seen_dates
        cleaned.append(daily_prices) #Si pasa todas las validaciones, se añade a la lista cleaned

    return cleaned

