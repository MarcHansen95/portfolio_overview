# Portfolio Overview - Project Structure

## Project Architecture

The Portfolio Overview Streamlit application is built with a clean, modular architecture following best practices for code organization and reusability.

```
portfolio_overview/
├── app.py                          # Main Streamlit application entry point
├── pyproject.toml                  # Poetry project configuration & dependencies
├── poetry.lock                     # Locked dependency versions
├── README.md                       # Project documentation
├── portfolio_data.xlsx             # Portfolio data file (input)
│
└── src/                            # Source code package
    ├── config/                     # Configuration & constants
    │   ├── __init__.py
    │   ├── constants.py            # Column names, labels, metrics, table configs
    │   └── theme.py                # Color schemes, styling, chart configs
    │
    ├── data/                       # Data loading & processing
    │   ├── __init__.py
    │   ├── loader.py               # DataLoader class - Excel file loading & validation
    │   └── processor.py            # DataProcessor class - Calculations & filtering
    │
    ├── utils/                      # Utility functions
    │   ├── __init__.py
    │   ├── formatting.py           # Formatter class - Number/currency/percentage formatting
    │   └── filters.py              # FilterManager class - Filter state management
    │
    └── components/                 # Reusable UI components
        ├── __init__.py
        ├── metrics.py              # MetricCards class - Metric card components
        ├── charts.py               # Charts class - Interactive chart components
        └── tables.py               # Tables class - Table components
```

## Module Descriptions

### Core Modules

#### `app.py` - Main Application
- Entry point for the Streamlit app
- Page configuration and layout management
- Tab-based navigation (Overview, Holdings, Sectors, Allocation)
- Data loading and filter application
- Session state management

#### `src/config/constants.py` - Constants & Configuration
- Column name mappings (original vs display labels)
- App title, icon, and metadata
- Table column configurations
- Metric definitions
- Number formatting rules

#### `src/config/theme.py` - Theme & Styling
- Color palettes for sectors and types
- Chart styling configurations
- Font sizes and spacing
- Metric card and table styling

### Data Handling

#### `src/data/loader.py` - DataLoader Class
```python
class DataLoader:
    @staticmethod
    def load_portfolio_data() -> pd.DataFrame
    @staticmethod
    def validate_data(df: pd.DataFrame) -> tuple[bool, str]
```
- Loads Excel portfolio data with caching
- Validates data integrity
- Handles file errors gracefully

#### `src/data/processor.py` - DataProcessor Class
```python
class DataProcessor:
    @staticmethod
    def calculate_totals(df) -> Dict
    @staticmethod
    def calculate_weights(df) -> pd.DataFrame
    @staticmethod
    def aggregate_by_sector(df) -> pd.DataFrame
    @staticmethod
    def aggregate_by_type(df) -> pd.DataFrame
    @staticmethod
    def get_top_holdings(df, n=10) -> pd.DataFrame
    @staticmethod
    def get_best_performers(df, n=5) -> pd.DataFrame
    @staticmethod
    def get_worst_performers(df, n=5) -> pd.DataFrame
    @staticmethod
    def get_unique_values(df, column) -> List[str]
    @staticmethod
    def filter_data(df, **filters) -> pd.DataFrame
```
- Portfolio calculations and aggregations
- Performance metrics
- Multi-filter support
- Data transformations

### Utilities

#### `src/utils/formatting.py` - Formatter Class
```python
class Formatter:
    @staticmethod
    def format_currency(value) -> str
    @staticmethod
    def format_percentage(value) -> str
    @staticmethod
    def format_weight(value) -> str
    @staticmethod
    def format_number(value, decimals=2) -> str
    @staticmethod
    def get_return_color(value) -> str
```
- Consistent numerical formatting
- Currency, percentage, and weight formatting
- Color coding based on values

#### `src/utils/filters.py` - FilterManager Class
```python
class FilterManager:
    @staticmethod
    def initialize_filters(df) -> None
    @staticmethod
    def get_filter_options(df) -> Dict[str, List[str]]
    @staticmethod
    def reset_filters() -> None
    @staticmethod
    def apply_filters(df) -> pd.DataFrame
    @staticmethod
    def are_filters_active() -> bool
```
- Filter state management using Streamlit session state
- Filter option discovery from data
- Filter application and reset functionality

### UI Components

#### `src/components/metrics.py` - MetricCards Class
```python
class MetricCards:
    @staticmethod
    def render_metric_card(label, value, delta=None, formatter_func=None)
    @staticmethod
    def render_overview_metrics(totals) -> None
```
- Portfolio summary metric cards
- Customizable formatting and delta display
- 4-column layout for overview metrics

#### `src/components/charts.py` - Charts Class
```python
class Charts:
    @staticmethod
    def render_sector_pie_chart(df) -> None
    @staticmethod
    def render_type_pie_chart(df) -> None
    @staticmethod
    def render_top_holdings_bar_chart(df, n=10) -> None
    @staticmethod
    def render_sector_performance_chart(df) -> None
    @staticmethod
    def render_return_distribution_chart(df) -> None
    @staticmethod
    def render_currency_exposure_chart(df) -> None
```
- Interactive Plotly charts
- Pie charts for allocation visualization
- Bar charts for comparative analysis
- Scatter plots for performance distribution
- All charts respect theme colors and configurations

#### `src/components/tables.py` - Tables Class
```python
class Tables:
    @staticmethod
    def format_dataframe_for_display(df) -> pd.DataFrame
    @staticmethod
    def render_holdings_table(df) -> None
    @staticmethod
    def render_sector_breakdown_table(df) -> None
    @staticmethod
    def render_top_performers_table(df, title) -> None
```
- Sortable holdings table with all portfolio metrics
- Sector breakdown table with aggregations
- Top/worst performers tables
- Consistent formatting across all tables

## Key Features

### Dashboard Views

1. **Overview Tab** 📊
   - 4 metric cards: Total Value, Return, Return %, Holdings
   - Sector allocation pie chart
   - Asset type pie chart
   - Top 10 holdings bar chart
   - Sector performance chart
   - Currency exposure pie chart

2. **Holdings Tab** 📋
   - Sortable/filterable holdings table
   - 11 columns with holdings details
   - Sort by: Value, Return %, Weight, Quantity, Name
   - Ascending/Descending sort order

3. **Sectors Tab** 🏭
   - Sector breakdown table
   - Best/worst performing sectors
   - Sector performance chart
   - Aggregated metrics by sector

4. **Allocation Tab** 📐
   - Asset type distribution
   - Geographic distribution
   - Return vs value scatter plot

### Filter Sidebar
- Multi-select filters for:
  - Security Type
  - Sector
  - Platform
  - Market
  - Region
  - Currency
- Text search by security name or ticker
- Reset and Apply buttons
- Active filter counter

## Design Patterns

### 1. Class-Based Organization
- Static methods for utility functions
- Single responsibility principle
- Easy to import and use

### 2. Configuration Management
- Centralized constants
- Theme configuration separate from logic
- Easy to maintain and update

### 3. Data Processing Pipeline
- Separation of concerns (loading, processing, filtering)
- Reusable processor methods
- Cached data loading with Streamlit

### 4. UI Component Composition
- Modular chart and table components
- Consistent styling
- Easy to reuse and extend

### 5. Session State Management
- Filter persistence across reruns
- Efficient data filtering
- Clean state initialization

## Dependencies

- **streamlit** (>=1.35.0) - Web framework
- **pandas** (>=2.1.0) - Data manipulation
- **plotly** (>=5.17.0) - Interactive charts
- **altair** (>=5.1.0) - Declarative visualization
- **numpy** (>=1.24.0) - Numerical computing

## Running the App

```bash
# Install dependencies
poetry install

# Run the app
poetry run streamlit run app.py

# Access at http://localhost:8501
```

## Code Quality Practices

✅ Modular architecture with clear separation of concerns
✅ Reusable components and utility functions
✅ Centralized configuration management
✅ Type hints for better code documentation
✅ Docstrings for all classes and methods
✅ Consistent naming conventions
✅ Error handling with user-friendly messages
✅ Data validation and integrity checks
✅ Performance optimization with caching
✅ Responsive design with adaptive layouts

---

**Status**: ✅ Fully implemented and ready to use
**Version**: 0.1.0
**Date**: February 28, 2026
