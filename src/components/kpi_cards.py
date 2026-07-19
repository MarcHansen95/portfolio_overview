"""Custom KPI card components for portfolio metrics."""

import streamlit as st
from src.config.theme import COLOR_SCHEME


class KPICard:
    """Renders custom KPI cards for portfolio metrics."""

    @staticmethod
    def render_kpi_card(
        label: str,
        value: str,
        description: str = "",
        icon: str = "📊",
        color_accent: str = "#73766A",
    ) -> None:
        """
        Render a single KPI card with custom styling.

        Args:
            label: Card label (e.g., "Total Portfolio Value")
            value: Main metric value (e.g., "$1,250,000.00")
            description: Secondary text below value
            icon: Emoji icon to display
            color_accent: Accent color for the left border
        """
        description_html = f'<div style="font-size: 13px; color: #666; line-height: 1.5;">{description}</div>' if description else ''
        
        card_html = (
            f'<div style="background: white; border-radius: 12px; padding: 20px; margin-bottom: 10px; '
            f'border-left: 4px solid {color_accent}; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); '
            f'font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">'
            f'<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">'
            f'<div style="font-size: 13px; color: #666; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">'
            f'{label}'
            f'</div>'
            f'<div style="font-size: 20px;">{icon}</div>'
            f'</div>'
            f'<div style="font-size: 32px; font-weight: 700; color: #1a1a1a; margin-bottom: 8px; '
            f'font-family: \'Inter\', -apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif;">'
            f'{value}'
            f'</div>'
            f'{description_html}'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

    @staticmethod
    def render_kpi_row(metrics: list) -> None:
        """
        Render multiple KPI cards in a row.

        Args:
            metrics: List of dicts with keys: label, value, description, icon, color_accent
        """
        cols = st.columns(len(metrics))
        
        for col, metric in zip(cols, metrics):
            with col:
                KPICard.render_kpi_card(
                    label=metric.get("label", ""),
                    value=metric.get("value", "N/A"),
                    description=metric.get("description", ""),
                    icon=metric.get("icon", "📊"),
                    color_accent=metric.get("color_accent", COLOR_SCHEME["secondary"]),
                )

    @staticmethod
    def render_portfolio_overview_cards(totals: dict, type_allocation: dict = None) -> None:
        """
        Render the portfolio overview KPI cards.

        Args:
            totals: Dictionary with portfolio metrics
            type_allocation: Dictionary with asset type allocation data
        """
        total_value = totals.get("total_value", 0)
        total_return_dkk = totals.get("total_return_dkk", 0)
        total_return_percent = totals.get("total_return_percent", 0)
        num_holdings = totals.get("num_holdings", 0)

        # Format values
        from src.utils.formatting import Formatter
        
        value_formatted = Formatter.format_currency(total_value)
        return_formatted = Formatter.format_currency(total_return_dkk)
        return_pct_formatted = Formatter.format_percentage(total_return_percent)

        # Determine color based on returns
        return_color = COLOR_SCHEME["secondary"] if total_return_dkk > 0 else COLOR_SCHEME["tertiary"]

        # Determine top asset type
        top_type = "N/A"
        top_type_value = 0
        top_type_pct = 0
        type_distribution = ""
        if type_allocation:
            type_allocation_sorted = sorted(
                type_allocation.items(),
                key=lambda x: x[1],
                reverse=True
            )
            if type_allocation_sorted:
                top_type = type_allocation_sorted[0][0]
                top_type_value = type_allocation_sorted[0][1]
                top_type_pct = (top_type_value / total_value * 100) if total_value > 0 else 0
                
                # Create distribution string for top 3 types
                distribution_parts = []
                for asset_type, value in type_allocation_sorted[:3]:
                    pct = (value / total_value * 100) if total_value > 0 else 0
                    distribution_parts.append(f"{asset_type}: {pct:.0f}%")
                type_distribution = " | ".join(distribution_parts)

        metrics = [
            {
                "label": "Total Portfolio Value",
                "value": value_formatted,
                "description": f"Total invested: {num_holdings} holdings",
                "icon": "💼",
                "color_accent": COLOR_SCHEME["primary"],
            },

            {
                "label": "Asset Type Distribution",
                "value": type_distribution if type_distribution else "N/A",
                "description": f"Top: {top_type} ({top_type_pct:.1f}%)",
                "icon": "📑",
                "color_accent": COLOR_SCHEME["tertiary"],
            },
            {
                "label": "Return Percentage",
                "value": return_pct_formatted,
                "description": f"Total return: {Formatter.format_currency(total_return_dkk)}",
                "icon": "📊",
                "color_accent": return_color,
            },
        ]

        KPICard.render_kpi_row(metrics)
