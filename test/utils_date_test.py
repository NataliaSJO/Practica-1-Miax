import pytest
import datetime
from src.utils.utils_date import calculate_init_date_ms, calculate_init_date_yf  # ajusta el import según tu estructura

@pytest.fixture
def end_date():
    return datetime.datetime(2025, 11, 2)

# Tests for calculate_init_date_yf
def test_calculate_years(end_date):
    result = calculate_init_date_yf("2y", end_date)
    assert result == datetime.datetime(2023, 11, 2)

def test_calculate_months_under_12(end_date):
   result = calculate_init_date_yf("5m", end_date)
   assert result == datetime.datetime(2025, 6, 2)

def test_calculate_months_over_12(end_date):
   result = calculate_init_date_yf("15m", end_date)
   assert result == datetime.datetime(2024, 8, 2)

def test_calculate_days_under_30(end_date):
   result = calculate_init_date_yf("10d", end_date)
   assert result == datetime.datetime(2025, 10, 23)

def test_calculate_days_over_30(end_date):
   result = calculate_init_date_yf("45d", end_date)
   assert result == datetime.datetime(2025, 9, 18)

def test_invalid_range(end_date):
   with pytest.raises(ValueError):
       calculate_init_date_yf("3w", end_date)

# Tests for calculate_init_date_ms
def test_years_with_leap():
    result = calculate_init_date_ms("2y", include_leap_years=True)
    assert result== 730.5

def test_years_without_leap():
    result = calculate_init_date_ms("2y", include_leap_years=False)
    assert result == 730

def test_months():
    result = calculate_init_date_ms("3m")
    assert result == int(3 * 30.44)  # 91.32 → 91

def test_days():
    result = calculate_init_date_ms("45d")
    assert result == 45

def test_large_months():
    result = calculate_init_date_ms("24m")
    assert result == int(24 * 30.44)

def test_zero_days():
    result = calculate_init_date_ms("0d")
    assert result == 0

def test_one_year_vs_months_equivalence():
    days_y = calculate_init_date_ms("1y", include_leap_years=False)
    days_m = calculate_init_date_ms("12m")
    assert abs(days_y - days_m) <= 5  # tolerancia por redondeo
