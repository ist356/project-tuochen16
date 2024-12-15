import pandas as pd

# Functions for processing
def calculate_discount_in_dollars(sales: float, discount: float) -> float:
    """Calculate total discount in dollars."""
    return sales * discount

def calculate_profit_margin(sales: float, profit: float) -> float:
    """Calculate profit margin as a percentage."""
    return (profit / sales) * 100 if sales != 0 else 0

def add_month_and_year_columns(data: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """Add 'month' and 'year' columns based on a date column."""
    data['month'] = pd.to_datetime(data[date_column]).dt.month
    data['year'] = pd.to_datetime(data[date_column]).dt.year
    return data

# Test Functions
def test_calculate_discount_in_dollars():
    assert calculate_discount_in_dollars(100, 0.1) == 10.0
    assert calculate_discount_in_dollars(250, 0.2) == 50.0
    assert calculate_discount_in_dollars(0, 0.5) == 0.0

def test_calculate_profit_margin():
    assert calculate_profit_margin(100, 25) == 25.0
    assert calculate_profit_margin(200, 50) == 25.0
    assert calculate_profit_margin(0, 50) == 0.0

def test_add_month_and_year_columns():
    data = pd.DataFrame({"Order Date": ["2020-03-06", "2019-12-15"]})
    result = add_month_and_year_columns(data, "Order Date")
    assert result.loc[0, 'month'] == 3
    assert result.loc[0, 'year'] == 2020
    assert result.loc[1, 'month'] == 12
    assert result.loc[1, 'year'] == 2019