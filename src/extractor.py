import requests
import yfinance as yf
from datetime import datetime
from typing import List, Dict, Any



from Dt_Clases import DailyPrice
 
class Extractor:
    def __init__(self, alpha_vantage_key, finnhub_key):
        self.alpha_key = alpha_vantage_key
        self.finnhub_key = finnhub_key
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
                    date=fecha,
                    open=float(data["open"]),
                    high=float(data["high"]),
                    low=float(data["low"]),
                    close=float(data["close"]),
                    volume=int(data["volume"])
                )
            )
        print(list_price)
        return sorted(list_price, key=lambda p: p.date)
    
    def get_alpha_vantage(self, symbol, range):
        """Funcion que llama a la api de Alpha Vantage, capturando el error HTTPS en caso de ocurrir.
        Arguments:
            
        Sus parametros son: function(), symbol (introducido por terminal), apikey, 
        outputsize(full indica que solicita todos los datos históricos)"""

        url = f"https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.alpha_key,
            "outputsize": "compact" #PONER 'full' y filtrar por fechas usando el range
        }
        try:
            print("REQUEST ALPHA")
            response = requests.get(url, params=params).json()
        except requests.exceptions.RequestException as e:
            print("Error", e)
        time_series = response.get("Time Series (Daily)", {})
        
      #  init_date = today - range
      #  today = datetime.today()
      #  datos_filtrados = {
      #      fecha: valores
       #     for fecha, valores in time_series.items()
        #    if init_date <= fecha <= today
        #}
 
        data = [{
            "date": date,
            "open": prices["1. open"],
            "high": prices["2. high"],
            "low": prices["3. low"],
            "close": prices["4. close"],
            "volume": prices["5. volume"]
        } for date, prices in time_series.items()]
        print("ESTOY AQUI")
      #  print(self._standard_data(data, "alpha_vantage"))

        print(self._convert(self._standard_data(data, "alpha_vantage")))

        return(self._convert(self._standard_data(data, "alpha_vantage")))
       # return self._standard_data(data, "alpha_vantage")

    def get_yahoo_finance(self, symbol, range):
        ticker = yf.Ticker(symbol)
        historic = ticker.history(period=range)
        data = [{
            "date": str(date.date()), #la fecha tiene que tener formatio YYYY-MM-dd
            "open": prices["Open"],
            "high": prices["High"],
            "low": prices["Low"],
            "close": prices["Close"],
            "volume": prices["Volume"]
        } for date, prices in historic.iterrows()]
        return self._standard_data(data, "yahoo_finance")

    def get_finnhub(self, symbol):
        now = int(datetime.now().timestamp())
        past = now - 30 * 86400
        url = f"https://finnhub.io/api/v1/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": "D",
            "from": past,
            "to": now,
            "token": self.finnhub_key
        }
        response = requests.get(url, params=params).json()
        if response.get("s") != "ok":
            return "Error en la prespuesta"
        data = [{
            "date": datetime.utcfromtimestamp(t).strftime('%Y-%m-%d'),
            "open": o,
            "high": h,
            "low": l,
            "close": c,
            "volume": v
        } for t, o, h, l, c, v in zip(response["t"], response["o"], response["h"], response["l"], response["c"], response["v"])]
        return self._standard_data(data, "finnhub")

    def get_multiple_outputs(self, symbols, source, range):

        print("ESTOY EN MULTIPLES OPCIONES")
        print(symbols)
        print(source)
        """Obtiene múltiples series de datos simultáneamente."""
        results = {}
        for symbol, source in zip(symbols, source):
            if source == "alpha_vantage":
                results[symbol] = self.get_alpha_vantage(symbol, range)
            elif source == "yahoo_finance":
                results[symbol] = self.get_yahoo_finance(symbol, range)
            elif source == "finnhub":
                results[symbol] = self.get_finnhub(symbol)
        return results
    
