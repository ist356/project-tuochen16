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
