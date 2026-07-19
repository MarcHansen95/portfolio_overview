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
