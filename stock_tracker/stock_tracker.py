import streamlit as st
import pandas as pd
import yfinance as yf

# App title
st.title("NSE Stock Tracker")
st.markdown("Track your favorite NSE stocks and their performance.")

# List of sample NSE stocks (you can customize this list)
sample_stocks = {
    "RELIANCE": "Reliance Industries Ltd",
    "TCS": "Tata Consultancy Services",
    "INFY": "Infosys",
    "HDFCBANK": "HDFC Bank",
    "ITC": "ITC Limited",
    "SBIN": "State Bank of India"
}

# Function to fetch stock data
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker + ".NS")
        hist = stock.history(period="1y")
        current_price = stock.info['currentPrice']
        pe_ratio = stock.info.get('forwardPE', "N/A")
        industry = stock.info.get('industry', "N/A")
        fifty_two_week_high = stock.info.get('fiftyTwoWeekHigh', "N/A")
        fifty_two_week_low = stock.info.get('fiftyTwoWeekLow', "N/A")
        one_year_change = stock.info.get('52WeekChange', "N/A")

        gain_from_low = round(((current_price - fifty_two_week_low) / fifty_two_week_low) * 100, 2) if fifty_two_week_low != "N/A" else "N/A"
        drop_from_high = round(((fifty_two_week_high - current_price) / fifty_two_week_high) * 100, 2) if fifty_two_week_high != "N/A" else "N/A"

        trend = "Upward" if current_price > hist['Close'].iloc[0] else "Downward"

        return {
            "Company Name": sample_stocks.get(ticker, "Unknown"),
            "Industry": industry,
            "52W Low": fifty_two_week_low,
            "52W High": fifty_two_week_high,
            "Current Price": current_price,
            "Gain from 52W Low (%)": gain_from_low,
            "Drop from 52W High (%)": drop_from_high,
            "1-Year Change (%)": round(one_year_change * 100, 2) if one_year_change != "N/A" else "N/A",
            "1-Year Trend": trend,
            "PE Ratio": pe_ratio
        }
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

# User input for stock selection
selected_stocks = st.multiselect("Select Stocks", options=list(sample_stocks.keys()))

# Fetch and display stock data
if selected_stocks:
    data = [get_stock_data(ticker) for ticker in selected_stocks]
    data = [d for d in data if d is not None]  # Remove None entries in case of errors
    df = pd.DataFrame(data)

    # Display data as a table
    st.dataframe(df)
else:
    st.warning("Please select at least one stock to display data.")
