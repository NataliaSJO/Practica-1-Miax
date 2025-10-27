import json
import requests
import yfinance as yf
from datetime import datetime
from typing import List, Dict, Any

import os

from utils_data import standard_data, convert_to_dailyprice

from utils_file import save_output

from data_classes import DailyPrice
 
class Extractor:
    def __init__(self, marketstack_key):
        self.marketstack_key = marketstack_key
        self.data_series = []


    def get_yahoo_finance(self, symbol: str, source: str, format:str, range: str):
        data = yf.download(symbol, start = '2025-10-01', end = datetime.now().strftime('%Y-%m-%d'), group_by='column', auto_adjust=False, progress=False)

        prices = [{
            "date": str(date.date()), #la fecha tiene que tener formatio YYYY-MM-dd
            "open": entry["Open"],
            "high": entry["High"],
            "low": entry["Low"],
            "close": entry["Close"],
            "adj_close": entry.get("Adj Close", entry["Close"]),
            "volume": entry["Volume"]
        } for date, entry in data.iterrows()]
        standardized = standard_data(prices, "yahoo_finance")

        print("STANDARDIZED\n")
        print(standardized)
        print(type(standardized))
        folder_origin = f"{source}_original".lower()
        save_output(standardized, symbol, source, format, folder_origin)
        
        
        converted = convert_to_dailyprice(standardized)
    
        print("CONVERTED\n")
        print(converted)
        print(type(converted))
        return converted

   
    def get_marketstack_prices(self, symbol: str, range: str, source: str, format:str):

        url = f"http://api.marketstack.com/v1/eod"
        params = {
            "access_key": self.marketstack_key,
            "symbols": 'AAPL',
            "limit": 100  # número de días
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "data" not in data:
            print("Error o respuesta vacía:", data)
            return []

        prices = [{
            "date": entry["date"][:10],  # YYYY-MM-DD
            "open": entry["open"],
            "high": entry["high"],
            "low": entry["low"],
            "close": entry["close"],
            "adj_close": entry.get("adj_close", entry["close"]), 
            "volume": entry["volume"]
        } for entry in data["data"]]

        standardized = standard_data(prices, "marketstack")
        return convert_to_dailyprice(standardized)


    def get_multiple_outputs(self, symbols, source, format, range):

        """Obtiene múltiples series de datos simultáneamente."""
        results = {}
        for symbol, source in zip(symbols, source):
            if source == "marketstack":
                results[symbol] = self.get_marketstack_prices(symbol, source, format, range)
            elif source == "yahoo_finance":
                results[symbol] = self.get_yahoo_finance(symbol, source, format, range)
        return results
    
