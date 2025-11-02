import datetime

from matplotlib.dates import relativedelta

end_date = datetime.datetime.now()

def calculate_init_date_yf(range:str, end_date: datetime.datetime = end_date):
    last_char_range = range[-1]
    time = int(range[:-1])
   
    if(last_char_range == 'y'):
         return end_date - relativedelta(years=time)

    if(last_char_range == 'm'):
        return end_date - relativedelta(months=time)
        
    if(last_char_range == 'd'):
        return end_date - datetime.timedelta(days=time)

    raise ValueError("Invalid range format. Use 'y' for years, 'm' for months, or 'd' for days.")
        

def calculate_init_date_ms(range:str, include_leap_years: bool = True):
    last_char_range = range[-1]
    time = int(range[:-1])
   
    if(last_char_range == 'y'):
        days_per_year = 365.25 if include_leap_years else 365
        return time * days_per_year
    if(last_char_range == 'm'):
       days_per_month = 30.44  # promedio considerando años bisiestos
       return int(time * days_per_month)
    if(last_char_range == 'd'):
        return time