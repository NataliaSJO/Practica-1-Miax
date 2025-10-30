import json
import requests
import yfinance as yf
from datetime import datetime
from typing import List, Dict, Any

import os
from utils_date import calculate_init_date_yf, calculate_init_date_ms
from utils_data import standard_data, convert_to_dailyprice

from utils_file import save_output

from data_classes import DailyPrice
 
class Extractor:
    def __init__(self, marketstack_key):
        self.marketstack_key = marketstack_key
        self.data_series = []


    def get_yahoo_finance(self, symbols: list, source: str, format:str, range: str):
        start_date = calculate_init_date_yf(range)
        all_converted = {}
        print(f"symbols: {symbols}")
        for symbol in symbols:
            print(f"symbol: {symbol}")
            data = yf.download(symbol, start = start_date, end = datetime.now().strftime('%Y-%m-%d'), group_by='column', auto_adjust=False, progress=False)


            prices = [{
                "date": str(date.date()), #la fecha tiene que tener formatio YYYY-MM-dd
                "open": entry["Open"],
                "high": entry["High"],
                "low": entry["Low"],
                "close": entry["Close"],
                "adj_close": entry.get("Adj Close", entry["Close"]),
                "volume": entry["Volume"]
            } for date, entry in data.iterrows()]
            standardized = standard_data(prices)

            #print("STANDARDIZED\n")
            #print(standardized)
            #print(type(standardized))
            folder_origin = f"{source}_original".lower()
            save_output(standardized, symbol, source, format, folder_origin)


            converted = convert_to_dailyprice(standardized)

            if symbol not in all_converted:
                all_converted[symbol] = []
            all_converted[symbol].append(converted)

        print("ALL CONVERTED\n")
        print(all_converted)    
        return all_converted

   
    def get_marketstack_prices(self, symbols: list, source: str, format:str, range: str):
        all_converted = {}

        limit = calculate_init_date_ms(range, include_leap_years=True)
        url = f"http://api.marketstack.com/v1/eod"
        params = {
            "access_key": self.marketstack_key,
            "symbols": symbols,
            "limit":  limit # número de días
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "data" not in data:
            print("Error o respuesta vacía:", data)
            return []
        for symbol in symbols:
            prices = [{
                "date": entry["date"][:10],  # YYYY-MM-DD
                "open": entry["open"],
                "high": entry["high"],
                "low": entry["low"],
                "close": entry["close"],
                "adj_close": entry.get("adj_close", entry["close"]), 
                "volume": entry["volume"]
            } for entry in data["data"]]

            standardized = standard_data(prices)

            print("STANDARDIZED\n")
            print(standardized)
            print(type(standardized))

            folder_origin = f"{source}_original".lower()
            save_output(standardized, symbol, source, format, folder_origin)

            converted = convert_to_dailyprice(standardized)
            if symbol not in all_converted:
                all_converted[symbol] = []
                all_converted[symbol].append(converted)

        print("ALL CONVERTED\n")
        print(all_converted)    
        return all_converted


    def get_multiple_outputs(self, symbols, source, format, range):

        """Obtiene múltiples series de datos simultáneamente."""
        for source in source:
            if source == "marketstack":
                results = self.get_marketstack_prices(symbols, source, format, range)
            elif source == "yahoo_finance":
                results = self.get_yahoo_finance(symbols, source, format, range)
    
        return results