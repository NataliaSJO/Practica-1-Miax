import pytest
import pandas as pd
from datetime import date
from src.utils.utils_data import standard_data, convert_to_dailyprice, clean_daily_prices
from src.data_classes import DailyPrice

@pytest.fixture
def raw_data():
    return [
        {
            "date": "2025-10-24",
            "open": pd.Series([261.19], name="2025-10-24"),
            "high": pd.Series([264.13], name="2025-10-24"),
            "low": pd.Series([259.18], name="2025-10-24"),
            "close": pd.Series([262.82], name="2025-10-24"),
            "adj_close": pd.Series([262.82], name="2025-10-24"),
            "volume": pd.Series([38253700.0], name="2025-10-24")
        },
        {
            "date": "2025-10-27",
            "open": pd.Series([264.88], name="2025-10-27"),
            "high": pd.Series([269.12], name="2025-10-27"),
            "low": pd.Series([264.65], name="2025-10-27"),
            "close": pd.Series([268.81], name="2025-10-27"),
            "adj_close": pd.Series([268.81], name="2025-10-27"),
            "volume": pd.Series([44888200.0], name="2025-10-27")
        }
    ]
@pytest.fixture
def valid_daily_price():
    return [
        DailyPrice(date=date(2025, 1, 1), open=100.0, high=110.0, low=95.0,
                   close=105.0, adj_close=104.5, volume=1000000),
        DailyPrice(date=date(2023, 1, 2), open=101.0, high=111.0, low=96.0,
                   close=106.0, adj_close=105.5, volume=900000)
    ]
@pytest.fixture
def invalid_daily_price():   
    return [
        DailyPrice(date=date(2025, 10, 1), open=None, high=110.0, low=95.0,
                   close=105.0, adj_close=104.5, volume=1000000),
        DailyPrice(date=date(2025, 10, 2), open=100.0, high=110.0, low=95.0,
                   close=0.0, adj_close=104.5, volume=1000000),
        DailyPrice(date=date(2025, 10, 3), open=100.0, high=110.0, low=95.0,
                   close=105.0, adj_close=float("nan"), volume=1000000)
    ]   

def standard_data_test():
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
            "open": pd.Series([101.0]),
            "high": pd.Series([112.0]),
            "low": pd.Series([96.0]),
            "close": pd.Series([106.0]),
            "adj_close": pd.Series([105.5]),
            "volume": pd.Series([900000])
        }
    ]


def test_standard_data_structure(raw_data):
    result = standard_data(raw_data)
    assert isinstance(result, list)
    assert all(isinstance(entry, dict) for entry in result)
    for entry in result:
        assert set(entry.keys()) == {
            "date", "open", "high", "low", "close", "adj_close", "volume"
        }

def test_standard_data_values(raw_data):
    result = standard_data(raw_data)
    assert result[0]["date"] == "2025-10-24"
    assert result[0]["open"] == 261.19
    assert result[0]["high"] == 264.13
    assert result[0]["low"] ==  259.18
    assert result[0]["close"] == 262.82
    assert result[0]["adj_close"] == 262.82
    assert result[0]["volume"] == 38253700

    assert result[1]["date"] == "2025-10-27"
    assert result[1]["volume"] == 44888200


def test_convert_to_dailyprice(raw_data):
    standardized = standard_data(raw_data)
    daily_prices = convert_to_dailyprice(standardized)
    assert daily_prices[0].date == date(2025, 10, 24)
    assert daily_prices[1].volume == 44888200

def test_clean_daily_prices_valid(valid_daily_price):
    
    cleaned = clean_daily_prices(valid_daily_price)
    assert len(cleaned) == 2

    assert isinstance(cleaned[0], DailyPrice)
    


def test_clean_daily_prices_invalid(invalid_daily_price):
  
   result = clean_daily_prices(invalid_daily_price)
   assert len(result) == 0
