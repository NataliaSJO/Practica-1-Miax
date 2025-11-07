import datetime

from matplotlib.dates import relativedelta

class DateUtils:
    """Clase con métodos estáticos para el manejo de fechas."""
    def __init__(self):
        self.end_date = datetime.datetime.now()

    def calculate_init_date(self, range: str) -> datetime:
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

        raise ValueError("Formato invalido. Usa 'y' para años, 'm' para meses, o 'd' para días.")
