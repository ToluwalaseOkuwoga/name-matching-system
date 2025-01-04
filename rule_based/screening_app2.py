import streamlit as st
import pandas as pd
import random
from faker import Faker
from rapidfuzz import process, fuzz
import re

# Step 1: Generate Large Datasets
def generate_large_datasets(num_customers, num_sanctioned):
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    # Generate customer data
    customers = []
    for _ in range(num_customers):
        name = fake.name()
        nationality = fake.country()
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=70)
        customers.append({"Name": name, "Nationality": nationality, "Birthdate": birthdate})

    customers_df = pd.DataFrame(customers)

    # Generate sanctioned data with variations
    sanctioned = []
    for _ in range(num_sanctioned):
        name = fake.name()
        variations = [
            name,
            name.lower(),
            ''.join(random.sample(name, len(name))),  # Scrambled name
            name.replace("a", "@"),  # Typo
            name + " Jr.",  # Alias
        ]
        sanctioned.append({"Sanctioned_Name": random.choice(variations), "Sanctioned_Nationality": fake.country()})

    sanctioned_df = pd.DataFrame(sanctioned)

    # Save to CSV
    customers_df.to_csv("customers_data.csv", index=False)
    sanctioned_df.to_csv("sanctioned_data.csv", index=False)

    return customers_df, sanctioned_df

# Step 2: Preprocessing and Loading Data
@st.cache(allow_output_mutation=True)
def load_data():
    customers_df = pd.read_csv("customers_data.csv")
    sanctioned_df = pd.read_csv("sanctioned_data.csv")

    # Preprocess names
    customers_df["Preprocessed_Name"] = customers_df["Name"].apply(preprocess_name)
    sanctioned_df["Preprocessed_Sanctioned_Name"] = sanctioned_df["Sanctioned_Name"].apply(preprocess_name)

    return customers_df, sanctioned_df

def preprocess_name(name):
    return re.sub(r"[^a-zA-Z\s]", "", name).lower().strip()

# Step 3: Fuzzy Matching Function
def match_name(customer_name, sanctioned_list, threshold=85):
    match, score, _ = process.extractOne(customer_name, sanctioned_list, scorer=fuzz.ratio)
    if score >= threshold:
        return match, score
    return None, 0

# Step 4: Contextual Matching
def contextual_filter(row, sanctioned_df):
    sanctioned_entry = sanctioned_df[sanctioned_df["Preprocessed_Sanctioned_Name"] == row["Matched_Name"]]
    if not sanctioned_entry.empty and row["Nationality"] == sanctioned_entry.iloc[0]["Sanctioned_Nationality"]:
        return 1
    return 0

# Step 5: Main Logic for Matching
def compute_filtered_matches(customers_df, sanctioned_df, threshold):
    sanctioned_list = sanctioned_df["Preprocessed_Sanctioned_Name"].tolist()
    customers_df["Matched_Name"], customers_df["Match_Score"] = zip(
        *customers_df["Preprocessed_Name"].apply(lambda x: match_name(x, sanctioned_list, threshold))
    )

    customers_df["Contextual_Match"] = customers_df.apply(lambda row: contextual_filter(row, sanctioned_df), axis=1)
    filtered_matches = customers_df[customers_df["Contextual_Match"] == 1]

    filtered_matches.to_csv("filtered_matches.csv", index=False)
    return filtered_matches

# Step 6: Streamlit Dashboard
st.title("Sanctions Screening Dashboard")

# Generate datasets if not already created
if "customers_data.csv" not in locals() or "sanctioned_data.csv" not in locals():
    generate_large_datasets(10000, 2000)  # Generate large datasets

# Threshold slider
threshold = st.slider("Match Threshold", 0, 100, 85)

# Load and process data
customers_df, sanctioned_df = load_data()
filtered_matches = compute_filtered_matches(customers_df, sanctioned_df, threshold)

# Display results
st.dataframe(filtered_matches)
st.write(f"Total Matches After Contextual Filtering: {len(filtered_matches)}")
