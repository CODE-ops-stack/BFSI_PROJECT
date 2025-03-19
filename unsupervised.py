import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def unsupervised_module():
    st.title("Unsupervised Module - Clustering Analysis")
    file = st.file_uploader("Upload Unstructured CSV", type=["csv"])
    if file is not None:
        try:
            df = pd.read_csv(file)
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            if numeric_cols:
                col = st.selectbox("Select a numeric column for clustering", numeric_cols)
                try:
                    X = df[[col]].dropna()
                    kmeans = KMeans(n_clusters=3, random_state=0)
                    clusters = kmeans.fit_predict(X)
                    df['Cluster'] = None
                    df.loc[X.index, 'Cluster'] = clusters
                    st.subheader("Clustering Result")
                    st.dataframe(df.head())
                    
                    st.markdown("**Scatter Plot:**")
                    fig, ax = plt.subplots()
                    ax.scatter(range(len(X)), X[col], c=clusters, cmap='viridis')
                    ax.set_xlabel("Index")
                    ax.set_ylabel(col)
                    ax.set_title(f"Clustering on {col}")
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error during clustering: {e}")
            else:
                st.info("No numeric columns found in the CSV.")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    else:
        st.info("Upload a CSV file for clustering analysis.")

def main():
    unsupervised_module()

if __name__ == "__main__":
    main()
