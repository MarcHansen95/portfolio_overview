"""Chart components for data visualization."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from src.config.theme import (
    SECTOR_COLORS,
    TYPE_COLORS,
    CHART_HEIGHT,
    COLOR_SCHEME,
)


class Charts:
    """Renders interactive charts for portfolio analysis."""

    @staticmethod
    def render_sector_pie_chart(df: pd.DataFrame) -> None:
        """
        Render pie chart showing portfolio allocation by sector.

        Args:
            df: Filtered portfolio DataFrame
        """
        if df.empty:
            st.warning("No data available for sector distribution")
            return

        sector_data = df.groupby("Sektor")["Value_DKK"].sum().reset_index()
        sector_data = sector_data.sort_values("Value_DKK", ascending=False)

        fig = px.pie(
            sector_data,
            values="Value_DKK",
            names="Sektor",
            title="Portfolio Allocation by Sector",
            color_discrete_sequence=SECTOR_COLORS,
            hole=0.3,
        )
        
        # Calculate percentages for hover
        total_value = sector_data["Value_DKK"].sum()
        sector_data["Percentage"] = (sector_data["Value_DKK"] / total_value * 100).round(2)
        
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                         "Value: DKK %{value:,.0f}<br>" +
                         "Allocation: %{customdata:.2f}%<extra></extra>",
            customdata=sector_data["Percentage"],
        )
        
        fig.update_layout(height=CHART_HEIGHT)
        st.plotly_chart(fig, key="sector_pie", width='stretch')

    @staticmethod
    def render_type_pie_chart(df: pd.DataFrame) -> None:
        """
        Render pie chart showing portfolio allocation by security type.

        Args:
            df: Filtered portfolio DataFrame
        """
        if df.empty:
            st.warning("No data available for type distribution")
            return

        type_data = df.groupby("Type")["Value_DKK"].sum().reset_index()
        type_data = type_data.sort_values("Value_DKK", ascending=False)

        fig = px.pie(
            type_data,
            values="Value_DKK",
            names="Type",
            title="Portfolio Allocation by Type",
            color_discrete_map=TYPE_COLORS,
            hole=0.3,
        )
        
        # Calculate percentages for hover
        total_value = type_data["Value_DKK"].sum()
        type_data["Percentage"] = (type_data["Value_DKK"] / total_value * 100).round(2)
        
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                         "Value: DKK %{value:,.0f}<br>" +
                         "Allocation: %{customdata:.2f}%<extra></extra>",
            customdata=type_data["Percentage"],
        )
        
        fig.update_layout(height=CHART_HEIGHT)
        st.plotly_chart(fig, key="type_pie", width='stretch')

    @staticmethod
    def render_top_holdings_bar_chart(df: pd.DataFrame, n: int | None = None) -> None:
        """
        Render a bar chart showing each holding's allocation share of the portfolio.

        Args:
            df: Filtered portfolio DataFrame
            n: Number of top holdings to display
        """
        if df.empty:
            st.warning("No data available for top holdings")
            return

        total_value = pd.to_numeric(df["Value_DKK"], errors="coerce").sum()
        if total_value == 0:
            st.info("No portfolio value to calculate allocation")
            return

        top_holdings = (
            df.groupby("Mapped_Security", as_index=False)
            .agg(Value_DKK=("Value_DKK", "sum"))
        )
        top_holdings["Display_Name"] = top_holdings["Mapped_Security"]

        top_holdings["Allocation_Percent"] = (
            top_holdings["Value_DKK"] / total_value * 100
        ).round(1)
        top_holdings = top_holdings.sort_values("Allocation_Percent", ascending=False)
        if n is not None:
            top_holdings = top_holdings.head(n)
        top_holdings = top_holdings.reset_index(drop=True)

        fig = px.bar(
            top_holdings,
            x="Display_Name",
            y="Allocation_Percent",
            title="Portfolio Allocation by Holding",
            labels={"Display_Name": "Holding", "Allocation_Percent": "Allocation %"},
            color="Allocation_Percent",
            color_continuous_scale="Blues",
            text=top_holdings["Allocation_Percent"].astype(str) + "%",
        )

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Allocation: %{y:.0f}%<br>" +
                         "Value: DKK %{customdata:,.0f}<extra></extra>",
            customdata=top_holdings["Value_DKK"],
            textposition="outside",
        )

        fig.update_layout(
            height=max(300, min(900, 28 * len(top_holdings) + 100)),
            showlegend=False,
            xaxis_title="Holding",
            yaxis_title="Allocation %",
            margin=dict(l=20, r=20, t=60, b=20),
            xaxis=dict(
                automargin=True,
                tickangle=-45,
            ),
        )
        fig.update_xaxes(categoryarray=top_holdings["Display_Name"].tolist(), categoryorder="array")
        st.plotly_chart(
            fig,
            key="top_holdings",
            width='stretch',
        )

    @staticmethod
    def render_sector_performance_chart(df: pd.DataFrame, key_suffix: str = "") -> None:
        """
        Render bar chart showing sector performance by return percentage.

        Args:
            df: Filtered portfolio DataFrame
            key_suffix: Suffix for unique key identification
        """
        if df.empty:
            st.warning("No data available for sector performance")
            return

        sector_perf = (
            df.groupby("Sektor")
            .agg({
                "Return_Percent": "mean",
                "Value_DKK": "sum",
            })
            .reset_index()
            .sort_values("Return_Percent", ascending=False)
        )

        colors = [
            COLOR_SCHEME["secondary"] if x > 0 else COLOR_SCHEME["tertiary"]
            for x in sector_perf["Return_Percent"]
        ]

        fig = px.bar(
            sector_perf,
            x="Sektor",
            y="Return_Percent",
            title="Average Return % by Sector",
            labels={"Return_Percent": "Avg Return %", "Sektor": "Sector"},
            color="Return_Percent",
            color_continuous_scale=["#9E6752", "#73766A", "#73766A"],
        )
        
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Avg Return: %{y:.2f}%<br>" +
                         "Total Value: DKK %{customdata:,.0f}<extra></extra>",
            customdata=sector_perf["Value_DKK"],
        )
        
        fig.update_layout(height=CHART_HEIGHT, showlegend=False)
        key = f"sector_performance{key_suffix}"
        st.plotly_chart(fig, key=key, width='stretch')

    @staticmethod
    def render_return_distribution_chart(df: pd.DataFrame) -> None:
        """
        Render scatter chart showing return vs value distribution.

        Args:
            df: Filtered portfolio DataFrame
        """
        if df.empty:
            st.warning("No data available for return distribution")
            return

        fig = px.scatter(
            df,
            x="Value_DKK",
            y="Return_Percent",
            size="Weight",
            color="Sektor",
            hover_name="Mapped_Security",
            title="Return % vs Portfolio Value",
            labels={"Value_DKK": "Value (DKK)", "Return_Percent": "Return %"},
            color_discrete_sequence=SECTOR_COLORS,
        )
        
        fig.update_traces(
            hovertemplate="<b>%{hovertext}</b><br>" +
                         "Portfolio Value: DKK %{x:,.0f}<br>" +
                         "Return: %{y:.2f}%<br>" +
                         "Weight: %{customdata:.2f}%<extra></extra>",
            customdata=df["Weight"],
        )
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig.update_layout(height=CHART_HEIGHT)
        st.plotly_chart(fig, key="return_distribution", width='stretch')

    @staticmethod
    def render_currency_exposure_chart(df: pd.DataFrame) -> None:
        """
        Render pie chart showing currency exposure.

        Args:
            df: Filtered portfolio DataFrame
        """
        if df.empty:
            st.warning("No data available for currency exposure")
            return

        currency_data = df.groupby("Currency")["Value_DKK"].sum().reset_index()
        currency_data = currency_data.sort_values("Value_DKK", ascending=False)

        fig = px.pie(
            currency_data,
            values="Value_DKK",
            names="Currency",
            title="Portfolio Exposure by Currency",
            color_discrete_sequence=SECTOR_COLORS,
        )
        
        # Calculate percentages for hover
        total_value = currency_data["Value_DKK"].sum()
        currency_data["Percentage"] = (currency_data["Value_DKK"] / total_value * 100).round(2)
        
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                         "Exposure: DKK %{value:,.0f}<br>" +
                         "% of Portfolio: %{customdata:.2f}%<extra></extra>",
            customdata=currency_data["Percentage"],
        )
        
        fig.update_layout(height=CHART_HEIGHT)
        st.plotly_chart(fig, key="currency_exposure", width='stretch')

    @staticmethod
    @st.cache_data(ttl=3600)
    def _fetch_price_data(tickers: list, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch price data for multiple tickers.

        Args:
            tickers: List of ticker symbols
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)

        Returns:
            DataFrame with price data or empty DataFrame if fetch fails
        """
        if not tickers:
            return pd.DataFrame()
        
        try:
            price_data = yf.download(
                tickers,
                start=start_date,
                end=end_date,
                interval="1d",
                auto_adjust=True,
                group_by="ticker",
                progress=False,
            )
            return price_data
        except Exception as e:
            st.warning(f"⚠️ Could not fetch price data: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def render_portfolio_performance_chart(df: pd.DataFrame, key_suffix: str = "") -> None:
        """
        Render interactive performance chart for all portfolio holdings.

        Args:
            df: Portfolio DataFrame with 'yahoo_tickers' and 'Mapped_Security' columns
            key_suffix: Suffix for unique chart key
        """
        if df.empty:
            st.warning("No data available for performance chart")
            return

        # Layout with controls
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            period_options = {
                "1 Month": 30,
                "3 Months": 90,
                "6 Months": 182,
                "1 Year": 365,
                "3 Years": 365 * 3,
                "5 Years": 365 * 5,
                "10 Years": 365 * 10,
            }
            selected_period_label = st.selectbox(
                "Time Period",
                options=list(period_options.keys()),
                key=f"perf_period{key_suffix}",
            )
            days = period_options[selected_period_label]

        with col2:
            display_type = st.selectbox(
                "Display Type",
                options=["Relative %", "Absolute Price"],
                key=f"perf_type{key_suffix}",
            )

        with col3:
            show_all = st.checkbox("All Visible", value=False, key=f"perf_visible{key_suffix}")

        # Calculate date range
        end_date = datetime.today().strftime("%Y-%m-%d")
        start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")

        # Get unique tickers and security names
        ticker_mapping = df[["yahoo_tickers", "Mapped_Security"]].drop_duplicates()
        valid_tickers = ticker_mapping[ticker_mapping["yahoo_tickers"].notna()]["yahoo_tickers"].tolist()

        if not valid_tickers:
            st.warning("No valid tickers found in portfolio")
            return

        # Fetch price data
        with st.spinner(f"📈 Fetching data for {len(valid_tickers)} tickers..."):
            price_data = Charts._fetch_price_data(valid_tickers, start_date, end_date)

        if price_data.empty:
            st.error("Could not fetch price data. Please try again.")
            return

        # Create figure
        fig = go.Figure()

        # Create color palette (cycle through custom colors)
        color_palette = [
            COLOR_SCHEME["primary"],
            COLOR_SCHEME["secondary"],
            COLOR_SCHEME["tertiary"],
            "#FED7A5",
            "#9E6752",
            "#534145",
        ]

        trace_count = 0

        # Add traces for each ticker
        for idx, row in ticker_mapping.iterrows():
            ticker = row["yahoo_tickers"]
            security_name = row["Mapped_Security"]

            if ticker not in price_data.columns and ticker not in price_data.index:
                continue

            try:
                # Extract closing prices
                if isinstance(price_data.columns, pd.MultiIndex):
                    closing_prices = price_data[(ticker, "Close")].dropna()
                else:
                    closing_prices = price_data["Close"].dropna()

                if closing_prices.empty:
                    continue

                # Calculate values to display
                if display_type == "Relative %":
                    first_price = closing_prices.iloc[0]
                    y_values = ((closing_prices - first_price) / first_price) * 100
                    y_title = "Relative Change (%)"
                    hovertemplate = (
                        f"<b>{security_name}</b><br>"
                        f"Date: %{{x|%Y-%m-%d}}<br>"
                        f"Relative Change: %{{y:.2f}}%<br>"
                        f"Initial Price: {first_price:.2f}<extra></extra>"
                    )
                else:
                    y_values = closing_prices
                    y_title = "Price (Currency)"
                    hovertemplate = (
                        f"<b>{security_name}</b><br>"
                        f"Date: %{{x|%Y-%m-%d}}<br>"
                        f"Price: %{{y:.2f}}<extra></extra>"
                    )

                # Choose color
                color = color_palette[trace_count % len(color_palette)]
                is_visible = True if show_all else "legendonly"

                # Add trace
                fig.add_trace(
                    go.Scatter(
                        x=closing_prices.index,
                        y=y_values,
                        mode="lines",
                        name=security_name,
                        visible=is_visible,
                        line=dict(color=color, width=2),
                        hovertemplate=hovertemplate,
                    )
                )

                # Add end value label
                last_date = closing_prices.index[-1]
                last_value = y_values.iloc[-1]
                
                if display_type == "Relative %":
                    label_text = f"{last_value:.1f}%"
                else:
                    label_text = f"{last_value:.2f}"
                
                fig.add_annotation(
                    x=last_date,
                    y=last_value,
                    text=label_text,
                    showarrow=False,
                    xanchor="left",
                    xshift=5,
                    font=dict(size=10, color=color),
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor=color,
                    borderwidth=1,
                    borderpad=2,
                )

                trace_count += 1

            except Exception as e:
                st.warning(f"⚠️ Could not process {security_name} ({ticker}): {str(e)}")
                continue

        if trace_count == 0:
            st.error("Could not process any ticker data")
            return

        # Add zero line for relative change
        if display_type == "Relative %":
            fig.add_hline(y=0, line_dash="dash", line_color="rgba(100, 100, 100, 0.5)", name="Baseline")

        # Update layout
        fig.update_layout(
            title=f"Portfolio Performance ({selected_period_label})",
            xaxis_title="Date",
            yaxis_title=y_title,
            height=600,
            hovermode="x unified",
            template="plotly_white",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor="rgba(0, 0, 0, 0.2)",
                borderwidth=1,
            ),
            plot_bgcolor="rgba(240, 240, 240, 0.5)",
            margin=dict(l=60, r=60, t=80, b=60),
        )

        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(200, 200, 200, 0.3)",
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(200, 200, 200, 0.3)",
        )

        if display_type == "Relative %":
            fig.update_yaxes(ticksuffix="%")

        st.plotly_chart(fig, key=f"portfolio_performance{key_suffix}", width='stretch')
