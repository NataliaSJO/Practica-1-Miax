import pytest
import pandas as pd
from datetime import date
from utils.utils_data import standard_data, convert_to_dailyprice, clean_daily_prices
from utils.data_classes import DailyPrice

@pytest.fixture
def data_test():
    return [
        {
            "date": "2023-01-01",
            "open": pd.Series([100.0]),
            "high": pd.Series([110.0]),
            "low": pd.Series([95.0]),
            "close": pd.Series([105.0]),
            "adj_close": pd.Series([104.5]),
            "volume": pd.Series([1000000])
        },
        {
            "date": "2023-01-02",
            "open": pd.Series([None]),
            "high": pd.Series([112.0]),
            "low": pd.Series([96.0]),
            "close": pd.Series([106.0]),
            "adj_close": pd.Series([105.5]),
            "volume": pd.Series([900000])
        }
    ]

def test_standard_data(data_test):
    result = standard_data(data_test)
    assert isinstance(result, list)
    assert result[0]["open"] == 100.0
    assert result[0]["volume"] == 1000000
    assert result[1]["high"] == 112.0

def test_convert_to_dailyprice(data_test):
    standardized = standard_data(data_test)
    daily_prices = convert_to_dailyprice(standardized)
    assert isinstance(daily_prices[0], DailyPrice)
    assert daily_prices[0].date == date(2023, 1, 1)
    assert daily_prices[1].volume == 900000

def test_clean_daily_prices_valid():
    valid = [
        DailyPrice(date=date(2023, 1, 1), open=100.0, high=110.0, low=95.0,
                   close=105.0, adj_close=104.5, volume=1000000),
        DailyPrice(date=date(2023, 1, 2), open=101.0, high=111.0, low=96.0,
                   close=106.0, adj_close=105.5, volume=900000)
    ]
    cleaned = clean_daily_prices(valid)
    assert len(cleaned) == 2

def test_clean_daily_prices_invalid():
    invalid = [
        DailyPrice(date=date(2023, 1, 1), open=None, high=110.0, low=95.0,
                   close=105.0, adj_close=104.5, volume=1000000),
        DailyPrice(date=date(2023, 1, 1), open=100.0, high=110.0, low=95.0,
                   close=0.0, adj_close=104.5, volume=1000000),
        DailyPrice(date=date(2023, 1, 2), open=100.0, high=110.0, low=95.0,
                   close=105.0, adj_close=float("nan"), volume=1000000)
    ]
    cleaned = clean_daily_prices(invalid)
    assert len(cleaned) == 0
