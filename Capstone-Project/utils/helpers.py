"""
Utility helper functions for formatting, classification, and data processing.
"""

from typing import Tuple, Optional


def format_minutes(minutes: int) -> str:
    """
    Format minutes into a human-readable string.
    
    Args:
        minutes: Number of minutes
        
    Returns:
        Formatted string like "2h 15m" or "45m"
    """
    if minutes < 0:
        return "0m"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if hours > 0 and remaining_minutes > 0:
        return f"{hours}h {remaining_minutes}m"
    elif hours > 0:
        return f"{hours}h"
    else:
        return f"{remaining_minutes}m"


def severity_classification(total_minutes: int, daily_goal: int) -> str:
    """
    Classify screen-time severity based on comparison to goal.
    
    Args:
        total_minutes: Total screen time in minutes
        daily_goal: Daily goal in minutes
        
    Returns:
        Severity level: "low", "moderate", or "high"
    """
    percentage = (total_minutes / daily_goal) * 100 if daily_goal > 0 else 0
    
    if percentage <= 80:
        return "low"
    elif percentage <= 120:
        return "moderate"
    else:
        return "high"


def goal_comparison_text(total_minutes: int, daily_goal: int) -> str:
    """
    Generate comparison text between actual and goal.
    
    Args:
        total_minutes: Total screen time in minutes
        daily_goal: Daily goal in minutes
        
    Returns:
        Comparison string like "+25m over" or "-10m under"
    """
    difference = total_minutes - daily_goal
    
    if difference > 0:
        return f"+{difference}m over"
    elif difference < 0:
        return f"{difference}m under"
    else:
        return "On goal"


def get_severity_style(severity: str) -> Tuple[str, str]:
    """
    Get styling parameters based on severity level.
    
    Args:
        severity: Severity level ("low", "moderate", "high")
        
    Returns:
        Tuple of (color, icon)
    """
    styles = {
        "low": ("#27ae60", "✅"),
        "moderate": ("#f39c12", "⚠️"),
        "high": ("#e74c3c", "🔴"),
    }
    return styles.get(severity, ("#95a5a6", "❓"))


def calculate_weekly_average(df, date_column="Date", value_column="Minutes_Used") -> Optional[float]:
    """
    Calculate weekly average screen time.
    
    Args:
        df: DataFrame with screen-time data
        date_column: Name of date column
        value_column: Name of value column
        
    Returns:
        Average daily minutes for the week
    """
    daily_totals = df.groupby(date_column)[value_column].sum()
    
    if len(daily_totals) == 0:
        return None
    
    # Get last 7 days
    last_7_days = daily_totals.tail(7)
    
    return last_7_days.mean()


def categorize_usage_pattern(category_data: dict) -> str:
    """
    Categorize usage pattern based on category distribution.
    
    Args:
        category_data: Dictionary of category: minutes
        
    Returns:
        Usage pattern description
    """
    total = sum(category_data.values())
    
    if total == 0:
        return "No data"
    
    entertainment_social = category_data.get("Social Media", 0) + category_data.get("Entertainment", 0)
    productive = category_data.get("Coding", 0) + category_data.get("Education", 0) + category_data.get("Productivity", 0)
    
    ent_social_pct = (entertainment_social / total) * 100
    productive_pct = (productive / total) * 100
    
    if ent_social_pct > 60:
        return "Heavy entertainment/social media day"
    elif productive_pct > 60:
        return "Highly productive day"
    elif ent_social_pct > 40:
        return "Mixed day with entertainment bias"
    elif productive_pct > 40:
        return "Mixed day with productivity bias"
    else:
        return "Balanced day"