"""Constants and configuration values for the portfolio overview app."""

# File paths
DATA_FILE = "portfolio_data.xlsx"

# Column names (keep original names as they appear in the data)
COLUMNS = {
    "MIDLER": "Midler",
    "PLATFORM": "Platform",
    "DEPOT": "Depot",
    "SECURITY": "Security",
    "MAPPED_SECURITY": "Mapped_Security",
    "SECTOR": "Sektor",
    "TYPE": "Type",
    "TICKER": "TICKER",
    "YAHOO_TICKER": "yahoo_tickers",
    "QUANTITY": "Antal",
    "GAK": "GAK",
    "CURRENCY": "Currency",
    "PRICE": "Price",
    "VALUE_DKK": "Value_DKK",
    "RETURN_DKK": "Return_DKK",
    "RETURN_PERCENT": "Return_Percent",
    "WEIGHT": "Weight",
    "EXCHANGE_RATE_DKK": "exchange_rate_dkk",
    "REGION": "Region",
}

# Display labels (friendly names for UI)
DISPLAY_LABELS = {
    "Midler": "Fund",
    "Platform": "Platform",
    "Depot": "Depot",
    "Security": "Security Name",
    "Mapped_Security": "Security",
    "Sektor": "Sector",
    "Type": "Type",
    "TICKER": "Ticker",
    "yahoo_tickers": "Yahoo Ticker",
    "Antal": "Quantity",
    "GAK": "GAK",
    "Currency": "Currency",
    "Price": "Price (DKK)",
    "Value_DKK": "Value (DKK)",
    "Return_DKK": "Return (DKK)",
    "Return_Percent": "Return %",
    "Weight": "Weight %",
    "exchange_rate_dkk": "Exchange Rate",
    "Region": "Region",
}

# App configuration
APP_TITLE = "Portfolio Overview"
APP_ICON = "📊"

# Page config
PAGE_LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Metrics to display in the overview
OVERVIEW_METRICS = [
    "Total Portfolio Value",
    "Total Return",
    "Return Percentage",
    "Number of Holdings",
]

# Display table columns for holdings detail
HOLDINGS_TABLE_COLUMNS = [
    "Mapped_Security",
    "Type",
    "Sektor",
    "Antal",
    "Price",
    "Value_DKK",
    "Return_DKK",
    "Return_Percent",
    "Weight",
    "Currency",
]

# Default sorting column and order
DEFAULT_SORT_COLUMN = "Value_DKK"
DEFAULT_SORT_ORDER = "descending"

# Number formatting
DECIMAL_PLACES_PERCENT = 2
DECIMAL_PLACES_CURRENCY = 2
DECIMAL_PLACES_WEIGHT = 2

# Colors and styling (imported from theme.py)
# These are defined in theme.py for consistency
COLOR_POSITIVE = "#73766A"  # Olive green for gains
COLOR_NEGATIVE = "#9E6752"  # Rust brown for losses
COLOR_NEUTRAL = "#73766A"   # Olive green for neutral
