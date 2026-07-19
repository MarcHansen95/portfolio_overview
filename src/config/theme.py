"""Theme and styling configuration for the app."""

# Color scheme based on custom palette
COLOR_SCHEME = {
    "primary": "#2D4354",       # Dark blue
    "secondary": "#73766A",     # Olive green
    "accent": "#FED7A5",        # Peachy cream
    "tertiary": "#9E6752",      # Rust brown
    "quaternary": "#534145",    # Mauve
    "dark": "#20212B",          # Very dark
    "light": "#FED7A5",         # Light accent
}

# Sector colors palette for pie charts (using the custom color scheme)
SECTOR_COLORS = [
    "#2D4354",  # Dark blue
    "#73766A",  # Olive green
    "#9E6752",  # Rust brown
    "#534145",  # Mauve
    "#20212B",  # Very dark
    "#FED7A5",  # Peachy cream
    "#6B5B4A",  # Muted brown (blend)
    "#4A5A6A",  # Muted blue (blend)
    "#5A6B5A",  # Muted green (blend)
    "#6B534A",  # Muted rust (blend)
]

# Type colors for pie charts using the custom palette
TYPE_COLORS = {
    "Stock": "#2D4354",      # Dark blue
    "Bond": "#73766A",       # Olive green
    "ETF": "#9E6752",        # Rust brown
    "Fund": "#534145",       # Mauve
    "Cash": "#FED7A5",       # Peachy cream
}

# Metric card styling
METRIC_CARD_HEIGHT = 120

# Chart configuration
CHART_HEIGHT = 400
CHART_MARGIN = dict(l=0, r=0, t=30, b=0)

# Font sizes
FONT_SIZE_TITLE = 24
FONT_SIZE_SUBTITLE = 18
FONT_SIZE_LABEL = 14
FONT_SIZE_SMALL = 12

# Table styling
TABLE_ROW_HEIGHT = 35
TABLE_HEADER_HEIGHT = 40

# Positive/Negative colors for returns
COLOR_POSITIVE = "#73766A"  # Olive green for gains
COLOR_NEGATIVE = "#9E6752"  # Rust brown for losses
COLOR_NEUTRAL = "#73766A"   # Olive green for neutral
