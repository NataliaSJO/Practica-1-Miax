import argparse
import requests
import datetime

import extractor
fecha_fin = datetime.datetime.now()

year_ago = 15
def calculate_init_date_yf(range):
    range_text = range
    last_char_range = range_text[-1]
    time = int(range_text[:-1])
    print(last_char_range)
    print(time)

    if(last_char_range == 'y'):
        init_date = datetime.datetime(fecha_fin.year - time, fecha_fin.month, fecha_fin.day)
        print(init_date)
        return init_date

def call_api_yf(symbol, interval, range, fecha_init):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
  
    fecha_fin = datetime.datetime.now()

    params = {
           'interval': interval,
           'range': range,
           'period1': fecha_init.timestamp(),
           'period2': fecha_fin.timestamp()
       }
    
    response = requests.get(url, params=params)

    print(response.status_code)
    print(response.text)

    if response.headers.get("Content-Type") == "application/json":
        data = response.json()
    else:
        print("La respuesta no es JSON:", response.text)

    print(response)

    
def call_api_alpha(symbol, interval, range):
    api_key = 'LMD40040TKC5WMWM'

    """Symbol for the US no supported IBEX"""

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

  
    fecha_fin = datetime.datetime.now()

    params = {
        'symbol': symbol, #IBM, AAPL,
        'function': 'TIME_SERIES_DAILY',
       }
    
    response = requests.get(url, params=params)

    print(response.status_code)
    print(response.text)

    if response.headers.get("Content-Type") == "application/json":
        data = response.json()
    else:
        print("La respuesta no es JSON:", response.text)

    print(f"Esta es la respuesta: \n {response}")

#def calculate_init_date(range):
#    range_text = range
#    last_char_range = range_text[-1]
#    time = int(range_text[:-1])
#
#    if(last_char_range == 'y'):
#        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=365*time)
#        print(f"Datos desde{cutoff_date.date()}:\n")
#    
#    for date_str in sorted(time_series.keys(), reverse=True):
#        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
#        if date_obj >= cutoff_date:
#            close_price = time_series[date_str]["4. close"]
#            print(f"{date_str}: {close_price}")


def main():
    parser = argparse.ArgumentParser(description="Consulta los datos historicos de una accion o un indece desde la terminal")
    
    parser.add_argument("--source", nargs='+', type=str, default=["alpha_vantage"], help="Fuente de datos disponibles (ej: alpha_vantage, yahoo_finance, finnhub)")
    
    parser.add_argument("--symbol", nargs='+', type=str, default=["^IBEX"], help="Símbolo del activo (ej. AAPL, SAN.MC)")
    parser.add_argument("--interval", type=str, default="1d", help="Intervalo de datos (ej. 1d, 1wk)")
    parser.add_argument("--range", type=str, default="5y", help="Rango de tiempo (ej. 5d, 1mo, 1y)")
   
  #3  parser.add_argument("--format", type=str, default="json", help="Hay dos formatos disponibles (ej: json, csv)")
    args = parser.parse_args()
    print(vars(args))
    
    print(args.symbol)


   
    api_key_alpha = 'LMD40040TKC5WMWM'
    api_key_finnhub = 'XXXXXXXX'
    
    my_extractor = Extractor.Extractor(alpha_vantage_key=api_key_alpha, finnhub_key=api_key_finnhub)

    print(datetime.datetime.now())
    print(args.source)

    
    print(my_extractor.get_multiple_outputs(args.symbol, args.source, args.range))
   # if (len(args.source)) == 1 and args.source == ['alpha_vantage']:    
   #     for ticker in args.symbol:
   #         data_alpha = my_extractor.get_alpha_vantage(ticker)
   #         print(data_alpha)
#
   # elif args.source == ["yahoo_finance"]:
   #     for ticker in args.symbol:
   #         data_yf = my_extractor.get_yahoo_finance(ticker, args.range)
   #         print(data_yf)
#
   # elif args.source == ["finnhub"]:
   #     for ticker in args.symbol:
   #         data_finnhub = my_extractor.get_yahoo_finance(ticker)
   #         print(data_finnhub)
#
  #  return data_alpha, data_yf            

if __name__ == "__main__":
    main()
   


    #
    #python useApi.py --symbol SAN.MC --interval 1d --range 10y