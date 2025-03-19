import streamlit as st

# Predefined education loan schemes with additional details
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
    st.title("AI Loan Recommendation")
    st.markdown("Enter your details to get personalized education loan recommendations.")
    
    academic_score = st.number_input("Academic Score (0-100)", min_value=0, max_value=100, value=75)
    credit_score = st.number_input("Credit Score (300-850)", min_value=300, max_value=850, value=720)
    annual_income = st.number_input("Parent's Annual Income (INR)", min_value=0, value=1000000)
    marks_12 = st.number_input("12th Marks Percentage", min_value=0.0, max_value=100.0, value=80.0)
    ug_marks = st.number_input("Undergraduate Marks Percentage (Optional)", min_value=0.0, max_value=100.0, value=0.0)
    ug_marks_optional = st.checkbox("I want to provide Undergraduate Marks")
    
    past_loan_taken = st.radio("Have you taken any loan in the past?", ("No", "Yes"))
    past_loan_amount = 0.0
    emi_bounces = 0
    if past_loan_taken == "Yes":
        past_loan_amount = st.number_input("Enter the Past Loan Amount (INR)", min_value=0.0, value=50000.0)
        emi_bounces = st.number_input("Number of EMI bounces", min_value=0, value=0)
    
    # Simple risk calculation (adjust weights/thresholds as needed)
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
    
    # Loan recommendation logic based on risk thresholds
    recommended = []
    if risk < 20:
        recommended = [loan for loan in education_loans if loan["name"] in 
                       ["SBI Education Loan", "HDFC Education Loan", "Canara Bank Education Loan"]]
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

def main():
    ai_loan_recommendation_module()

if __name__ == "__main__":
    main()
