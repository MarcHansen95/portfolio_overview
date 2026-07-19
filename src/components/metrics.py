"""Metric card components."""

import streamlit as st
from typing import Union
from src.utils.formatting import Formatter


class MetricCards:
    """Legacy component - kept for backwards compatibility. Use KPICard instead."""

    @staticmethod
    def render_metric_card(
        label: str,
        value: Union[int, float],
        delta: Union[int, float] = None,
        delta_suffix: str = "",
        formatter_func=None,
    ) -> None:
        """
        Deprecated: Use KPICard.render_kpi_card() instead.
        
        Render a single metric card.

        Args:
            label: Card label
            value: Main value to display
            delta: Optional delta/change value
            delta_suffix: Suffix for delta display (e.g., "%", "DKK")
            formatter_func: Optional formatter function for value
        """
        if formatter_func:
            formatted_value = formatter_func(value)
        else:
            formatted_value = str(value)

        delta_str = None
        if delta is not None:
            delta_color = "inverse" if delta < 0 else "off"
            delta_str = f"{delta:+.2f} {delta_suffix}".strip()

        st.metric(
            label=label,
            value=formatted_value,
            delta=delta_str,
            delta_color=delta_color if delta is not None else "off",
        )

    @staticmethod
    def render_overview_metrics(totals: dict) -> None:
        """
        Deprecated: Use KPICard.render_portfolio_overview_cards() instead.
        
        Render overview metrics cards in columns.

        Args:
            totals: Dictionary with portfolio totals
        """
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            MetricCards.render_metric_card(
                "Total Portfolio Value",
                totals["total_value"],
                formatter_func=lambda x: Formatter.format_currency(x),
            )

        with col2:
            MetricCards.render_metric_card(
                "Total Return (DKK)",
                totals["total_return_dkk"],
                formatter_func=lambda x: Formatter.format_currency(x),
            )

        with col3:
            MetricCards.render_metric_card(
                "Return %",
                totals["total_return_percent"],
                formatter_func=lambda x: Formatter.format_percentage(x),
            )

        with col4:
            MetricCards.render_metric_card(
                "Number of Holdings",
                totals["num_holdings"],
                formatter_func=lambda x: f"{int(x)}",
            )
