import pandas as pd

INPUT  = "raw_alzheimers.csv"
OUTPUT = "alzheimers_cleaned.csv"

df = pd.read_csv(INPUT, dtype=str)
print(f"Dataset has {len(df)} rows, {len(df.columns)} columns")

columnsDict = { # Based off Data from https://data.cdc.gov/Healthy-Aging/Alzheimer-s-Disease-and-Healthy-Aging-Data/hfr9-rurv/data_preview
    "yearstart": "Year",
    "locationabbr": "State_Code",
    "locationdesc": "State",
    "class": "Category",
    "topic": "Topic",
    "question": "Question",
    "data_value_type": "Measure_Type",
    "data_value_unit":  "Unit",
    "data_value": "Value",
    "low_confidence_limit": "CI_Low",
    "high_confidence_limit":"CI_High",
    "stratificationcategory1": "Stratification_Category", # Age Group
    "stratification1": "Stratification", # Age
    "stratificationcategory2": "Stratification_Category2", # Race/Ethnicity Group
    "stratification2": "Stratification2", # Race/Ethnicity
}

df = df.rename(columns=columnsDict)
df = df[[col for col in columnsDict.values() if col in df.columns]]

print(f"After column selection: {list(df.columns)}")

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df["CI_Low"] = pd.to_numeric(df["CI_Low"], errors="coerce")
df["CI_High"] = pd.to_numeric(df["CI_High"], errors="coerce")

# Dropped empty rows of Value category
before = len(df)
df = df.dropna(subset=["Value"])
after  = len(df)
print(f"Dropped {before - after} rows with missing Value, {after} rows remaining.")

# Non-state need to be removed, as regions were categorized with abbreviations as well.
non_states = ["MDW", "NE", "STH", "WST", "US", "GU", "PR", "VI"]
df = df[~df["State_Code"].isin(non_states)]
print(f"Num rows after non-states removal: {len(df)} rows")

# ── Add a clean short question label (for Tableau tooltips / filters) ──────────

# Limit question column's length in response, for readability and fitting purposes.
df["Question_Short"] = df["Question"].str[:80] + "..."

print(df.head(5).to_string(index=False))

df.to_csv(OUTPUT, index=False)