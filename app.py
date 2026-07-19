"""Main Streamlit application for Portfolio Overview."""

import streamlit as st
import pandas as pd
from src.config.constants import APP_TITLE, APP_ICON, PAGE_LAYOUT, INITIAL_SIDEBAR_STATE
from src.data.loader import DataLoader
from src.data.processor import DataProcessor
from src.utils.filters import FilterManager
from src.components.kpi_cards import KPICard
from src.components.charts import Charts
from src.components.tables import Tables


# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE,
)

# Minimal custom CSS - keep default Streamlit theme
st.markdown(
    """
    <style>
    [data-testid="stMetricContainer"] {
        padding: 15px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "data" not in st.session_state:
        st.session_state.data = None
    if "filtered_data" not in st.session_state:
        st.session_state.filtered_data = None


def load_and_validate_data() -> pd.DataFrame:
    """
    Load and validate portfolio data.

    Returns:
        Portfolio DataFrame or None if loading fails
    """
    try:
        data = DataLoader.load_portfolio_data()
        is_valid, message = DataLoader.validate_data(data)
        
        if not is_valid:
            st.error(f"Data validation failed: {message}")
            return None
        
        # Calculate weights for all data
        data = DataProcessor.calculate_weights(data)
        return data
    except Exception as e:
        st.error(f"Error loading portfolio data: {str(e)}")
        return None


def render_sidebar_filters(df: pd.DataFrame) -> None:
    """
    Render filter controls in the sidebar.

    Args:
        df: Portfolio DataFrame
    """
    with st.sidebar:
        st.header("🔍 Filters")
        
        # Initialize filters
        FilterManager.initialize_filters(df)
        
        # Get available filter options
        filter_options = FilterManager.get_filter_options(df)
        
        # Security Type Filter
        security_types = st.multiselect(
            "Security Type",
            options=filter_options["security_types"],
            default=st.session_state.filters["security_types"],
            key="filter_types",
        )
        st.session_state.filters["security_types"] = security_types
        
        # Sector Filter
        sectors = st.multiselect(
            "Sector",
            options=filter_options["sectors"],
            default=st.session_state.filters["sectors"],
            key="filter_sectors",
        )
        st.session_state.filters["sectors"] = sectors
        
        # Platform Filter
        platforms = st.multiselect(
            "Platform",
            options=filter_options["platforms"],
            default=st.session_state.filters["platforms"],
            key="filter_platforms",
        )
        st.session_state.filters["platforms"] = platforms
        
        # Region Filter
        regions = st.multiselect(
            "Region",
            options=filter_options["regions"],
            default=st.session_state.filters["regions"],
            key="filter_regions",
        )
        st.session_state.filters["regions"] = regions
        
        # Currency Filter
        currencies = st.multiselect(
            "Currency",
            options=filter_options["currencies"],
            default=st.session_state.filters["currencies"],
            key="filter_currencies",
        )
        st.session_state.filters["currencies"] = currencies
        
        # Search Box
        search_term = st.text_input(
            "Search by name or ticker",
            value=st.session_state.filters["search_term"],
            key="filter_search",
        )
        st.session_state.filters["search_term"] = search_term
        
        # Filter buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset Filters", use_container_width=True):
                FilterManager.reset_filters()
                st.rerun()
        
        with col2:
            st.button("✅ Apply", use_container_width=True, disabled=True)
        
        # Show filter status
        if FilterManager.are_filters_active():
            filtered_count = len(st.session_state.filtered_data)
            total_count = len(df)
            st.info(
                f"📊 Filtered: {filtered_count} / {total_count} holdings"
            )


def render_overview_tab(df: pd.DataFrame) -> None:
    """
    Render the overview dashboard tab.

    Args:
        df: Portfolio DataFrame
    """
    st.subheader("📊 Portfolio Overview")
    
    # Calculate totals
    totals = DataProcessor.calculate_totals(df)
    
    # Get type allocation for KPI cards
    type_data = DataProcessor.aggregate_by_type(df)
    type_allocation = type_data["Value_DKK"].to_dict() if not type_data.empty else {}
    
    # Render custom KPI cards
    KPICard.render_portfolio_overview_cards(totals, type_allocation)
    
    st.divider()
    
    # Charts in columns
    col1, col2 = st.columns(2)
    
    with col1:
        Charts.render_sector_pie_chart(df)
    
    with col2:
        Charts.render_top_holdings_bar_chart(df)
        
    
    st.divider()
    
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        Charts.render_sector_performance_chart(df, key_suffix="_overview")
    
    with col2:
        Charts.render_currency_exposure_chart(df)
    
    st.divider()
    
    # Portfolio performance over time
    Charts.render_portfolio_performance_chart(df)


def render_holdings_tab(df: pd.DataFrame) -> None:
    """
    Render the holdings detail tab.

    Args:
        df: Portfolio DataFrame
    """
    st.subheader("📋 Holdings Details")
    
    # Show summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Holdings", len(df))
    with col2:
        st.metric("Total Value", f"DKK {df['Value_DKK'].sum():,.0f}")
    with col3:
        st.metric("Total Return %", f"{(df['Return_DKK'].sum() / (df['Value_DKK'].sum() - df['Return_DKK'].sum()) * 100) if (df['Value_DKK'].sum() - df['Return_DKK'].sum()) != 0 else 0:.2f}%")
    
    st.divider()
    
    # Sort options
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox(
            "Sort by",
            options=[
                "Value (DKK)",
                "Return %",
                "Weight %",
                "Quantity",
                "Security Name",
            ],
        )
    
    with col2:
        sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True)
    
    # Apply sorting
    ascending = sort_order == "Ascending"
    sort_column_map = {
        "Value (DKK)": "Value_DKK",
        "Return %": "Return_Percent",
        "Weight %": "Weight",
        "Quantity": "Antal",
        "Security Name": "Mapped_Security",
    }
    
    sorted_df = df.sort_values(
        by=sort_column_map[sort_by],
        ascending=ascending,
    )
    
    # Render table
    Tables.render_holdings_table(sorted_df)


def render_sector_analysis_tab(df: pd.DataFrame) -> None:
    """
    Render the sector analysis tab.

    Args:
        df: Portfolio DataFrame
    """
    st.subheader("🏭 Sector Analysis")
    
    # Sector breakdown table
    sector_data = DataProcessor.aggregate_by_sector(df)
    
    st.write("**Sector Breakdown**")
    Tables.render_sector_breakdown_table(sector_data)
    
    st.divider()
    
    # Sector performance chart
    Charts.render_sector_performance_chart(df)
    
    st.divider()
    
    # Best and worst performing sectors
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Best Performing Sectors**")
        best_sectors = sector_data.nlargest(5, "Return_Percent")
        if not best_sectors.empty:
            for idx, (sector, row) in enumerate(best_sectors.iterrows(), 1):
                st.metric(
                    f"{idx}. {sector}",
                    f"{row['Return_Percent']:.2f}%",
                    f"DKK {row['Value_DKK']:,.0f}",
                )
    
    with col2:
        st.write("**Worst Performing Sectors**")
        worst_sectors = sector_data.nsmallest(5, "Return_Percent")
        if not worst_sectors.empty:
            for idx, (sector, row) in enumerate(worst_sectors.iterrows(), 1):
                st.metric(
                    f"{idx}. {sector}",
                    f"{row['Return_Percent']:.2f}%",
                    f"DKK {row['Value_DKK']:,.0f}",
                )


def render_asset_allocation_tab(df: pd.DataFrame) -> None:
    """
    Render the asset allocation tab.

    Args:
        df: Portfolio DataFrame
    """
    st.subheader("📐 Asset Allocation")
    
    # Type breakdown
    type_data = DataProcessor.aggregate_by_type(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Asset Type Distribution**")
        Tables.render_sector_breakdown_table(type_data)
    
    with col2:
        st.write("**Geographic Distribution**")
        region_data = df.groupby("Region")["Value_DKK"].sum().reset_index()
        region_data.columns = ["Region", "Value_DKK"]
        st.dataframe(region_data, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Distribution chart
    Charts.render_return_distribution_chart(df)


def main() -> None:
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()
    
    # Page title
    st.title(f"{APP_ICON} {APP_TITLE}")
    
    # Load data
    if st.session_state.data is None:
        with st.spinner("Loading portfolio data..."):
            st.session_state.data = load_and_validate_data()
    
    if st.session_state.data is None:
        st.stop()
    
    data = st.session_state.data
    
    # Render sidebar filters
    render_sidebar_filters(data)
    
    # Apply filters
    st.session_state.filtered_data = FilterManager.apply_filters(data)
    filtered_data = st.session_state.filtered_data
    
    if filtered_data.empty:
        st.warning("No holdings match the selected filters. Please adjust your filters.")
        st.stop()
    
    # Tabs navigation
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Overview", "📋 Holdings", "🏭 Sectors", "📐 Allocation"]
    )
    
    with tab1:
        render_overview_tab(filtered_data)
    
    with tab2:
        render_holdings_tab(filtered_data)
    
    with tab3:
        render_sector_analysis_tab(filtered_data)
    
    with tab4:
        render_asset_allocation_tab(filtered_data)


if __name__ == "__main__":
    main()
