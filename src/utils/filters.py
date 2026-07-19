"""Filter management utilities."""

import streamlit as st
from typing import Dict, List, Any
from src.data.processor import DataProcessor


class FilterManager:
    """Manages filter state and operations."""

    @staticmethod
    def initialize_filters(df) -> None:
        """
        Initialize filter state in session state.

        Args:
            df: Portfolio DataFrame
        """
        if "filters" not in st.session_state:
            st.session_state.filters = {
                "security_types": [],
                "sectors": [],
                "platforms": [],
                "regions": [],
                "currencies": [],
                "search_term": "",
            }

    @staticmethod
    def get_filter_options(df) -> Dict[str, List[str]]:
        """
        Get available filter options from data.

        Args:
            df: Portfolio DataFrame

        Returns:
            Dictionary of filter options
        """
        return {
            "security_types": DataProcessor.get_unique_values(df, "Type"),
            "sectors": DataProcessor.get_unique_values(df, "Sektor"),
            "platforms": DataProcessor.get_unique_values(df, "Platform"),
            "regions": DataProcessor.get_unique_values(df, "Region"),
            "currencies": DataProcessor.get_unique_values(df, "Currency"),
        }

    @staticmethod
    def reset_filters() -> None:
        """Reset all filters to default state."""
        st.session_state.filters = {
            "security_types": [],
            "sectors": [],
            "platforms": [],
            "regions": [],
            "currencies": [],
            "search_term": "",
        }

    @staticmethod
    def apply_filters(df) -> Any:
        """
        Apply current filters to dataframe.

        Args:
            df: Portfolio DataFrame

        Returns:
            Filtered DataFrame
        """
        filters = st.session_state.filters
        
        return DataProcessor.filter_data(
            df,
            security_types=filters["security_types"] if filters["security_types"] else None,
            sectors=filters["sectors"] if filters["sectors"] else None,
            platforms=filters["platforms"] if filters["platforms"] else None,
            regions=filters["regions"] if filters["regions"] else None,
            currencies=filters["currencies"] if filters["currencies"] else None,
            search_term=filters["search_term"] if filters["search_term"] else None,
        )

    @staticmethod
    def are_filters_active() -> bool:
        """
        Check if any filters are currently active.

        Returns:
            True if any filter is applied
        """
        filters = st.session_state.filters
        
        return any([
            filters.get("security_types"),
            filters.get("sectors"),
            filters.get("platforms"),
            filters.get("markets"),
            filters.get("regions"),
            filters.get("currencies"),
            filters.get("search_term"),
        ])
