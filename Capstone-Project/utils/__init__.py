__version__ = "1.0.0"
__author__ = "Life-OS Developer"

from .data_loader import load_data, filter_by_date, get_daily_summary
from .helpers import format_minutes, severity_classification
from .ai_coach import get_coach_response