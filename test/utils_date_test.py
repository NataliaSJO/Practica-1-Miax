import pytest
import datetime
from src.utils.utils_date import DateUtils  # ajusta el import según tu estructura

@pytest.fixture
def end_date():
    return datetime.datetime(2025, 11, 2)

@pytest.fixture
def date_utils(end_date):
    dateUtils = DateUtils()
    dateUtils.end_date = end_date
    return dateUtils

def test_calculate_years(date_utils):
    assert date_utils.calculate_init_date("2y") == datetime.datetime(2023, 11, 2)

def test_calculate_months_under_12(date_utils):
    assert date_utils.calculate_init_date("5m") == datetime.datetime(2025, 6, 2)

def test_calculate_months_over_12(date_utils):
    assert date_utils.calculate_init_date("15m") == datetime.datetime(2024, 8, 2)

def test_calculate_days_under_30(date_utils):
    assert date_utils.calculate_init_date("10d") == datetime.datetime(2025, 10, 23)

def test_calculate_days_over_30(date_utils):
    assert date_utils.calculate_init_date("45d") == datetime.datetime(2025, 9, 18)

def test_invalid_range(date_utils):
    with pytest.raises(ValueError):
        date_utils.calculate_init_date("3w")