import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def stock_analysis_module():
    st.title("Stock Market Analysis")
    st.markdown("Upload one or more CSV files containing stock data. Each CSV file should have at least two columns: `Date` and `Close`.")
    
    # Upload multiple CSV files
    files = st.file_uploader("Upload Stock Market Data (CSV)", type=["csv"], accept_multiple_files=True)
    
    # To store individual stock series for combined visualization
    aggregated_series = []
    
    if files:
        for idx, file in enumerate(files, start=1):
            st.markdown(f"### Stock Data File {idx}: {file.name}")
            try:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(file)
                st.subheader("Data Preview")
                st.dataframe(df.head())
                
                # Check if required columns exist
                if "Date" in df.columns and "Close" in df.columns:
                    # Convert the Date column to datetime and sort the data
                    df["Date"] = pd.to_datetime(df["Date"])
                    df = df.sort_values("Date")
                    
                    # Display an individual line chart for the stock's closing price
                    st.line_chart(df.set_index("Date")["Close"])
                    st.markdown("**Individual Stock Trend:** The above chart shows the stock's closing prices over time.")
                    
                    # Append the series for combined visualization
                    aggregated_series.append((file.name, df.set_index("Date")["Close"]))
                else:
                    st.info("The CSV must contain 'Date' and 'Close' columns.")
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")
        
        # If multiple stock series have been uploaded, create a combined visualization
        if aggregated_series:
            st.subheader("Combined Stock Closing Prices")
            st.markdown("This combined chart overlays the closing prices of all uploaded stocks for comparison.")
            fig, ax = plt.subplots(figsize=(10, 6))
            cmap = plt.get_cmap("tab10")
            for i, (name, series) in enumerate(aggregated_series):
                ax.plot(series.index, series.values, label=name, color=cmap(i))
            ax.set_xlabel("Date")
            ax.set_ylabel("Closing Price")
            ax.set_title("Combined Line Chart of Stock Closing Prices")
            ax.legend(title="Stocks")
            st.pyplot(fig)
    else:
        st.info("Please upload at least one CSV file for stock market analysis.")

def main():
    stock_analysis_module()

if __name__ == "__main__":
    main()
