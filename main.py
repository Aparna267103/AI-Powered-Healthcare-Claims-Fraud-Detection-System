from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# 1. FILE PATHS
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------
if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"CSV file not found: {DATA_FILE}\n"
        "Place the CSV in the same folder as main.py."
    )

df = pd.read_csv(DATA_FILE)

print("\n========== DATA LOADED ==========")
print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\n========== COLUMN INFORMATION ==========")
df.info()

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())


# --------------------------------------------------
# 3. BASIC DATA CLEANING
# --------------------------------------------------
df = df.drop_duplicates().copy()

# Convert invalid numeric values to NaN if any
amount_columns = [
    "MEDREIMB_IP",
    "MEDREIMB_OP",
    "MEDREIMB_CAR",
    "BENRES_IP",
    "BENRES_OP",
    "BENRES_CAR",
    "PPPYMT_IP",
    "PPPYMT_OP",
    "PPPYMT_CAR",
]

for col in amount_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Missing death date is retained:
# it may mean no death date was recorded.
print("\nRows after removing duplicates:", len(df))


# --------------------------------------------------
# 4. FEATURE ENGINEERING
# --------------------------------------------------
reimbursement_columns = [
    "MEDREIMB_IP",
    "MEDREIMB_OP",
    "MEDREIMB_CAR",
]

for col in reimbursement_columns:
    if col not in df.columns:
        raise ValueError(f"Required column missing: {col}")

df["Total_Reimbursement"] = (
    df[reimbursement_columns].fillna(0).sum(axis=1)
)

df["Total_Beneficiary_Responsibility"] = (
    df[["BENRES_IP", "BENRES_OP", "BENRES_CAR"]]
    .fillna(0)
    .sum(axis=1)
)

df["Total_Primary_Payer_Amount"] = (
    df[["PPPYMT_IP", "PPPYMT_OP", "PPPYMT_CAR"]]
    .fillna(0)
    .sum(axis=1)
)

print("\n========== REIMBURSEMENT SUMMARY ==========")
print(df["Total_Reimbursement"].describe())


# --------------------------------------------------
# 5. SAVE CLEANED DATA
# --------------------------------------------------
df.to_csv(OUTPUT_DIR / "cleaned_beneficiary_data.csv", index=False)
print("\nSaved cleaned data.")


# --------------------------------------------------
# 6. EXPLORATORY DATA ANALYSIS (EDA)
# --------------------------------------------------
print("\n========== TOP 10 BENEFICIARIES BY REIMBURSEMENT ==========")

top_beneficiaries = (
    df[["DESYNPUF_ID", "Total_Reimbursement"]]
    .sort_values("Total_Reimbursement", ascending=False)
    .head(10)
)

print(top_beneficiaries.to_string(index=False))
top_beneficiaries.to_csv(
    OUTPUT_DIR / "top_10_beneficiaries.csv", index=False
)

print("\n========== SEX CODE COUNTS ==========")
print(df["BENE_SEX_IDENT_CD"].value_counts(dropna=False))

print("\n========== RACE CODE COUNTS ==========")
print(df["BENE_RACE_CD"].value_counts(dropna=False))


# --------------------------------------------------
# 7. VISUALIZATIONS
# --------------------------------------------------
sns.set_theme()

plt.figure(figsize=(9, 5))
sns.histplot(df["Total_Reimbursement"], bins=50)
plt.title("Distribution of Total Medicare Reimbursement")
plt.xlabel("Total reimbursement")
plt.ylabel("Number of beneficiaries")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "reimbursement_distribution.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.boxplot(x=df["Total_Reimbursement"])
plt.title("Reimbursement Amount Boxplot")
plt.xlabel("Total reimbursement")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "reimbursement_boxplot.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="BENE_SEX_IDENT_CD")
plt.title("Beneficiary Count by Sex Code")
plt.xlabel("Sex code")
plt.ylabel("Number of beneficiaries")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "beneficiary_sex_counts.png")
plt.close()

print("\nSaved charts in outputs folder.")


# --------------------------------------------------
# 8. ANOMALY DETECTION
# --------------------------------------------------
# Use reimbursement and beneficiary-responsibility features.
# An anomaly is unusual, NOT proof of fraud.

features = [
    "MEDREIMB_IP",
    "MEDREIMB_OP",
    "MEDREIMB_CAR",
    "BENRES_IP",
    "BENRES_OP",
    "BENRES_CAR",
]

model_data = df[features].copy()
model_data = model_data.replace([np.inf, -np.inf], np.nan)
model_data = model_data.fillna(model_data.median()).fillna(0)

scaler = StandardScaler()
scaled_features = scaler.fit_transform(model_data)

model = IsolationForest(
    n_estimators=100,
    contamination=0.02,
    random_state=42
)

predictions = model.fit_predict(scaled_features)

df["Anomaly_Flag"] = np.where(predictions == -1, "Review", "Normal")
df["Anomaly_Score"] = model.decision_function(scaled_features)

anomalies = (
    df[df["Anomaly_Flag"] == "Review"]
    .sort_values("Anomaly_Score")
)

print("\n========== ANOMALY DETECTION RESULTS ==========")
print("Total beneficiaries:", len(df))
print("Flagged for review:", len(anomalies))

print("\nTop 10 unusual reimbursement records:")
print(
    anomalies[
        ["DESYNPUF_ID", "Total_Reimbursement", "Anomaly_Score"]
    ].head(10).to_string(index=False)
)

anomalies.to_csv(OUTPUT_DIR / "anomalies_for_review.csv", index=False)

# Save full results too
df.to_csv(OUTPUT_DIR / "beneficiary_anomaly_results.csv", index=False)


# --------------------------------------------------
# 9. FINAL SUMMARY
# --------------------------------------------------
print("\n========== PROJECT COMPLETED ==========")
print("Total records analysed:", len(df))
print("Total reimbursement:", round(df["Total_Reimbursement"].sum(), 2))
print("Mean reimbursement:", round(df["Total_Reimbursement"].mean(), 2))
print("Flagged for review:", len(anomalies))
print("Output folder:", OUTPUT_DIR)
