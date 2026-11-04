# AI-Powered Healthcare Claims Fraud & Anomaly Detection System

## Project Overview

This project focuses on identifying unusual patterns in healthcare insurance claims using Machine Learning and data analytics.

The system analyzes synthetic Medicare claims data and identifies potentially unusual healthcare providers based on claim volume and payment patterns using the Isolation Forest algorithm.

The project combines Python, Scikit-learn, data analysis, and Power BI to build an end-to-end healthcare claims anomaly detection solution.

## Objectives

- Analyze healthcare insurance claims data.
- Identify unusual provider claim patterns.
- Detect potentially anomalous providers using Machine Learning.
- Generate provider-level risk results.
- Build an interactive Power BI dashboard for investigation and monitoring.

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Power BI
- Visual Studio Code
- Git and GitHub

## Datasets

**CMS DE-SynPUF – Medicare Claims Synthetic Public Use File**

Source: https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf/de10-sample-1

The repository includes two different sample CSV files from this synthetic dataset:

- **Beneficiary-level analysis (`main.py`):** Download the Medicare Beneficiary Summary File sample CSV, `DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv`, from the CMS source above and place it in the repository root.
- **Provider-level analysis (`provider_analysis.py`):** Download the Medicare Inpatient Claims sample CSV, `DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv`, from the CMS source above and place it in the repository root.

The included sample CSV files are already in the repository root. If you replace either file, keep the exact filename shown above. These datasets have different rows and columns and are not interchangeable; each script requires its corresponding file.

## Machine Learning Approach

**Algorithm:** Isolation Forest

The model identifies unusual provider-level patterns using features such as:

- Total number of claims
- Total claim payments
- Average claim payment
- Maximum claim payment
- Standard deviation of claim payments

### Model Output

- Anomaly label: -1 indicates an anomaly; 1 indicates normal.
- Anomaly score: Lower scores indicate more unusual provider patterns. Flagged providers are sorted from the lowest score (most unusual) upward; negative scores indicate an anomaly with the current model configuration.
- Review status: Providers are classified as Review or Normal based on the model output.
- `total_claim_payments` is the sum of claim payment amounts (`CLM_PMT_AMT`), not billed charges.
- The `contamination` parameter is set to `0.03` as a modeling assumption. It controls the expected proportion of outliers identified by the algorithm and does not represent the actual fraud rate.

## Power BI Dashboard

The Power BI report has three pages, each focused on a different area of claims analysis. The complete interactive report is included in [`PowerBi_Report.pbix`](PowerBi_Report.pbix); download it and open it with Power BI Desktop to explore the pages and use the filters.

### Page 1 — Executive Risk Overview
- Summary cards for total claims, flagged providers, total providers, total claim payments, and provider risk rate.
- Top 10 providers by claim count.
- Provider review status distribution.

![Executive Risk Overview dashboard page](screenshots/Executive%20Risk%20Overview.png)

### Page 2 — Provider Investigation
- Provider claim details, including claim counts, payment amounts, anomaly scores, and review status.
- Provider claim volume versus average payment analysis.
- Filters and summary metrics to support provider-level investigation.

![Provider Investigation dashboard page](screenshots/Provider%20Investigation.png)

### Page 3 — Payment Patterns & Model Insights
- Claim payment distribution.
- Monthly claim payment trend from 2008 to 2010.
- Top 10 most unusual providers by anomaly score.

![Payment Patterns & Model Insights dashboard page](screenshots/Payment%20Patterns%20%26%20Model%20Insights.png)

## Project Workflow

The beneficiary-level and provider-level scripts are separate analyses:

- `main.py` analyzes beneficiary-summary records and writes beneficiary-level results and charts to `outputs`.
- `provider_analysis.py` analyzes inpatient claims aggregated by provider and writes provider-level results to `outputs`. The Power BI dashboard uses this script's output, including `provider_anomaly_results.csv` and `flagged_providers.csv`; the beneficiary-level output from `main.py` is not the dashboard's provider dataset.

## How to Run

Clone the repository:

```bash
git clone https://github.com/Aparna267103/AI-Powered-Healthcare-Claims-Fraud-Detection-System.git
cd AI-Powered-Healthcare-Claims-Fraud-Detection-System
```

Install dependencies once:

```bash
pip install -r requirements.txt
```

### Beneficiary-level analysis

Ensure `DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv` is in the repository root, alongside `main.py`. The included sample CSV is already in this location.

```bash
python main.py
```

This writes beneficiary-level results and visualizations to `outputs`, including `beneficiary_anomaly_results.csv` and `anomalies_for_review.csv`.

### Provider-level analysis and Power BI

Ensure `DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv` is in the repository root, alongside `provider_analysis.py`. The included sample CSV is already in this location.

```bash
python provider_analysis.py
```

Provider-level results are saved in `outputs`, including `provider_anomaly_results.csv` and `flagged_providers.csv`. These are the provider analysis outputs used by the Power BI dashboard.

## Limitations

- The project uses synthetic Medicare data.
- Anomaly detection identifies unusual patterns, not confirmed fraud. Results are providers flagged for further review.
- Model results depend on the selected features and contamination parameter.

## Future Enhancements

- Add more advanced anomaly detection algorithms.
- Integrate SQL-based analytics.
- Improve model evaluation and comparison.
- Add provider-level drill-through in Power BI.
- Develop a more advanced risk scoring framework.

## Disclaimer

This is an educational portfolio project using synthetic healthcare claims data. The model output should not be interpreted as evidence of actual healthcare fraud.

## Author

Created as a Data Analytics and Machine Learning portfolio project.
