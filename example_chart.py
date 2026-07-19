@st.fragment()
def performance_chart(portfolio):
    # Time period options
    period_options = {
        "10 Years": 365 * 10,
        "1 Year": 365,
        "6 Months": 182,
        "3 Months": 90,
        "1 Month": 30
    }
    selected_period = st.selectbox("Select Time Period", list(period_options.keys()), index=1)
    days = period_options[selected_period]

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
        
    # Fetch all tickers at once
    tickers = portfolio['yahoo_tickers'].unique()
    try:
        price_data = yf.download(tickers.tolist(), start=start_date, end=end_date, interval="1d", auto_adjust=True, group_by="ticker")
    except Exception as e:
        st.error(f"Error fetching price data: {str(e)}")
        price_data = None

    fig_performance = go.Figure()
    fig_performance.add_hline(y=0, line_dash="solid", line_color="red")

    if price_data is not None and not price_data.empty:
        unique_combinations = portfolio[['yahoo_tickers', 'Security']].drop_duplicates()
        for _, row in unique_combinations.iterrows():
            ticker = row['yahoo_tickers']
            name = row['Security']
            try:
                if ticker in price_data and not price_data[ticker]['Close'].empty:
                    closing_prices = price_data[ticker]['Close'].dropna()
                    if not closing_prices.empty:
                        first_price = closing_prices.iloc[0]
                        relative_changes = ((closing_prices - first_price) / first_price) * 100
                        fig_performance.add_trace(
                            go.Scatter(
                                x=closing_prices.index,
                                y=relative_changes,
                                mode='lines',
                                name=name,
                                visible="legendonly"
                            )
                        )
            except Exception as e:
                st.warning(f"Could not process data for {name} ({ticker}): {str(e)}")

    fig_performance.update_layout(
        title=f"{selected_period} Relative Performance",
        xaxis_title="Date",
        yaxis_title="Relative Change (%)",
        template="plotly_dark",
        showlegend=True
    )
    fig_performance.update_yaxes(ticksuffix="%")
    st.plotly_chart(fig_performance, use_container_width=True)