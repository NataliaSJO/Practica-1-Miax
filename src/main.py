import os
from dotenv import load_dotenv

import argparse

import extractor




def main():
    load_dotenv() # Carga las variables de entorno desde el archivo .env

    parser = argparse.ArgumentParser(description="Consulta los datos historicos de una accion o un indece desde la terminal")
    
    parser.add_argument("--source", nargs='+', type=str, default=["yaho_finance"], help="Fuente de datos disponibles (ej: yahoo_finance, marketstack)")
    
    parser.add_argument("--symbol", nargs='+', type=str, default=["^IBEX"], help="Símbolo del activo (ej. AAPL, SAN.MC)")
    parser.add_argument("--interval", type=str, default="1d", help="Intervalo de datos (ej. 1d, 1wk)")
    parser.add_argument("--range", type=str, default="5y", help="Rango de tiempo (ej. 5d, 1m, 1y)")
   
    parser.add_argument("--format", type=str, default="json", help="Hay dos formatos disponibles (ej: json, csv)")
    args = parser.parse_args()
   
    api_key_marketstack = os.getenv("MARKETSTACK_KEY")
 
    my_extractor = extractor.Extractor(marketstack_key = api_key_marketstack)

    my_extractor.get_multiple_outputs(args.symbol, args.source, args.format, args.range)
   # print(my_extractor.get_multiple_outputs(args.symbol, args.source, args.format, args.range))

    
    results = my_extractor.get_multiple_outputs(args.symbol, args.source, args.format, args.range)
    print("RESULTS")
    print(results)


    media = extractor.DailyPrice.media(args.symbol, results)


    deviation = extractor.DailyPrice.standard_deviation(args.symbol, results)
if __name__ == "__main__":
    main()
   





    #
    #python useApi.py --symbol SAN.MC --interval 1d --range 10y