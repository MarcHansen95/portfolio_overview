"""Data loading module for portfolio data."""

import pandas as pd
import streamlit as st
from pathlib import Path
from src.config.constants import DATA_FILE, COLUMNS


class DataLoader:
    """Handles loading and initial validation of portfolio data."""

    @staticmethod
    @st.cache_data
    def load_portfolio_data():
        """
        Load portfolio data from Excel file and infer missing sectors.

        Returns:
            pd.DataFrame: Portfolio data with all columns and filled sectors
            
        Raises:
            FileNotFoundError: If data file is not found
            pd.errors.EmptyDataError: If Excel file is empty
        """
        file_path = Path(DATA_FILE)

        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        try:
            df = pd.read_excel(file_path)
            
            # Validate that required columns exist
            required_columns = set(COLUMNS.values())
            missing_columns = required_columns - set(df.columns)
            
            if missing_columns:
                raise ValueError(
                    f"Missing required columns in data file: {missing_columns}"
                )
            
            # Fill missing sectors using inference
            from src.data.processor import DataProcessor
            df = DataProcessor.fill_missing_sectors(df)
            
            return df
        except Exception as e:
            raise Exception(f"Error loading portfolio data: {str(e)}")

    @staticmethod
    def validate_data(df: pd.DataFrame) -> tuple[bool, str]:
        """
        Validate data integrity.

        Args:
            df: Portfolio DataFrame

        Returns:
            tuple: (is_valid, message)
        """
        if df.empty:
            return False, "No portfolio data loaded"

        # Check for critical columns with NaN values
        critical_columns = ["Value_DKK", "Mapped_Security", "Type", "Sektor"]
        null_counts = df[critical_columns].isnull().sum()
        
        if null_counts.any():
            return False, f"Missing values in critical columns: {null_counts[null_counts > 0].to_dict()}"

        return True, "Data validation passed"

    @staticmethod
    def save_portfolio_data(df: pd.DataFrame, file_path: str | None = None) -> None:
        """
        Save portfolio data back to Excel and recalculate derived values.

        Args:
            df: Portfolio DataFrame with edited holdings
            file_path: Optional override for the target Excel file
        """
        df = df.copy()

        if "Antal" in df.columns and "Price" in df.columns:
            quantity = pd.to_numeric(df["Antal"], errors="coerce")
            price = pd.to_numeric(df["Price"], errors="coerce")
            df["Value_DKK"] = quantity * price

        if "Value_DKK" in df.columns and "Return_Percent" in df.columns:
            value = pd.to_numeric(df["Value_DKK"], errors="coerce")
            return_pct = pd.to_numeric(df["Return_Percent"], errors="coerce")
            df["Return_DKK"] = value * return_pct / 100

        if "Value_DKK" in df.columns:
            total_value = pd.to_numeric(df["Value_DKK"], errors="coerce").sum()
            if total_value != 0:
                df["Weight"] = (
                    pd.to_numeric(df["Value_DKK"], errors="coerce") / total_value * 100
                )
            else:
                df["Weight"] = 0

        from src.data.processor import DataProcessor

        if "Sektor" in df.columns:
            df = DataProcessor.fill_missing_sectors(df)
        elif "Sector" in df.columns:
            df = df.rename(columns={"Sector": "Sektor"})
        else:
            df["Sektor"] = "Other"

        target_path = Path(file_path or DATA_FILE)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(target_path, index=False)
