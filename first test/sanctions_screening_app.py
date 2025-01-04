import streamlit as st
import pandas as pd

# Load data
matched_customers = pd.read_csv("data/matched_customers.csv")

# Streamlit app
st.title("Sanctions Screening Dashboard")

threshold = st.slider("Match Threshold", 0, 100, 80)
filtered_matches = matched_customers[matched_customers["Match_Score"] >= threshold]

st.dataframe(filtered_matches)
st.write(f"Total Matches Above Threshold: {len(filtered_matches)}")
