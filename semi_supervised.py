import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Helper function: Generate vibrant colors using a chosen colormap
def get_vibrant_colors(n, cmap_name="Set1"):
    cmap = plt.get_cmap(cmap_name)
    return [cmap(i / n) for i in range(n)]

def semi_supervised_module():
    st.title("BFSI OCR of Bank Statement - Semi-Supervised Module")
    st.markdown("Upload a CSV file containing semi-structured data. The data will be previewed and visualized for key insights.")

    # File uploader for CSV data
    file = st.file_uploader("Upload Semi-Structured CSV", type=["csv"])
    
    if file is not None:
        try:
            # Read CSV into a DataFrame
            df = pd.read_csv(file)
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            # Identify numeric columns for visualization
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            if numeric_cols:
                col = st.selectbox("Select a numeric column for visualization", numeric_cols)
                
                # Bar Chart Visualization
                st.markdown("**Bar Chart:** Distribution of the selected numeric column.")
                fig, ax = plt.subplots()
                df[col].plot(kind="bar", ax=ax, color=get_vibrant_colors(1, "Set2")[0], edgecolor="black")
                ax.set_xlabel("Index")
                ax.set_ylabel(col)
                ax.set_title(f"Bar Chart of {col}")
                st.pyplot(fig)
                
                # Pie Chart Visualization
                st.markdown("**Pie Chart:** Proportions of data in defined ranges for the selected column.")
                if df[col].nunique() <= 10:
                    # If few unique values, show value counts directly
                    data = df[col].value_counts()
                    labels = data.index.astype(str)
                    sizes = data.values
                else:
                    # Create bins for broader ranges
                    bins = np.linspace(df[col].min(), df[col].max(), 6)
                    data = pd.cut(df[col], bins=bins).value_counts().sort_index()
                    labels = [f"{round(interval.left, 2)} - {round(interval.right, 2)}" for interval in data.index]
                    sizes = data.values
                pie_colors = get_vibrant_colors(len(labels), "Set2")
                fig2, ax2 = plt.subplots()
                ax2.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, colors=pie_colors)
                ax2.axis('equal')
                ax2.set_title(f"Pie Chart of {col}")
                st.pyplot(fig2)
            else:
                st.info("No numeric columns found for visualization in the uploaded CSV.")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    else:
        st.info("Please upload a CSV file for semi-supervised analysis.")

def main():
    semi_supervised_module()

if __name__ == "__main__":
    main()
