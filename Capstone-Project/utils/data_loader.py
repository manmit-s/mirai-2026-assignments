"""
Data loading and processing utilities for screen-time analysis.
"""

import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime


REQUIRED_COLUMNS = ["Date", "App_Name", "Category", "Minutes_Used"]


def load_data(filepath: str) -> Optional[pd.DataFrame]:
    """
    Load screen-time data from CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with screen-time data or None if loading fails
    """
    try:
        df = pd.read_csv(filepath)

        # Some exported files wrap each complete CSV row in quotes. Pandas then
        # reads the file as a single comma-delimited column, so normalize it.
        if len(df.columns) == 1 and "," in df.columns[0]:
            df = df.iloc[:, 0].str.split(",", expand=True)
            df.columns = REQUIRED_COLUMNS

        missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")
        
        # Parse dates
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        df["Minutes_Used"] = pd.to_numeric(df["Minutes_Used"], errors="coerce")
        df = df.dropna(subset=["Date", "App_Name", "Category", "Minutes_Used"])
        df["Minutes_Used"] = df["Minutes_Used"].astype(int)
        
        # Sort by date
        df = df.sort_values("Date")
        
        return df
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def filter_by_date(df: pd.DataFrame, date: Any) -> pd.DataFrame:
    """
    Filter DataFrame for a specific date.
    
    Args:
        df: Input DataFrame
        date: Date to filter for (string or date object)
        
    Returns:
        Filtered DataFrame
    """
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()
    
    return df[df["Date"] == date]


def get_daily_summary(df: pd.DataFrame, date: Any) -> Dict[str, Any]:
    """
    Generate a summary dictionary for a specific date.
    
    Args:
        df: Input DataFrame
        date: Date to summarize
        
    Returns:
        Dictionary with daily summary metrics
    """
    daily_data = filter_by_date(df, date)
    
    if daily_data.empty:
        return {}
    
    summary = {
        "date": str(date),
        "total_minutes": daily_data["Minutes_Used"].sum(),
        "app_count": daily_data["App_Name"].nunique(),
        "category_count": daily_data["Category"].nunique(),
        "most_used_app": daily_data.groupby("App_Name")["Minutes_Used"].sum().idxmax(),
        "most_used_app_minutes": daily_data.groupby("App_Name")["Minutes_Used"].sum().max(),
        "top_category": daily_data.groupby("Category")["Minutes_Used"].sum().idxmax(),
        "top_category_minutes": daily_data.groupby("Category")["Minutes_Used"].sum().max(),
        "categories": daily_data.groupby("Category")["Minutes_Used"].sum().to_dict(),
        "apps": daily_data.groupby(["Category", "App_Name"])["Minutes_Used"].sum().to_dict(),
    }
    
    return summary


def get_trend_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate daily trend data for visualization.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with daily totals
    """
    trend = df.groupby("Date")["Minutes_Used"].sum().reset_index()
    trend.columns = ["Date", "Total_Minutes"]
    return trend.sort_values("Date")


def get_category_summary(df: pd.DataFrame, date: Optional[Any] = None) -> pd.DataFrame:
    """
    Generate category-wise summary for a specific date or all data.
    
    Args:
        df: Input DataFrame
        date: Optional date to filter
        
    Returns:
        DataFrame with category summaries
    """
    if date:
        data = filter_by_date(df, date)
    else:
        data = df
    
    summary = data.groupby("Category")["Minutes_Used"].sum().reset_index()
    summary.columns = ["Category", "Minutes"]
    return summary.sort_values("Minutes", ascending=False)


def get_app_summary(df: pd.DataFrame, date: Optional[Any] = None) -> pd.DataFrame:
    if date:
        data = filter_by_date(df, date)
    else:
        data = df
    
    summary = data.groupby(["Category", "App_Name"])["Minutes_Used"].sum().reset_index()
    summary.columns = ["Category", "App_Name", "Minutes"]
    return summary.sort_values("Minutes", ascending=False)
