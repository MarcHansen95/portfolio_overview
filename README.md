# Portfolio Overview

A user-friendly Streamlit dashboard for portfolio analysis and performance tracking.

## Features

- **Portfolio Dashboard**: View your total portfolio value, returns, and key metrics
- **Holdings Analysis**: Detailed breakdown of all investments with sortable/filterable tables
- **Sector Analysis**: Understand your sector exposure and performance
- **Asset Allocation**: Visualize portfolio composition by type and sector
- **Interactive Filters**: Filter by security type, sector, platform, market, region, and currency

## Installation

```bash
poetry install
```

## Running the App

```bash
poetry run streamlit run app.py
```

## Data

The app loads portfolio data from an Excel file (`portfolio_data.xlsx`) with the following columns:

- Midler, Platform, Depot, Security, Mapped_Security
- Sektor, Type, TICKER, yahoo_tickers, Market
- Antal, GAK, Currency, Price, Value_DKK
- Return_DKK, Return_Percent, Weight, exchange_rate_dkk, Region

## License

MIT
