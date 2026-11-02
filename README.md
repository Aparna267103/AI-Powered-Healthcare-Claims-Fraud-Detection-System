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

## Dataset

**CMS DE-SynPUF – Medicare Claims Synthetic Public Use File**

Source: https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf/de10-sample-1

The project uses synthetic Medicare inpatient claims data.

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

The Power BI report has four pages. Pages 1–3 focus on individual analysis areas, and page 4 brings the report visuals together in one view. The complete interactive report is included in [`PowerBi_Report.pbix`](PowerBi_Report.pbix); download it and open it with Power BI Desktop to explore all four pages and use the filters.

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

1. Download synthetic Medicare claims data.
2. Load and preprocess the claims dataset using Python.
3. Aggregate claims at provider level.
4. Scale numerical features.
5. Train the Isolation Forest model.
6. Identify unusual providers.
7. Export provider anomaly results as CSV files.
8. Import the results into Power BI.
9. Build an interactive analytics dashboard.

## How to Run

Clone the repository:

```bash
git clone https://github.com/Aparna267103/Healthcare-Claims-Fraud-Detection.git
cd Healthcare-Claims-Fraud-Detection
```

The inpatient claims CSV must be in the repository root, alongside `provider_analysis.py`. The included sample CSV is already in this location.

```bash
pip install -r requirements.txt
python provider_analysis.py
```

Provider results are saved in the `outputs` folder, including `provider_anomaly_results.csv` and `flagged_providers.csv`.

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
