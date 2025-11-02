import datetime

fecha_fin = datetime.datetime.now()

def calculate_init_date_yf(range:str):
    range_text = range
    last_char_range = range_text[-1]
    time = int(range_text[:-1])
   
    if(last_char_range == 'y'):
        init_date = datetime.datetime(fecha_fin.year - time, fecha_fin.month, fecha_fin.day)
        return init_date
    if(last_char_range == 'm'):
        if time >= 12:
            years = time // 12
            months = time % 12
            init_date = datetime.datetime(fecha_fin.year - years, fecha_fin.month - months, fecha_fin.day)
            return init_date
        else:
            init_date = datetime.datetime(fecha_fin.year, fecha_fin.month - time, fecha_fin.day)
            return init_date
    if(last_char_range == 'd'):
        if time >= 30:
            months = time // 30
            days = time % 30
            init_date = datetime.datetime(fecha_fin.year, fecha_fin.month - months, fecha_fin.day - days)
            return init_date
        else:
            init_date = datetime.datetime(fecha_fin.year, fecha_fin.month, fecha_fin.day - time)
            return init_date
        
def calculate_init_date_ms(range:str, include_leap_years: bool = True):
    range_text = range
    last_char_range = range_text[-1]
    time = int(range_text[:-1])
   
    if(last_char_range == 'y'):
        days_per_year = 365.25 if include_leap_years else 365
        return time * days_per_year
    if(last_char_range == 'm'):
       days_per_month = 30.44  # promedio considerando años bisiestos
       return int(time * days_per_month)
    if(last_char_range == 'd'):
        return time