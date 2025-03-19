import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import re

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def profit_loss_module():
    st.title("Profit/Loss Statement Analysis Module")
    st.markdown("Upload profit/loss statements (CSV or image). The module extracts key financial information and provides a data preview.")
    
    files = st.file_uploader("Upload Profit/Loss Documents", type=["csv", "png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if files:
        for file in files:
            ext = file.name.split(".")[-1].lower()
            st.markdown(f"**Processing file: {file.name}**")
            if ext == "csv":
                try:
                    df = pd.read_csv(file)
                    st.markdown("**Profit/Loss CSV Preview:**")
                    st.dataframe(df.head())
                    # If a 'Profit' or 'Loss' column exists, show summary
                    if "Profit" in df.columns:
                        st.write("Profit Summary:", df["Profit"].describe())
                    elif "Loss" in df.columns:
                        st.write("Loss Summary:", df["Loss"].describe())
                    else:
                        st.info("CSV does not include 'Profit' or 'Loss' columns.")
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
            elif ext in ["png", "jpg", "jpeg"]:
                try:
                    image = Image.open(file)
                    text = extract_text_from_image(image)
                    st.markdown("**Extracted Text from Profit/Loss Image:**")
                    st.text_area("", text, height=150)
                    # Optionally extract profit/loss figures
                    figures = re.findall(r'\d+\.\d{2}', text)
                    if figures:
                        st.write("Extracted Figures:", figures)
                    else:
                        st.info("No profit/loss figures found in the image text.")
                except Exception as e:
                    st.error(f"Error processing image: {e}")
            else:
                st.info("Unsupported file format.")
    else:
        st.info("Please upload at least one profit/loss statement document.")

def main():
    profit_loss_module()

if __name__ == "__main__":
    main()
