import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import re

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def invoice_module():
    st.title("Invoice Analysis Module")
    st.markdown("Upload invoice documents (CSV or image). For images, OCR will extract key details (e.g., invoice numbers, amounts).")
    
    files = st.file_uploader("Upload Invoice Documents", type=["csv", "png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if files:
        for file in files:
            ext = file.name.split(".")[-1].lower()
            st.markdown(f"**Processing file: {file.name}**")
            if ext == "csv":
                try:
                    df = pd.read_csv(file)
                    st.markdown("**Invoice CSV Preview:**")
                    st.dataframe(df.head())
                    # If an 'Amount' column exists, show summary
                    if "Amount" in df.columns:
                        st.write("Invoice Amount Summary:", df["Amount"].describe())
                    else:
                        st.info("CSV does not include an 'Amount' column.")
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
            elif ext in ["png", "jpg", "jpeg"]:
                try:
                    image = Image.open(file)
                    text = extract_text_from_image(image)
                    st.markdown("**Extracted Text from Invoice Image:**")
                    st.text_area("", text, height=150)
                    # Optionally extract numeric amounts if present
                    amounts = re.findall(r'\d+\.\d{2}', text)
                    if amounts:
                        st.write("Extracted Amounts:", amounts)
                    else:
                        st.info("No numeric amounts found in the image text.")
                except Exception as e:
                    st.error(f"Error processing image: {e}")
            else:
                st.info("Unsupported file format.")
    else:
        st.info("Please upload at least one invoice document.")

def main():
    invoice_module()

if __name__ == "__main__":
    main()
