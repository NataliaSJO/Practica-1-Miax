from data_classes import DailyPrice 
import datetime

class Utils:
    def __init__(self, extractor):
        self.prices = self._convert(extractor.data_series)
        
        
    def _convert(self, time_series: dict) -> list[DailyPrice]:
        print(time_series)
        list_price = []
        for date_str, data in time_series.items():
            fecha = datetime.strptime(date_str, "%Y-%m-%d").date()
            list_price.append(
                DailyPrice(
                    date=fecha,
                    open=float(data["1. open"]),
                    high=float(data["2. high"]),
                    low=float(data["3. low"]),
                    close=float(data["4. close"]),
                    volume=int(data["5. volume"])
                )
            )
        print(list_price)
        return sorted(list_price, key=lambda p: p.date)
    