import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import re

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def balance_sheet_module():
    st.title("Balance Sheet Analysis Module")
    st.markdown("Upload balance sheet documents (CSV or image). The app extracts text from images and displays a data preview.")
    
    files = st.file_uploader("Upload Balance Sheet Documents", type=["csv", "png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if files:
        for file in files:
            ext = file.name.split(".")[-1].lower()
            st.markdown(f"**Processing file: {file.name}**")
            if ext == "csv":
                try:
                    df = pd.read_csv(file)
                    st.markdown("**Balance Sheet CSV Preview:**")
                    st.dataframe(df.head())
                    # Look for typical balance sheet fields such as Assets, Liabilities
                    if "Assets" in df.columns and "Liabilities" in df.columns:
                        st.write("Assets Summary:", df["Assets"].describe())
                        st.write("Liabilities Summary:", df["Liabilities"].describe())
                    else:
                        st.info("CSV may not include typical 'Assets' or 'Liabilities' columns.")
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
            elif ext in ["png", "jpg", "jpeg"]:
                try:
                    image = Image.open(file)
                    text = extract_text_from_image(image)
                    st.markdown("**Extracted Text from Balance Sheet Image:**")
                    st.text_area("", text, height=150)
                    # Optionally extract numbers
                    numbers = re.findall(r'\d+\.\d{2}', text)
                    if numbers:
                        st.write("Extracted Numbers:", numbers)
                    else:
                        st.info("No numeric data found in the image text.")
                except Exception as e:
                    st.error(f"Error processing image: {e}")
            else:
                st.info("Unsupported file format.")
    else:
        st.info("Please upload at least one balance sheet document.")

def main():
    balance_sheet_module()

if __name__ == "__main__":
    main()
