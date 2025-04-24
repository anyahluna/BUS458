import streamlit as st
import pandas as pd
import joblib

# Load trained model pipeline
model = joblib.load("salary2025_model.joblib")

# App title
st.title("💼 Data Science Salary Predictor")
st.subheader("📈 Estimate your expected salary based on your profile")

# Input fields
country = st.selectbox("🌍 Country", ["United States", "India", "Canada", "United Kingdom", "Other"])
education = st.selectbox("🎓 Highest Education Level", [
    "No formal education past high school",
    "Some college/university without degree",
    "Bachelor's degree",
    "Master's degree",
    "Doctoral degree",
    "Professional doctorate"
])
years_coding = st.slider("💻 Years of Coding Experience", 0, 40, 2)
age = st.slider("🎂 Your Age", 18, 75, 25)
company_size = st.selectbox("🏢 Company Size", [
    "0-49 employees", "50-249 employees", "250-999 employees",
    "1000-9,999 employees", "10,000 or more employees"
])
ml_exp = st.slider("📊 ML Experience (years)", 0, 30, 1)
ml_spend = st.selectbox("💸 ML/Cloud Spend (last 5 years)", [
    "$0", "$1-$99", "$100-$999", "$1000-$9,999",
    "$10,000-$99,999", "$100,000 or more"
])

# Mapping inputs
education_map = {
    "No formal education past high school": 0,
    "Some college/university without degree": 1,
    "Bachelor's degree": 2,
    "Master's degree": 3,
    "Doctoral degree": 4,
    "Professional doctorate": 5
}

company_map = {
    "0-49 employees": 0,
    "50-249 employees": 1,
    "250-999 employees": 2,
    "1000-9,999 employees": 3,
    "10,000 or more employees": 4
}

ml_spend_map = {
    "$0": 0, "$1-$99": 50, "$100-$999": 550,
    "$1000-$9,999": 5500, "$10,000-$99,999": 55000,
    "$100,000 or more": 100000
}

# Build base input DataFrame
input_df = pd.DataFrame([{
    "Country_clean": country,
    "Education_ord": education_map[education],
    "YearsCode_num": years_coding,
    "Age_mid": age,
    "CompanySize_ord": company_map[company_size],
    "ML_Experience_yrs": ml_exp,
    "ML_Spend_5yr": ml_spend_map[ml_spend]
}])

# Add required dummy columns the model expects, set to 0
expected_dummy_cols = [
    'JobFunction_0', 'JobFunction_1-2', 'JobFunction_3-4', 'JobFunction_5-9',
    'JobFunction_10-14', 'JobFunction_15-19', 'JobFunction_20+',
    'JobTitle_$0 ($USD)', 'JobTitle_$1-$99', 'JobTitle_$100-$999',
    'JobTitle_$1000-$9,999', 'JobTitle_$10,000-$99,999',
    'JobTitle_$100,000 or more ($USD)'
]
for col in expected_dummy_cols:
    input_df[col] = 0

# Predict
if st.button("💵 Predict Salary"):
    prediction = model.predict(input_df)[0]
    st.success(f"💰 Estimated Salary: ${prediction:,.0f}")

st.markdown("---")