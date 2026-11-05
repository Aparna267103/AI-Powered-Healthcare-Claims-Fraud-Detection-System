
from pathlib import Path
import pandas as pd

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent

# Update this filename if your extracted CSV has a different name
file_path = BASE_DIR / (
    "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv"
)

if not file_path.exists():
    raise FileNotFoundError(
        f"Claims CSV not found: {file_path.name}. "
        "Check the filename and project folder."
    )

df = pd.read_csv(
    file_path,
    low_memory=False,
    dtype={"PRVDR_NUM": "string"},
)

print("Dataset shape:", df.shape)
print("\nAvailable columns:")
print(df.columns.tolist())

required = [
    "CLM_ID",
    "PRVDR_NUM",
    "CLM_PMT_AMT",
]

missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

df["CLM_PMT_AMT"] = pd.to_numeric(
    df["CLM_PMT_AMT"], errors="coerce"
)

# A claim record needs an ID, provider, and payment to be analyzed.
claims = df.dropna(
    subset=["CLM_ID", "PRVDR_NUM", "CLM_PMT_AMT"]
).copy()

if claims.empty:
    raise ValueError("No valid claims available for analysis.")

# Keep repeated IDs because some have different providers or payment values;
# the source does not establish which row, if any, should be discarded.
repeated_claims = claims[claims["CLM_ID"].duplicated(keep=False)]
repeated_claim_id_count = repeated_claims["CLM_ID"].nunique()

# Provider-level features
provider_summary = (
    claims.groupby("PRVDR_NUM")
    .agg(
        total_claims=("CLM_ID", "size"),
        total_claim_payments=("CLM_PMT_AMT", "sum"),
        avg_claim=("CLM_PMT_AMT", "mean"),
        max_claim=("CLM_PMT_AMT", "max"),
        std_claim=("CLM_PMT_AMT", "std"),
    )
    .reset_index()
)

provider_summary["std_claim"] = (
    provider_summary["std_claim"].fillna(0)
)

# Log transform reduces the effect of very large values
features = [
    "total_claims",
    "total_claim_payments",
    "avg_claim",
    "max_claim",
    "std_claim",
]

X = provider_summary[features].clip(lower=0)
X = np.log1p(X)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train anomaly detection model
model = IsolationForest(
    n_estimators=200,
    contamination=0.03,
    random_state=42
)

provider_summary["anomaly_label"] = model.fit_predict(
    X_scaled
)

provider_summary["anomaly_score"] = (
    model.decision_function(X_scaled)
)

# -1 means flagged for review; 1 means not flagged
provider_summary["review_status"] = np.where(
    provider_summary["anomaly_label"] == -1,
    "Review",
    "Normal"
)

# Save flagged providers, lowest scores first
flagged = (
    provider_summary[
        provider_summary["review_status"] == "Review"
    ]
    .sort_values("anomaly_score")
)

output_dir = BASE_DIR / "outputs"
output_dir.mkdir(exist_ok=True)

provider_summary.to_csv(
    output_dir / "provider_anomaly_results.csv",
    index=False
)

flagged.to_csv(
    output_dir / "flagged_providers.csv",
    index=False
)

print("\n========== ANOMALY DETECTION ==========")
print(
    "Repeated claim IDs:",
    repeated_claim_id_count,
    f"({len(repeated_claims)} rows retained)",
)
print("Total providers:", len(provider_summary))
print("Providers flagged for review:", len(flagged))

print("\nTop flagged providers:")
print(
    flagged[
        [
            "PRVDR_NUM",
            "total_claims",
            "total_claim_payments",
            "avg_claim",
            "anomaly_score",
        ]
    ].head(10).to_string(index=False)
)

print("\nSaved files:")
print(output_dir / "provider_anomaly_results.csv")
print(output_dir / "flagged_providers.csv")
