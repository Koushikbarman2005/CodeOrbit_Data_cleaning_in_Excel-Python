"""
Data Cleaning Script — Titanic-style Passenger Sample
======================================================
Input : titanic_raw_messy.csv   (raw, messy sample dataset)
Output: titanic_cleaned.csv     (cleaned dataset)
        cleaning_log.txt        (step-by-step log of what was done and why)

Each step below is numbered and printed to the log so the process is
fully traceable / reproducible.
"""
import pandas as pd
import numpy as np

log_lines = []
def log(msg):
    print(msg)
    log_lines.append(msg)

df = pd.read_csv("titanic_raw_messy.csv")
log(f"STEP 0 — Loaded raw data: {df.shape[0]} rows, {df.shape[1]} columns")
log(f"Original columns: {list(df.columns)}\n")

# -----------------------------------------------------------------
# STEP 1: Standardize column names (strip whitespace, lowercase, snake_case)
# -----------------------------------------------------------------
before_cols = list(df.columns)
df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(" ", "_")
)
log("STEP 1 — Standardized column names")
log(f"  Before: {before_cols}")
log(f"  After : {list(df.columns)}\n")

# -----------------------------------------------------------------
# STEP 2: Remove exact duplicate rows
# -----------------------------------------------------------------
n_before = len(df)
dupes = df.duplicated().sum()
df = df.drop_duplicates()
log("STEP 2 — Removed exact duplicate rows")
log(f"  Duplicate rows found & removed: {dupes}")
log(f"  Row count: {n_before} -> {len(df)}\n")

# -----------------------------------------------------------------
# STEP 3: Remove duplicate passenger IDs re-keyed with different name casing
# (same passenger entered twice under a different PassengerId)
# -----------------------------------------------------------------
n_before = len(df)
df["name_key"] = df["name"].str.strip().str.upper()
df = df.drop_duplicates(subset=["name_key"], keep="first")
df = df.drop(columns=["name_key"])
log("STEP 3 — Removed re-keyed duplicate passengers (same name, different ID)")
log(f"  Row count: {n_before} -> {len(df)}\n")

# -----------------------------------------------------------------
# STEP 4: Clean 'name' formatting (trim whitespace, consistent Title Case)
# -----------------------------------------------------------------
df["name"] = df["name"].str.strip().str.title()
log("STEP 4 — Cleaned 'name' formatting")
log("  Trimmed extra whitespace and standardized to Title Case\n")

# -----------------------------------------------------------------
# STEP 5: Standardize 'sex' values to lowercase {male, female}
# -----------------------------------------------------------------
before_vals = df["sex"].unique().tolist()
df["sex"] = df["sex"].str.strip().str.lower()
log("STEP 5 — Standardized 'sex' values")
log(f"  Distinct values before: {before_vals}")
log(f"  Distinct values after : {df['sex'].unique().tolist()}\n")

# -----------------------------------------------------------------
# STEP 6: Standardize 'embarked' to single-letter port codes {S, C, Q}
# and fill missing values with the most frequent port (mode imputation)
# -----------------------------------------------------------------
before_vals = df["embarked"].unique().tolist()
port_map = {
    "southampton": "S", "cherbourg": "C", "queenstown": "Q",
    "s": "S", "c": "C", "q": "Q",
}
df["embarked"] = df["embarked"].str.strip().str.lower().map(port_map)
missing_embarked = df["embarked"].isnull().sum()
mode_port = df["embarked"].mode()[0]
df["embarked"] = df["embarked"].fillna(mode_port)
log("STEP 6 — Standardized 'embarked' to port codes (S/C/Q)")
log(f"  Distinct values before: {before_vals}")
log(f"  Missing values filled with most frequent port ('{mode_port}'): {missing_embarked}\n")

# -----------------------------------------------------------------
# STEP 7: Clean 'fare' — strip currency symbols, convert to numeric,
# fill missing values with the median fare for that passenger class
# -----------------------------------------------------------------
df["fare"] = (
    df["fare"].astype(str)
              .str.replace("$", "", regex=False)
              .str.strip()
)
df["fare"] = pd.to_numeric(df["fare"], errors="coerce")
missing_fare_before = df["fare"].isnull().sum()
df["fare"] = df.groupby("pclass")["fare"].transform(lambda x: x.fillna(x.median()))
df["fare"] = df["fare"].round(2)
log("STEP 7 — Cleaned 'fare' column")
log("  Removed '$' symbols and converted to numeric")
log(f"  Missing fares filled with median fare of matching Pclass: {missing_fare_before}\n")

# -----------------------------------------------------------------
# STEP 8: Handle missing 'age' — impute with median age per (sex, pclass) group
# -----------------------------------------------------------------
missing_age_before = df["age"].isnull().sum()
df["age"] = df.groupby(["sex", "pclass"])["age"].transform(lambda x: x.fillna(x.median()))
df["age"] = df["age"].round(1)
log("STEP 8 — Imputed missing 'age' values")
log(f"  Missing ages filled with median age of matching (sex, pclass) group: {missing_age_before}\n")

# -----------------------------------------------------------------
# STEP 9: Handle 'cabin' — mostly missing (expected for this data), so
# flag rather than impute a fake cabin number
# -----------------------------------------------------------------
missing_cabin = df["cabin"].isnull().sum()
df["cabin_known"] = df["cabin"].notnull()
df["cabin"] = df["cabin"].fillna("Unknown")
log("STEP 9 — Handled 'cabin' column")
log(f"  {missing_cabin} missing cabin values -> labeled 'Unknown'")
log("  Added boolean flag 'cabin_known' rather than fabricating cabin numbers\n")

# -----------------------------------------------------------------
# STEP 10: Enforce data types
# -----------------------------------------------------------------
df["passenger_id"] = df["passenger_id"].astype(int)
df["pclass"] = df["pclass"].astype(int)
df["survived"] = df["survived"].astype(int)
df["age"] = df["age"].astype(float)
df["fare"] = df["fare"].astype(float)
log("STEP 10 — Enforced consistent data types (int/float) on numeric columns\n")

# -----------------------------------------------------------------
# STEP 11: Reset index and reorder columns for a clean, organized presentation
# -----------------------------------------------------------------
col_order = ["passenger_id", "name", "sex", "age", "pclass", "survived",
             "fare", "embarked", "cabin", "cabin_known"]
df = df[col_order].sort_values("passenger_id").reset_index(drop=True)
log("STEP 11 — Reordered columns and sorted by passenger_id for final presentation\n")

# -----------------------------------------------------------------
# Save outputs
# -----------------------------------------------------------------
df.to_csv("titanic_cleaned.csv", index=False)
log(f"FINAL — Cleaned dataset saved: titanic_cleaned.csv ({df.shape[0]} rows, {df.shape[1]} columns)")
log(f"Remaining missing values:\n{df.isnull().sum().to_string()}")

with open("cleaning_log.txt", "w") as f:
    f.write("\n".join(log_lines))

print("\nDone. See cleaning_log.txt for the full documented log.")
