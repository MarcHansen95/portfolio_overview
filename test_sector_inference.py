"""Test sector inference functionality."""
import pandas as pd
from src.data.processor import DataProcessor

test_names = [
    'Global Index Fund',
    'XACT OMXC25 ESG (UCITS ETF)',
    'Xtrackers MSCI Emerging Markets UCITS ETF 1C',
    'iShares Digital Security UCITS ETF USD (Acc)',
    'iShares S&P 500 Info Technolg Sctr UCITS ETF USD Acc',
    'Xtrackers Euro Stoxx 50 UCITS ETF 1C',
    'iShares MSCI ACWI USD Acc UCITS ETF',
    'Xtrackers MSCI World Materials UCITS ETF 1C',
    'Danske Inv Global Indeks, kl DKK d',
    'Storebrand Indeks - Alle Markeder A5',
]

print("Testing sector inference:")
print("-" * 70)
for name in test_names:
    sector = DataProcessor.infer_sector_from_name(name)
    print(f'{name:50} -> {sector}')

print("\n" + "=" * 70)
print("Testing full data loading with sector filling:")
print("=" * 70)

from src.data.loader import DataLoader

try:
    df = DataLoader.load_portfolio_data()
    print(f"\nData loaded successfully!")
    print(f"Total rows: {len(df)}")
    print(f"Sectors with NaN: {df['Sektor'].isna().sum()}")
    print(f"\nSector distribution after inference:")
    print(df['Sektor'].value_counts())
except Exception as e:
    print(f"Error: {e}")
