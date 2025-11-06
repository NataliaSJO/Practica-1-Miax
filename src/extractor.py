from collections import defaultdict
import json
import requests
import yfinance as yf
import io
from datetime import date, datetime
from typing import List, Dict, Any
import time

import os
from utils.utils_date import DateUtils
from utils.utils_data import clean_daily_prices, standard_data, convert_to_dailyprice

from utils.utils_file import FileUtils

from data_classes import DailyPrice
from report import Portfolio 
class Extractor:
    def __init__(self, marketstack_key: str, tiingo_key: str):
        self.marketstack_key = marketstack_key
        self.tiingo_key = tiingo_key
        self.date_utils = DateUtils()

    def get_yahoo_finance(self, symbols: list, source: str, format: str, range: str) -> Dict[str, List[DailyPrice]]:
        """Obtiene los precios historicos de Yahoo_Finance para una lista de símbolos.
        Como argumentos:
            - symbols: lista de símbolos a consultar
            - source: fuente de datos
            - format: formato de salida (json, csv)
            - range: rango de tiempo
        Se estandarizan, convierten y limpian los datos obtenidos.
        Devuelve un diccionario con los símbolos como claves y listas de objetos DailyPrice como valores."""

        start_date = self.date_utils.calculate_init_date_yf(range)
        all_converted: Dict[str, List[DailyPrice]] = {}
     
        for symbol in symbols:
            
            data = yf.download(symbol, start=start_date, end=datetime.now().strftime('%Y-%m-%d'), group_by='column', auto_adjust=False, progress=False)
            
            prices = [{
                "date": str(date.date()), #la fecha tiene que tener formatio YYYY-MM-dd
                "open": entry["Open"],
                "high": entry["High"],
                "low": entry["Low"],
                "close": entry["Close"],
                "adj_close": entry.get("Adj Close", entry["Close"]),
                "volume": entry["Volume"]
            } for date, entry in data.iterrows()]

            standardized = standard_data(source, prices)

            folder_origin = f"output_{source}_original".lower()
            FileUtils.save_output(standardized, symbol, source, format, folder_origin)

            converted = convert_to_dailyprice(standardized)
            cleaned = clean_daily_prices(converted)

            if symbol not in all_converted:
                all_converted[symbol] = []
            all_converted[symbol].extend(cleaned)

        return all_converted

   
    def get_marketstack_prices(self, symbols: list, source: str, format: str, range: str) -> Dict[str, List[DailyPrice]]:
        """Obtiene los precios historicos de Marketstack para una lista de símbolos.
        Como argumentos:
            - symbols: lista de símbolos a consultar
            - source: fuente de datos
            - format: formato de salida (json, csv)
            - range: rango de tiempo
        Marketstack devuelve todos los datos en una sola lista, por lo que hay que agruparlos por símbolo para pode trabajar con ellos.
        Se estandarizan, convierten y limpian los datos obtenidos.
        Devuelve un diccionario con los símbolos como claves y listas de objetos DailyPrice como valores.
        """
        all_converted = {}

        start_date = self.date_utils.calculate_init_date_yf(range)

       # limit = self.date_utils.calculate_init_date_ms(range, include_leap_years=True)
        #print(limit)
        url = f"http://api.marketstack.com/v1/eod"

        all_data = []
        offset = 0
        limit = 100

        while True:
            params = {
                "access_key": self.marketstack_key,
                "symbols": ",".join(symbols), #Convierte la lista en un string serparado por comas
                "date_from": start_date.strftime('%Y-%m-%d'),
                "date_to": datetime.now().strftime('%Y-%m-%d'),
                "limit":  limit, 
                "offset": offset
            }

            response = requests.get(url, params=params)
            # handle non-200 responses and non-JSON bodies gracefully
            if response.status_code != 200:
                print(f"Marketstack API returned status {response.status_code}: {response.text}")
                return {}
            try:
                data = response.json()
            except ValueError as e:
                # JSON decoding failed (empty body or invalid JSON)
                print("Error decoding JSON from Marketstack response:", e)
                print("Response text:", response.text[:1000])
                return {}
           
            if "data" not in data:
                print("Error o respuesta vacía:", data)
                return {}
            
            all_data.extend(data["data"])
            offset += limit

            # para la paginacion si la longitud de la pagina es menor que el limite
            if len(data.get("data", [])) < limit:
                break
       
        grouped = defaultdict(list)
        for entry in all_data:
            grouped[entry["symbol"]].append(entry)

        for symbol in symbols:
            entries = grouped.get(symbol, [])
            prices = [{
                "date": entry["date"][:10],  # YYYY-MM-DD
                "open": entry["open"],
                "high": entry["high"],
                "low": entry["low"],
                "close": entry["close"],
                "adj_close": entry.get("adj_close", entry["close"]), 
                "volume": entry["volume"]
            } for entry in entries]

            standardized = standard_data(source, prices)

            folder_origin = f"output_{source}_original".lower()
            FileUtils.save_output(standardized, symbol, source, format, folder_origin)

            converted = convert_to_dailyprice(standardized)
            cleaned = clean_daily_prices(converted)

            if symbol not in all_converted:
                all_converted[symbol] = []
                all_converted[symbol].extend(cleaned)
    
        return all_converted

    def get_tiingo(self, symbols: list, source: str, format: str, range: str, resampleFreq: str = "daily") -> Dict[str, List[DailyPrice]]:
        """Obtener precios históricos desde la API de Tiingo en formato CSV.
        Como argumentos:   
            - symbols: lista de símbolos (tickers)
            - source: cadena usada por standard_data (ej. 'tiingo')
            - format: 'csv' o 'json' para el archivo de salida (seguimos usando csv/json naming)
            - start_date, end_date: strings 'YYYY-MM-DD' (end_date default = hoy)
            - resampleFreq: frecuencia de resampleo aceptada por Tiingo ('daily','monthly',...)
        Devuelve dict {symbol: [DailyPrice, ...]} similar a otros métodos del extractor."""


        start_date = self.date_utils.calculate_init_date_yf(range)
        all_converted: Dict[str, List[DailyPrice]] = {}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.tiingo_key}"
        }

        base_url = "https://api.tiingo.com/tiingo/daily/{ticker}/prices"

        for symbol in symbols:
            url = base_url.format(ticker=symbol)
            params = {
                "startDate": start_date,
                "endDate": datetime.now().strftime("%Y-%m-%d"),
                "format": format,
                "resampleFreq": resampleFreq,
            }

            try:
                response = requests.get(url, params=params, headers=headers, timeout=20)
            except requests.RequestException as e:
                print(f"Request error for {symbol} -> {e}")
                continue

            if response.status_code != 200:
                print(f"Tiingo returned status {response.status_code} for {symbol}: {response.text[:200]}")
                continue

            try:
                data = response.json()
            except ValueError as e:
                print(f"Error decoding JSON from Tiingo for {symbol}: {e}")
                print("Response snippet:", response.text[:500])
                continue

    
            prices = []
            for entry in data:
                date_raw = entry.get("date") or entry.get("Date")
                if date_raw:
                    try:
                        date_val = datetime.fromisoformat(date_raw.replace("Z", "")).strftime("%Y-%m-%d")
                    except Exception:
                        date_val = str(date_raw)[:10]
                else:
                    date_val = None

                prices.append({
                    "date": date_val,
                    "open": entry.get("open"),
                    "high": entry.get("high"),
                    "low": entry.get("low"),
                    "close": entry.get("close"),
                    "adj_close": entry.get("adjClose", entry.get("close")),
                    "volume": entry.get("volume"),
                })
         
            standardized = standard_data(source, prices)
            folder_origin = f"output_{source}_original".lower()
            FileUtils.save_output(standardized, symbol, source, format, folder_origin)

            converted = convert_to_dailyprice(standardized)
            cleaned = clean_daily_prices(converted)

            if symbol not in all_converted:
                all_converted[symbol] = []
            all_converted[symbol].extend(cleaned)

        return all_converted


    def get_multiple_outputs(self, symbols:list, source:str, format:str, range:str)-> Dict[str, Dict[str, List[DailyPrice]]]:    
        """Obtiene múltiples series de datos simultáneamente.
        Como argumentos:
            - symbols: lista de símbolos a consultar
            - source: lista de fuentes de datos
            - format: formato de salida (json, csv)
            - range: rango de tiempo
        Devuelve un diccionario con los resultados de cada fuente de datos."""

        all_results: Dict[str, Dict[str, List[DailyPrice]]] = {}
        
        for source in source:
            if source == "marketstack":
                results = self.get_marketstack_prices(symbols, source, format, range)
                all_results["marketstack"] = results
            elif source == "yahoo_finance":
                results = self.get_yahoo_finance(symbols, source, format, range)
                all_results["yahoo_finance"] = results
            elif source == "tiingo":
                results = self.get_tiingo(symbols, source, format, range)
                all_results["tiingo"] = results    
        return all_results