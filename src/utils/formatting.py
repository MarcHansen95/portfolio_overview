"""Formatting utilities for display values."""

from typing import Union
from src.config.constants import DECIMAL_PLACES_CURRENCY, DECIMAL_PLACES_PERCENT, DECIMAL_PLACES_WEIGHT


class Formatter:
    """Handles formatting of numerical values for display."""

    @staticmethod
    def format_currency(value: Union[int, float], currency: str = "DKK") -> str:
        """
        Format a value as currency.

        Args:
            value: Numerical value
            currency: Currency code (default: DKK)

        Returns:
            Formatted currency string
        """
        if value is None or (isinstance(value, float) and value != value):  # NaN check
            return "N/A"
        
        return f"{value:,.{DECIMAL_PLACES_CURRENCY}f} {currency}"

    @staticmethod
    def format_percentage(value: Union[int, float], include_sign: bool = True) -> str:
        """
        Format a value as percentage.

        Args:
            value: Percentage value (0-100)
            include_sign: Include + or - sign

        Returns:
            Formatted percentage string
        """
        if value is None or (isinstance(value, float) and value != value):  # NaN check
            return "N/A"
        
        sign = "+" if include_sign and value > 0 else ""
        return f"{sign}{value:.{DECIMAL_PLACES_PERCENT}f}%"

    @staticmethod
    def format_weight(value: Union[int, float]) -> str:
        """
        Format a value as weight percentage.

        Args:
            value: Weight value (0-100)

        Returns:
            Formatted weight string
        """
        if value is None or (isinstance(value, float) and value != value):  # NaN check
            return "N/A"
        
        return f"{value:.{DECIMAL_PLACES_WEIGHT}f}%"

    @staticmethod
    def format_number(value: Union[int, float], decimals: int = 2) -> str:
        """
        Format a number with specified decimal places.

        Args:
            value: Numerical value
            decimals: Number of decimal places

        Returns:
            Formatted number string
        """
        if value is None or (isinstance(value, float) and value != value):  # NaN check
            return "N/A"
        
        return f"{value:,.{decimals}f}"

    @staticmethod
    def get_return_color(value: Union[int, float]) -> str:
        """
        Get color based on return value using the custom theme.

        Args:
            value: Return value (positive or negative)

        Returns:
            Hex color code
        """
        if value is None or (isinstance(value, float) and value != value):  # NaN check
            return "#73766A"  # Olive green (neutral)
        
        if value > 0:
            return "#73766A"  # Olive green (positive/gain)
        elif value < 0:
            return "#9E6752"  # Rust brown (negative/loss)
        else:
            return "#73766A"  # Olive green (neutral)
