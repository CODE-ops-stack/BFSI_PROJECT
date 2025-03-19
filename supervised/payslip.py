import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import re

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def payslip_module():
    st.title("Payslip Analysis Module")
    st.markdown("Upload your payslips (CSV or image). For images, OCR will extract key information such as salary details and deductions.")
    
    files = st.file_uploader("Upload Payslip Documents", type=["csv", "png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if files:
        for file in files:
            ext = file.name.split(".")[-1].lower()
            st.markdown(f"**Processing file: {file.name}**")
            if ext == "csv":
                try:
                    df = pd.read_csv(file)
                    st.markdown("**Payslip CSV Preview:**")
                    st.dataframe(df.head())
                    if "Net Salary" in df.columns:
                        st.write("Net Salary Summary:", df["Net Salary"].describe())
                    else:
                        st.info("CSV does not include a 'Net Salary' column.")
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
            elif ext in ["png", "jpg", "jpeg"]:
                try:
                    image = Image.open(file)
                    text = extract_text_from_image(image)
                    st.markdown("**Extracted Text from Payslip Image:**")
                    st.text_area("", text, height=150)
                    # Optionally extract salary figures
                    salaries = re.findall(r'\d+\.\d{2}', text)
                    if salaries:
                        st.write("Extracted Salary Figures:", salaries)
                    else:
                        st.info("No salary figures found in the image text.")
                except Exception as e:
                    st.error(f"Error processing image: {e}")
            else:
                st.info("Unsupported file format.")
    else:
        st.info("Please upload at least one payslip document.")

def main():
    payslip_module()

if __name__ == "__main__":
    main()
