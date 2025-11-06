import datetime

from matplotlib.dates import relativedelta

class DateUtils:
    """Clase con métodos estáticos para el manejo de fechas."""
    def __init__(self):
        self.end_date = datetime.datetime.now()

    def calculate_init_date_yf(self, range: str) -> datetime:
        """Calcula la fecha inicial restando el rando introducido por teclado a la fecha actual. Se usa para calcular la fecha de inicio para Yahoo Finance.
        Como argumentos:
            - range: str con el formato '5y', '3m', '10d'
            - end_date:  la fecha actual
        Devuelve un objeto datatime con la fecha inicial cualculada.
        Si el formato no es valido, lanza un ValueError."""

        last_char_range = range[-1]
        time = int(range[:-1])
    
        if last_char_range == 'y':
             return self.end_date - relativedelta(years=time)

        if last_char_range == 'm':
            return self.end_date - relativedelta(months=time)

        if last_char_range == 'd':
            return self.end_date - datetime.timedelta(days=time)

        raise ValueError("Formato invalido. Usa 'y' pa años, 'm' para meses, o 'd' para días.")

    
    def calculate_init_date_ms(self, range: str, include_leap_years: bool = True) -> int:
        """Calcula la fecha inicial restando el rando introducido por teclado a la fecha actual. Se usa para calcular la fecha de inicio para Marketstack.
        Como argumentos:
            - range: str con el formato '5y', '3m', '10d'
            - include_leap_years: bool que indica si considerar años bisiestos al calcular días.
        Devuelve un entero con el número de días a restar.
        Si el formato no es valido, lanza un ValueError."""
    
        last_char_range = range[-1]
        time = int(range[:-1])
    
        if last_char_range == 'y':
            days_per_year = 365.25 if include_leap_years else 365
            return time * days_per_year
        if last_char_range == 'm':
           days_per_month = 30.44  # promedio considerando años bisiestos
           return int(time * days_per_month)
        if last_char_range == 'd':
            return time
        raise ValueError("Formato invalido. Usa 'y' pa años, 'm' para meses, o 'd' para días.")
        