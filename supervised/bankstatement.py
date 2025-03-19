import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import re

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def bank_statement_module():
    st.title("Bank Statement Analysis Module")
    st.markdown("Upload bank statements (CSV or image). The app will extract text from images and display financial data summaries.")
    
    files = st.file_uploader("Upload Bank Statement Documents", type=["csv", "png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if files:
        for file in files:
            ext = file.name.split(".")[-1].lower()
            st.markdown(f"**Processing file: {file.name}**")
            if ext == "csv":
                try:
                    df = pd.read_csv(file)
                    st.markdown("**Bank Statement CSV Preview:**")
                    st.dataframe(df.head())
                    if "Balance" in df.columns:
                        st.write("Balance Summary:", df["Balance"].describe())
                    else:
                        st.info("CSV may not include a 'Balance' column.")
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
            elif ext in ["png", "jpg", "jpeg"]:
                try:
                    image = Image.open(file)
                    text = extract_text_from_image(image)
                    st.markdown("**Extracted Text from Bank Statement Image:**")
                    st.text_area("", text, height=150)
                    # Example: extract numbers that might represent balance figures
                    balances = re.findall(r'\d+\.\d{2}', text)
                    if balances:
                        st.write("Extracted Balances:", balances)
                    else:
                        st.info("No balance figures found in the image text.")
                except Exception as e:
                    st.error(f"Error processing image: {e}")
            else:
                st.info("Unsupported file format.")
    else:
        st.info("Please upload at least one bank statement document.")

def main():
    bank_statement_module()

if __name__ == "__main__":
    main()
