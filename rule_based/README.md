# Rule-Based Name Matching System

This folder contains the implementation of a **rule-based system** for name matching, specifically designed for sanctions screening.

---

## Overview

The rule-based system works in the following steps:

### Data Generation
- Synthetic datasets for customers and sanctioned names are generated using the `Faker` library.
- The datasets include attributes like names, nationalities, and birthdates.

### Data Preprocessing
- Names are preprocessed by removing special characters, converting to lowercase, and stripping whitespace.
- Preprocessed names are used for efficient and consistent matching.

### Fuzzy Matching
- The `rapidfuzz` library is used for text similarity scoring.
- Customer names are compared against sanctioned names with a customizable threshold for matching.

### Contextual Filtering
- Contextual rules, such as matching based on nationality, are applied to reduce false positives.

### Streamlit Dashboard
- A Streamlit app is provided for interactive exploration of the results.
- Users can adjust the matching threshold dynamically and view the filtered matches.

---

## File Descriptions

- **`sanctions_screening_app.py`**:
  - The main script that integrates all functionalities, including data generation, preprocessing, matching, and dashboard creation.

- **`customers_data.csv`**:
  - A synthetic dataset containing customer names, nationalities, and birthdates.

- **`sanctioned_data.csv`**:
  - A synthetic dataset of sanctioned names with variations such as aliases, misspellings, and scrambled names.

- **`filtered_matches.csv`**:
  - The results of the rule-based matching process after applying contextual filters.

---

## Key Features

### Customizable Matching Threshold
- Users can adjust the threshold for fuzzy matching through the Streamlit dashboard.

### Contextual Rules
- Filters based on additional attributes like nationality to improve precision.

### Interactive Dashboard
- A visual interface for exploring results and fine-tuning parameters.

---

## How to Run

### Install Required Libraries
Run the following command to install the necessary libraries:
```bash
pip install streamlit pandas rapidfuzz faker
```

### Run the Streamlit App
Execute the following command to launch the app:
```bash
streamlit run sanctions_screening_app.py
```

### Explore Results
- Adjust the threshold slider in the dashboard to explore different matching results.
