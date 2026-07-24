"""Table components for displaying portfolio data."""

import streamlit as st
import pandas as pd
from src.utils.formatting import Formatter
from src.config.constants import DISPLAY_LABELS


class Tables:
    """Renders tables for portfolio data display."""

    @staticmethod
    def format_dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
        """
        Format dataframe for Streamlit display.

        Args:
            df: Portfolio DataFrame

        Returns:
            Formatted DataFrame with display labels and formatted values
        """
        df = df.copy()

        # Rename columns to display labels
        display_cols = {}
        for col in df.columns:
            if col in DISPLAY_LABELS:
                display_cols[col] = DISPLAY_LABELS[col]

        df = df.rename(columns=display_cols)

        # Format numerical columns
        numerical_cols = {
            "Value (DKK)": "Value_DKK",
            "Price (DKK)": "Price",
            "Return (DKK)": "Return_DKK",
        }

        for display_name, orig_name in numerical_cols.items():
            if orig_name in df.columns:
                df[orig_name] = df[orig_name].apply(
                    lambda x: Formatter.format_currency(x) if pd.notna(x) else "N/A"
                )

        # Format percentage columns
        pct_cols = ["Return %", "Weight %"]
        for col in pct_cols:
            if col in df.columns:
                orig_name = next(
                    (k for k, v in DISPLAY_LABELS.items() if v == col), None
                )
                if orig_name and orig_name in df.columns:
                    df[col] = df[orig_name].apply(
                        lambda x: Formatter.format_percentage(x)
                        if pd.notna(x)
                        else "N/A"
                    )

        return df

    @staticmethod
    def render_holdings_table(df: pd.DataFrame) -> None:
        """
        Render interactive holdings table.

        Args:
            df: Portfolio DataFrame with holdings
        """
        if df.empty:
            st.warning("No holdings to display")
            return

        # Select relevant columns for display
        display_cols = [
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

        available_cols = [col for col in display_cols if col in df.columns]
        table_df = df[available_cols].copy()

        # Format for display
        table_df = Tables.format_dataframe_for_display(table_df)

        st.dataframe(
            table_df,
            width='stretch',
            hide_index=True,
            column_config={
                "Mapped_Security": st.column_config.TextColumn("Security"),
                "Type": st.column_config.TextColumn("Type"),
                "Sektor": st.column_config.TextColumn("Sector"),
                "Antal": st.column_config.NumberColumn("Quantity", format="%d"),
                "Price": st.column_config.TextColumn("Price (DKK)"),
                "Value_DKK": st.column_config.TextColumn("Value (DKK)"),
                "Return_DKK": st.column_config.TextColumn("Return (DKK)"),
                "Return_Percent": st.column_config.TextColumn("Return %"),
                "Weight": st.column_config.TextColumn("Weight %"),
                "Currency": st.column_config.TextColumn("Currency"),
            },
        )

    @staticmethod
    def render_holdings_editor(df: pd.DataFrame) -> pd.DataFrame:
        """
        Render a data editor for editable holding fields.

        Args:
            df: Portfolio DataFrame with holdings

        Returns:
            Edited DataFrame with the same row order as the input
        """
        if df.empty:
            st.warning("No holdings to display")
            return df.copy()

        editable_columns = [
            "Mapped_Security",
            "Type",
            "Sektor",
            "Antal",
            "Price",
            "Return_Percent",
            "Currency",
            "Region",
            "Platform",
            "Depot",
            "TICKER",
        ]

        available_columns = [col for col in editable_columns if col in df.columns]
        edit_df = df[available_columns].copy()

        return st.data_editor(
            edit_df,
            width='stretch',
            hide_index=True,
            column_config={
                "Mapped_Security": st.column_config.TextColumn("Security"),
                "Type": st.column_config.TextColumn("Type"),
                "Sektor": st.column_config.TextColumn("Sector"),
                "Antal": st.column_config.NumberColumn("Quantity", format="%d"),
                "Price": st.column_config.NumberColumn("Price (DKK)", format="%.2f"),
                "Return_Percent": st.column_config.NumberColumn(
                    "Return %", format="%.2f"
                ),
                "Currency": st.column_config.TextColumn("Currency"),
                "Region": st.column_config.TextColumn("Region"),
                "Platform": st.column_config.TextColumn("Platform"),
                "Depot": st.column_config.TextColumn("Depot"),
                "TICKER": st.column_config.TextColumn("Ticker"),
            },
        )

    @staticmethod
    def render_sector_breakdown_table(df: pd.DataFrame) -> None:
        """
        Render sector breakdown table.

        Args:
            df: Aggregated sector data
        """
        if df.empty:
            st.warning("No sector data to display")
            return

        # Reset index to make sector a column
        if df.index.name == "Sektor":
            df = df.reset_index()

        display_df = df.copy()
        display_df.columns = [DISPLAY_LABELS.get(col, col) for col in display_df.columns]

        st.dataframe(
            display_df,
            width='stretch',
            hide_index=True,
            column_config={
                "Value (DKK)": st.column_config.NumberColumn(
                    "Value (DKK)", format="%.2f"
                ),
                "Return (DKK)": st.column_config.NumberColumn(
                    "Return (DKK)", format="%.2f"
                ),
                "Return %": st.column_config.NumberColumn("Return %", format="%.2f"),
                "Weight %": st.column_config.NumberColumn("Weight %", format="%.2f"),
                "Num_Holdings": st.column_config.NumberColumn("Holdings", format="%d"),
            },
        )

    @staticmethod
    def render_top_performers_table(df: pd.DataFrame, title: str = "Top Performers") -> None:
        """
        Render table with top/worst performers.

        Args:
            df: DataFrame with performer data
            title: Table title
        """
        if df.empty:
            st.warning("No performer data to display")
            return

        display_df = df.copy()
        display_df.columns = [DISPLAY_LABELS.get(col, col) for col in display_df.columns]

        st.dataframe(
            display_df,
            width='stretch',
            hide_index=True,
            column_config={
                "Security": st.column_config.TextColumn("Security"),
                "Value (DKK)": st.column_config.NumberColumn(
                    "Value (DKK)", format="%.2f"
                ),
                "Return (DKK)": st.column_config.NumberColumn(
                    "Return (DKK)", format="%.2f"
                ),
                "Return %": st.column_config.NumberColumn("Return %", format="%.2f"),
                "Sector": st.column_config.TextColumn("Sector"),
            },
        )
