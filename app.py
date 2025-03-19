import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image
import re
import random
from sklearn.cluster import KMeans

# =============================================================================
# Helper Function: Generate Vibrant Colors
# =============================================================================
def get_vibrant_colors(n, cmap_name="Set1"):
    cmap = plt.get_cmap(cmap_name)
    return [cmap(i / n) for i in range(n)]

# =============================================================================
# Demo Email OTP Authentication (Demo Mode)
# =============================================================================
def demo_email_otp_authentication():
    """
    This demo-based OTP authentication simulates email-based OTP.
    The user enters an email address, a 6-digit OTP is generated and displayed,
    and the user must enter the same OTP to proceed.
    """
    if "otp_verified" not in st.session_state:
        st.session_state.otp_verified = False

    if not st.session_state.otp_verified:
        st.header("Demo Email OTP Verification")
        st.markdown("**Demo Mode:** Enter your email address below. A 6-digit OTP will be generated and displayed (simulating an email send).")
        recipient_email = st.text_input("Enter your email address:")
        if st.button("Send OTP"):
            otp = random.randint(100000, 999999)
            st.session_state.generated_otp = otp
            st.success(f"OTP sent to {recipient_email} (Demo OTP: {otp})")
        user_otp = st.text_input("Enter the OTP received:")
        if st.button("Verify OTP"):
            try:
                if int(user_otp) == st.session_state.get("generated_otp"):
                    st.session_state.otp_verified = True
                    st.success("OTP verified successfully!")
                else:
                    st.error("Incorrect OTP. Please try again.")
            except Exception as e:
                st.error("Invalid OTP format. Please enter a numeric OTP.")
        st.stop()

# =============================================================================
# Fruit Vibe Integration (For UI)
# =============================================================================
st.sidebar.header("Extra Theming Options")
selected_fruit = st.sidebar.selectbox("Select a fruit", ["Apple", "Cherry", "Date", "Mango"])
fruit_theme = {
    "Apple": "#FF0000",    # Red
    "Cherry": "#FF69B4",   # Hot Pink
    "Date": "#8B4513",     # Brown
    "Mango": "#FFA500"     # Vibrant Orange
}
theme_color = fruit_theme[selected_fruit]
st.sidebar.markdown(f"<h3 style='color:{theme_color};'>Fruit Theme: {selected_fruit}</h3>", unsafe_allow_html=True)

# Inject Dynamic CSS for Background and Header using Fruit Color
st.markdown(
    f"""
    <style>
    body {{
        background: linear-gradient(45deg, #ff9a9e, #fad0c4, #fad0c4);
        background-size: 400% 400%;
        animation: gradientShift 10s ease infinite;
    }}
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    .front-header {{
        background: linear-gradient(90deg, {theme_color}, #ffffff);
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        animation: headerGlow 5s ease infinite alternate;
    }}
    @keyframes headerGlow {{
        0% {{ box-shadow: 0 0 10px {theme_color}; }}
        100% {{ box-shadow: 0 0 30px {theme_color}; }}
    }}
    .reportview-container .main .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# Module 1: Supervised Module - Document Analysis
# =============================================================================
def supervised_module():
    st.title("Supervised Module - Document Analysis")
    st.markdown("Upload documents (CSV and/or images) for analysis. For images, OCR extracts text and numeric values (if any) are aggregated for visualization.")
    
    doc_type = st.selectbox("Select Document Type", 
                             ["Invoices", "Bank Statements", "Payslips", "Balance Sheets", "Profit/Loss Statements"])
    st.write(f"**Document Type Selected:** {doc_type}")
    
    files = st.file_uploader(f"Upload {doc_type} Documents", 
                             type=["csv", "png", "jpg", "jpeg", "pdf", "doc", "docx", "tiff"],
                             accept_multiple_files=True)
    aggregated_values = []
    
    if files:
        for file in files:
            ext = file.name.split(".")[-1].lower()
            st.markdown(f"**Processing: {file.name}**")
            if ext == "csv":
                try:
                    df = pd.read_csv(file)
                    st.markdown("**CSV Preview:**")
                    st.dataframe(df.head())
                    if "Amount" in df.columns:
                        values = df["Amount"].dropna().tolist()
                    else:
                        num_cols = df.select_dtypes(include=np.number).columns.tolist()
                        values = df[num_cols[0]].dropna().tolist() if num_cols else []
                    aggregated_values.extend(values)
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
            elif ext in ["png", "jpg", "jpeg", "tiff"]:
                try:
                    image = Image.open(file)
                    extracted_text = pytesseract.image_to_string(image)
                    st.markdown("**Extracted Text:**")
                    st.text_area("", extracted_text, height=150)
                    numbers = re.findall(r'\d+\.\d{2}', extracted_text)
                    values = [float(x) for x in numbers]
                    aggregated_values.extend(values)
                except Exception as e:
                    st.error(f"Error processing image: {e}")
            elif ext in ["pdf", "doc", "docx"]:
                st.info(f"File {file.name} uploaded. Detailed OCR is not implemented for this format.")
            else:
                st.info(f"File {file.name}: Unsupported file format.")
        
        if aggregated_values:
            st.subheader("Aggregated Data Analysis")
            series = pd.Series(aggregated_values)
            st.write("Summary Statistics:", series.describe())
            
            st.markdown("**Histogram:**")
            hist_vals, bin_edges = np.histogram(aggregated_values, bins=10)
            colors = plt.get_cmap("Set1")(np.linspace(0, 1, len(hist_vals)))
            fig, ax = plt.subplots()
            for i in range(len(hist_vals)):
                ax.bar((bin_edges[i] + bin_edges[i+1]) / 2, hist_vals[i],
                       width=bin_edges[i+1]-bin_edges[i],
                       color=colors[i], align='center')
            ax.set_xlabel("Extracted Value")
            ax.set_ylabel("Frequency")
            ax.set_title(f"Histogram of {doc_type} Values")
            st.pyplot(fig)
            
            st.markdown("**Box Plot:**")
            fig2, ax2 = plt.subplots()
            bp = ax2.boxplot(aggregated_values, patch_artist=True)
            for patch in bp['boxes']:
                patch.set_facecolor(plt.get_cmap("Set1")(0.5))
            ax2.set_title(f"Box Plot of {doc_type} Values")
            st.pyplot(fig2)
            
            st.markdown("**2D Pie Chart:**")
            try:
                bins = np.linspace(min(aggregated_values), max(aggregated_values), 6)
                binned = pd.cut(aggregated_values, bins=bins)
                counts = binned.value_counts().sort_index()
                labels = [f"{round(interval.left,2)} - {round(interval.right,2)}" for interval in counts.index]
                pie_colors = plt.get_cmap("Set2")(np.linspace(0, 1, len(labels)))
                fig3, ax3 = plt.subplots()
                ax3.pie(counts, labels=labels, autopct="%1.1f%%", startangle=140, colors=pie_colors)
                ax3.axis('equal')
                ax3.set_title(f"2D Pie Chart of {doc_type} Values")
                st.pyplot(fig3)
            except Exception as e:
                st.error(f"Error generating pie chart: {e}")
    else:
        st.info("Please upload at least one document file.")

# =============================================================================
# Module 2: Semi-Supervised Module - Semi-Structured Data Analysis
# =============================================================================
def semi_supervised_module():
    st.title("Semi-Supervised Module - Semi-Structured Data Analysis")
    st.markdown("Upload a CSV file containing semi-structured data. The data will be previewed and a selected numeric column will be visualized.")
    
    file = st.file_uploader("Upload Semi-Structured CSV", type=["csv"])
    if file:
        try:
            df = pd.read_csv(file)
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            if numeric_cols:
                col = st.selectbox("Select a numeric column for visualization", numeric_cols)
                
                st.markdown("**Bar Chart:**")
                fig, ax = plt.subplots()
                df[col].plot(kind="bar", ax=ax, color=plt.get_cmap("Set2")(0.8), edgecolor='black')
                ax.set_xlabel("Index")
                ax.set_ylabel(col)
                ax.set_title(f"Bar Chart of {col}")
                st.pyplot(fig)
                
                st.markdown("**Pie Chart:**")
                if df[col].nunique() <= 10:
                    data = df[col].value_counts()
                    labels = data.index.astype(str)
                    sizes = data.values
                else:
                    bins = np.linspace(df[col].min(), df[col].max(), 6)
                    data = pd.cut(df[col], bins=bins).value_counts().sort_index()
                    labels = [f"{round(interval.left,2)} - {round(interval.right,2)}" for interval in data.index]
                    sizes = data.values
                colors = plt.get_cmap("Set2")(np.linspace(0, 1, len(labels)))
                fig2, ax2 = plt.subplots()
                ax2.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors)
                ax2.axis('equal')
                ax2.set_title(f"Pie Chart of {col}")
                st.pyplot(fig2)
            else:
                st.info("No numeric columns found for visualization.")
        except Exception as e:
            st.error(f"Error processing CSV: {e}")
    else:
        st.info("Please upload a CSV file for semi-supervised analysis.")

# =============================================================================
# Module 3: Unsupervised Module - Clustering Analysis
# =============================================================================
def unsupervised_module():
    st.title("Unsupervised Module - Clustering Analysis")
    st.markdown("Upload an unstructured CSV file to perform clustering analysis on a selected numeric column.")
    
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        try:
            df = pd.read_csv(file)
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
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
                    
                    st.markdown("**Scatter Plot of Clusters:**")
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
        st.info("Please upload a CSV file for clustering analysis.")

# =============================================================================
# Module 4: Stock Analysis Module - Stock Market Visualization
# =============================================================================
def stock_analysis_module():
    st.title("Stock Market Analysis Module")
    st.markdown("Upload CSV files containing stock data. Each file should have at least `Date` and `Close` columns.")
    
    files = st.file_uploader("Upload Stock Market Data (CSV)", type=["csv"], accept_multiple_files=True)
    aggregated_series = []
    if files:
        for idx, file in enumerate(files, start=1):
            st.markdown(f"### Stock Data File {idx}: {file.name}")
            try:
                df = pd.read_csv(file)
                st.subheader("Data Preview")
                st.dataframe(df.head())
                if "Date" in df.columns and "Close" in df.columns:
                    df["Date"] = pd.to_datetime(df["Date"])
                    df = df.sort_values("Date")
                    st.line_chart(df.set_index("Date")["Close"])
                    st.markdown("**Individual Stock Trend:**")
                    aggregated_series.append((file.name, df.set_index("Date")["Close"]))
                else:
                    st.info("CSV must contain 'Date' and 'Close' columns.")
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")
        if aggregated_series:
            st.subheader("Combined Stock Closing Prices")
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
        st.info("Upload at least one CSV file for stock market analysis.")

# =============================================================================
# Module 5: AI Loan Recommendation Module
# =============================================================================
education_loans = [
    {
        "name": "SBI Education Loan",
        "min_academic_score": 70,
        "min_credit_score": 750,
        "max_annual_income": 2000000,
        "description": "Offers competitive rates for higher studies in India and abroad.",
        "tenure": "15 years",
        "interest_rate": "7.5%"
    },
    {
        "name": "HDFC Education Loan",
        "min_academic_score": 75,
        "min_credit_score": 720,
        "max_annual_income": 1800000,
        "description": "Covers tuition fees and other expenses with attractive interest rates.",
        "tenure": "10-15 years",
        "interest_rate": "8.0%"
    },
    {
        "name": "Axis Bank Education Loan",
        "min_academic_score": 65,
        "min_credit_score": 700,
        "max_annual_income": 1500000,
        "description": "Quick approval process and broad coverage for educational expenses.",
        "tenure": "10 years",
        "interest_rate": "9.0%"
    },
    {
        "name": "PNB Education Loan",
        "min_academic_score": 60,
        "min_credit_score": 680,
        "max_annual_income": 1600000,
        "description": "Competitive rates with extensive support for educational financing.",
        "tenure": "10 years",
        "interest_rate": "10.0%"
    },
    {
        "name": "Canara Bank Education Loan",
        "min_academic_score": 70,
        "min_credit_score": 700,
        "max_annual_income": 1700000,
        "description": "Provides comprehensive financial support with flexible repayment options.",
        "tenure": "15 years",
        "interest_rate": "7.8%"
    }
]

def ai_loan_recommendation_module():
    st.title("AI Loan Recommendation Module")
    st.markdown("Enter your details to receive personalized education loan recommendations.")
    
    academic_score = st.number_input("Academic Score (0-100)", min_value=0, max_value=100, value=75)
    credit_score = st.number_input("Credit Score (300-850)", min_value=300, max_value=850, value=720)
    annual_income = st.number_input("Parent's Annual Income (INR)", min_value=0, value=1000000)
    marks_12 = st.number_input("12th Marks Percentage", min_value=0.0, max_value=100.0, value=80.0)
    ug_marks = st.number_input("Undergraduate Marks Percentage (Optional)", min_value=0.0, max_value=100.0, value=0.0)
    ug_marks_optional = st.checkbox("Provide Undergraduate Marks")
    
    past_loan_taken = st.radio("Have you taken any loan in the past?", ("No", "Yes"))
    past_loan_amount = 0.0
    emi_bounces = 0
    if past_loan_taken == "Yes":
        past_loan_amount = st.number_input("Enter Past Loan Amount (INR)", min_value=0.0, value=50000.0)
        emi_bounces = st.number_input("Number of EMI bounces", min_value=0, value=0)
    
    # Simple risk calculation
    risk = 0
    risk += (100 - academic_score) * 0.1
    risk += (850 - credit_score) * 0.05
    risk += (100 - marks_12) * 0.1
    if ug_marks_optional:
        risk += (100 - ug_marks) * 0.05
    if past_loan_taken == "Yes":
        risk += (past_loan_amount / 100000) * 0.2
        risk += emi_bounces * 5
    
    st.markdown(f"**Calculated Risk Score:** {risk:.2f}")
    
    # Loan recommendation logic
    recommended = []
    if risk < 20:
        recommended = [loan for loan in education_loans if loan["name"] in ["SBI Education Loan", "HDFC Education Loan", "Canara Bank Education Loan"]]
    elif 20 <= risk < 40:
        recommended = [loan for loan in education_loans if loan["name"] == "Axis Bank Education Loan"]
    else:
        recommended = [loan for loan in education_loans if loan["name"] == "PNB Education Loan"]
    
    if recommended:
        st.subheader("Recommended Education Loans")
        for loan in recommended:
            st.markdown(f"**{loan['name']}**")
            st.write(loan["description"])
            st.write(f"**Tenure:** {loan['tenure']}")
            st.write(f"**Interest Rate:** {loan['interest_rate']}")
    else:
        st.write("Based on your inputs, no education loans are recommended.")

# =============================================================================
# Main Application: Integrated BFSI OCR Project with Demo Email OTP
# =============================================================================
def main():
    # Run demo email OTP authentication (Demo Mode)
    demo_email_otp_authentication()
    
    # Render the header with fruit vibe styling
    st.markdown(
        f"""
        <div class="front-header">
            <h1 style="color: #333; margin: 0;">BFSI OCR of Bank Statement</h1>
            <p style="color: #555; font-size: 20px;">Experience a vibrant interface with {selected_fruit} vibes!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("This app integrates multiple functionalities: document analysis (OCR), semi-structured data analysis, clustering, stock market analysis, and AI-based education loan recommendations.")
    
    option = st.sidebar.selectbox("Select Module", 
                                  ["Supervised", "Semi-Supervised", "Unsupervised", "Stock Analysis", "AI Loan Recommendation"])
    
    if option == "Supervised":
        supervised_module()
    elif option == "Semi-Supervised":
        semi_supervised_module()
    elif option == "Unsupervised":
        unsupervised_module()
    elif option == "Stock Analysis":
        stock_analysis_module()
    elif option == "AI Loan Recommendation":
        ai_loan_recommendation_module()

if __name__ == "__main__":
    main()
