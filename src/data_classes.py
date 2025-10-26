import numpy as np
import matplotlib.pyplot as plt
import statistics
from dataclasses import dataclass,asdict
from datetime import date

from typing import Iterable, List, Optional

@dataclass
class DailyPrice:
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

    def to_dict(self) -> dict:
        return asdict(self)


class PriceSeries:
    def __init__(self, prices: Optional[Iterable[DailyPrice]] = None):
        self.prices: List[DailyPrice] = sorted(
            list(prices) if prices else [],
            key=lambda p: p.date
        )

    def append(self, p: DailyPrice) -> None:
        self.prices.append(p)
        self.prices.sort(key=lambda x: x.date)

    def extend(self, items: Iterable[DailyPrice]) -> None:
        self.prices.extend(items)
        self.prices.sort(key=lambda x: x.date)

    def mean_close(self) -> float:
        if not self.prices:
            return 0.0
        return statistics.mean(p.close for p in self.prices)

    def mean_open(self) -> float:
        if not self.prices:
            return 0.0
        return statistics.mean(p.open for p in self.prices)

    def mean_volume(self) -> float:
        if not self.prices:
            return 0.0
        return statistics.mean(p.volume for p in self.prices)

    def moving_average_close(self, window: int) -> List[Optional[float]]:
        if window <= 0:
            raise ValueError("window must be > 0")
        closes = [p.close for p in self.prices]
        result: List[Optional[float]] = []
        for i in range(len(closes)):
            if i + 1 < window:
                result.append(None)
            else:
                window_slice = closes[i + 1 - window:i + 1]
                result.append(sum(window_slice) / window)
        return result

    def filter_by_date_range(self, start: date, end: date) -> "PriceSeries":
        filtered = [p for p in self.prices if start <= p.date <= end]
        return PriceSeries(filtered)

    def returns(self) -> List[float]:
        if len(self.prices) < 2:
            return []
        return [self.prices[i+1].close / self.prices[i].close - 1 for i in range(len(self.prices)-1)]

    def mean_return(self) -> float:
        r = self.returns()
        return statistics.mean(r) if r else 0.0

    def to_lists(self):
        dates = [p.date for p in self.prices]
        closes = [p.close for p in self.prices]
        opens = [p.open for p in self.prices]
        volumes = [p.volume for p in self.prices]
        return {"dates": dates, "opens": opens, "closes": closes, "volumes": volumes}
