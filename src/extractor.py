import requests
import yfinance as yf
from datetime import datetime
from typing import List, Dict, Any



from data_classes import DailyPrice
 
class Extractor:
    def __init__(self, marketstack_key):
        self.marketstack_key = marketstack_key
        self.data_series = []

    def _standard_data(self, data, source):
        """Se formatean los datos en el tipo que más interesa, float o int.
            entry es un diccionario con las keys: date, open, high, low, close, volume, source.
            Siendo todos datos de la api, y source el identificador del api.
            Devulve los datos estandarizados como una lista de diccionarios."""
        standard_data = []
        for entry in data:
            standard_data.append({
                "date": entry["date"],
                "open": float(entry["open"]),
                "high": float(entry["high"]),
                "low": float(entry["low"]),
                "close": float(entry["close"]),
                "adj_close": float(entry["adj_close"]),
                "volume": int(entry["volume"]),
                "source": source
            })
        return standard_data
   
    def _convert(self, time_series:List[Dict[str, Any]]) -> List[DailyPrice]:
        print(time_series)
        list_price = []
        for data in time_series:
            fecha = datetime.strptime(data["date"], "%Y-%m-%d").date()
            list_price.append(
                DailyPrice(
                    date= fecha,
                    open= float(data["open"]),
                    high= float(data["high"]),
                    low= float(data["low"]),
                    close= float(data["close"]),
                    adj_close= float(data["adj_close"]),
                    volume= int(data["volume"])
                )
            )
        print(list_price)
        return sorted(list_price, key=lambda p: p.date)
    

    def get_yahoo_finance(self, symbol, range):
        data = yf.download(symbol, start = '2000-01-01', end = datetime.now().strftime('%Y-%m-%d'), group_by='column', auto_adjust=False, progress=False)
    
        print(data.columns)
        prices = [{
            "date": str(date.date()), #la fecha tiene que tener formatio YYYY-MM-dd
            "open": entry["Open"],
            "high": entry["High"],
            "low": entry["Low"],
            "close": entry["Close"],
            "adj_close": entry.get("Adj Close", entry["Close"]),
            "volume": entry["Volume"]
        } for date, entry in data.iterrows()]
        # return self._standard_data(data, "yahoo_finance")

        print(self._convert(self._standard_data(prices, "yahoo_finance")))

        return(self._convert(self._standard_data(prices, "yahoo_finance")))
    
    def get_marketstack_prices(self, symbol: str, limit: int = 100):

        url = f"http://api.marketstack.com/v1/eod"
        params = {
            "access_key": self.marketstack_key,
            "symbols": 'AAPL',
            "limit": limit  # número de días
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

        print(self._convert(self._standard_data(prices, "marketstack")))    
               
        return(self._convert(self._standard_data(prices, "marketstack")))
     

    def get_multiple_outputs(self, symbols, source, range):

        print("ESTOY EN MULTIPLES OPCIONES")
        print(symbols)
        print(source)
        """Obtiene múltiples series de datos simultáneamente."""
        results = {}
        for symbol, source in zip(symbols, source):
            if source == "marketstack":
                results[symbol] = self.get_marketstack_prices(symbol, range)
            elif source == "yahoo_finance":
                results[symbol] = self.get_yahoo_finance(symbol, range)
        return results
    
