"""Data processing and calculations module."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class DataProcessor:
    """Handles data processing and calculations."""

    @staticmethod
    def calculate_totals(df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate portfolio totals.

        Args:
            df: Portfolio DataFrame

        Returns:
            Dict with portfolio metrics
        """
        return {
            "total_value": df["Value_DKK"].sum(),
            "total_return_dkk": df["Return_DKK"].sum(),
            "total_return_percent": (
                (df["Return_DKK"].sum() / (df["Value_DKK"].sum() - df["Return_DKK"].sum())) * 100
                if (df["Value_DKK"].sum() - df["Return_DKK"].sum()) != 0
                else 0
            ),
            "num_holdings": len(df),
        }

    @staticmethod
    def calculate_weights(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate portfolio weight for each holding.

        Args:
            df: Portfolio DataFrame

        Returns:
            DataFrame with calculated weights
        """
        df = df.copy()
        total_value = df["Value_DKK"].sum()
        
        if total_value == 0:
            df["Weight"] = 0
        else:
            df["Weight"] = (df["Value_DKK"] / total_value) * 100
        
        return df

    @staticmethod
    def infer_sector_from_name(security_name: str) -> Optional[str]:
        """
        Infer sector/category from security name using keyword matching.

        Args:
            security_name: Security name or description string

        Returns:
            Inferred sector name or None if no match found
        """
        if pd.isna(security_name) or not isinstance(security_name, str):
            return None

        name_lower = security_name.lower()

        # Sector keywords mapping
        sector_keywords = {
            "Technology": [
                "technology", "tech", "technolog", "information", "digital security",
                "info technolog", "software", "semiconductor", "it ", "cyber",
            ],
            "Healthcare": [
                "healthcare", "health ", "pharma", "medical", "biotech", "bio-", "therapeut",
            ],
            "Financials": [
                "finance", "financial", "bank", "insurance", "investment", "fund",
                "capital", "trading", "payment",
            ],
            "Consumer Cyclical": [
                "consumer", "retail", "automotive", "auto ", "travel", "hospitality",
                "leisure", "restaurant", "apparel", "clothing",
            ],
            "Consumer Defensive": [
                "consumer defensive", "consumer staple", "staple", "food", "beverage",
                "grocery", "household", "personal care",
            ],
            "Energy": [
                "energy", "oil", "gas", "petroleum", "coal", "power", "utility",
                "renewable",
            ],
            "Industrials": [
                "industrial", "manufacturing", "construction", "machinery", "equipment",
                "aerospace", "defense", "transportation",
            ],
            "Materials": [
                "material", "mining", "metal", "chemicals", "chemical", "basic material",
                "steel", "copper", "rare earth",
            ],
            "Real Estate": [
                "real estate", "reit", "property", "realty", "residential",
            ],
            "Communication Services": [
                "communication", "telecom", "media", "entertainment", "broadcast",
                "internet", "social", "gaming",
            ],
            "Utilities": [
                "utility", "utilities", "electric", "water", "gas supply",
            ],
            "Index": [
                "index", "indeks", "all market", "global", "msci", "stoxx", "s&p",
                "nasdaq", "omx", "euro", "emerging market", "acwi",
            ],
        }

        # Check each sector's keywords
        for sector, keywords in sector_keywords.items():
            for keyword in keywords:
                if keyword in name_lower:
                    return sector

        return None

    @staticmethod
    def fill_missing_sectors(df: pd.DataFrame) -> pd.DataFrame:
        """
        Fill missing sector values by inferring from security name.

        Args:
            df: Portfolio DataFrame with potential missing sectors

        Returns:
            DataFrame with filled sector values
        """
        df = df.copy()

        # Find rows with missing sectors
        missing_mask = df["Sektor"].isna() | (df["Sektor"] == "")

        if missing_mask.any():
            # Try to infer sector from mapped security name first, then security name
            for idx in df[missing_mask].index:
                inferred_sector = None

                # Try Mapped_Security first
                if "Mapped_Security" in df.columns and pd.notna(df.loc[idx, "Mapped_Security"]):
                    inferred_sector = DataProcessor.infer_sector_from_name(
                        df.loc[idx, "Mapped_Security"]
                    )

                # Fall back to Security name
                if inferred_sector is None and "Security" in df.columns:
                    inferred_sector = DataProcessor.infer_sector_from_name(
                        df.loc[idx, "Security"]
                    )

                # If still not found, assign a default based on type
                if inferred_sector is None and "Type" in df.columns:
                    security_type = df.loc[idx, "Type"]
                    if pd.notna(security_type):
                        if security_type.lower() == "etf":
                            inferred_sector = "Index"
                        else:
                            inferred_sector = "Other"

                if inferred_sector is not None:
                    df.loc[idx, "Sektor"] = inferred_sector

        return df

    @staticmethod
    def aggregate_by_sector(df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate portfolio data by sector.

        Args:
            df: Portfolio DataFrame

        Returns:
            DataFrame with sector aggregations
        """
        sector_data = df.groupby("Sektor").agg({
            "Value_DKK": "sum",
            "Return_DKK": "sum",
            "Return_Percent": "mean",
            "Weight": "sum",
            "Mapped_Security": "count",
        }).round(2)

        sector_data.rename(
            columns={"Mapped_Security": "Num_Holdings"},
            inplace=True
        )

        sector_data["Return_Percent"] = sector_data["Return_Percent"].round(2)
        sector_data = sector_data.sort_values("Value_DKK", ascending=False)
        
        return sector_data

    @staticmethod
    def aggregate_by_type(df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate portfolio data by security type.

        Args:
            df: Portfolio DataFrame

        Returns:
            DataFrame with type aggregations
        """
        type_data = df.groupby("Type").agg({
            "Value_DKK": "sum",
            "Return_DKK": "sum",
            "Return_Percent": "mean",
            "Weight": "sum",
            "Mapped_Security": "count",
        }).round(2)

        type_data.rename(
            columns={"Mapped_Security": "Num_Holdings"},
            inplace=True
        )

        type_data["Return_Percent"] = type_data["Return_Percent"].round(2)
        type_data = type_data.sort_values("Value_DKK", ascending=False)
        
        return type_data

    @staticmethod
    def get_top_holdings(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """
        Get top N holdings by value.

        Args:
            df: Portfolio DataFrame
            n: Number of top holdings to return

        Returns:
            DataFrame with top holdings
        """
        return (
            df.nlargest(n, "Value_DKK")[
                ["Mapped_Security", "Value_DKK", "Return_DKK", "Return_Percent", "Sektor"]
            ]
            .reset_index(drop=True)
        )

    @staticmethod
    def get_best_performers(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
        """
        Get best performing holdings by return percentage.

        Args:
            df: Portfolio DataFrame
            n: Number of holdings to return

        Returns:
            DataFrame with best performers
        """
        return (
            df.nlargest(n, "Return_Percent")[
                ["Mapped_Security", "Value_DKK", "Return_DKK", "Return_Percent", "Sektor"]
            ]
            .reset_index(drop=True)
        )

    @staticmethod
    def get_worst_performers(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
        """
        Get worst performing holdings by return percentage.

        Args:
            df: Portfolio DataFrame
            n: Number of holdings to return

        Returns:
            DataFrame with worst performers
        """
        return (
            df.nsmallest(n, "Return_Percent")[
                ["Mapped_Security", "Value_DKK", "Return_DKK", "Return_Percent", "Sektor"]
            ]
            .reset_index(drop=True)
        )

    @staticmethod
    def get_unique_values(df: pd.DataFrame, column: str) -> List[str]:
        """
        Get unique values for a column, sorted and excluding None/NaN.

        Args:
            df: Portfolio DataFrame
            column: Column name

        Returns:
            Sorted list of unique values
        """
        return sorted(df[column].dropna().unique().tolist())

    @staticmethod
    def filter_data(
        df: pd.DataFrame,
        security_types: List[str] = None,
        sectors: List[str] = None,
        platforms: List[str] = None,
        regions: List[str] = None,
        currencies: List[str] = None,
        search_term: str = None,
    ) -> pd.DataFrame:
        """
        Apply multiple filters to portfolio data.

        Args:
            df: Portfolio DataFrame
            security_types: Filter by security type
            sectors: Filter by sector
            platforms: Filter by platform
            regions: Filter by region
            currencies: Filter by currency
            search_term: Search by security name or ticker

        Returns:
            Filtered DataFrame
        """
        filtered_df = df.copy()

        if security_types:
            filtered_df = filtered_df[filtered_df["Type"].isin(security_types)]

        if sectors:
            filtered_df = filtered_df[filtered_df["Sektor"].isin(sectors)]

        if platforms:
            filtered_df = filtered_df[filtered_df["Platform"].isin(platforms)]

        if regions:
            filtered_df = filtered_df[filtered_df["Region"].isin(regions)]

        if currencies:
            filtered_df = filtered_df[filtered_df["Currency"].isin(currencies)]

        if search_term:
            search_mask = (
                filtered_df["Mapped_Security"].str.contains(
                    search_term, case=False, na=False
                )
                | filtered_df["TICKER"].str.contains(
                    search_term, case=False, na=False
                )
            )
            filtered_df = filtered_df[search_mask]

        return filtered_df
