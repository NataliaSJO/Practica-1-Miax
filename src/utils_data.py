# utils.py
from datetime import datetime
from typing import List, Dict, Any
from data_classes import DailyPrice


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

def convert_to_dailyprice(time_series: List[Dict[str, Any]]) -> List[DailyPrice]:
    """Convierte los datos estandarizados en objetos DailyPrice."""
    list_price = []
    for data in time_series:
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