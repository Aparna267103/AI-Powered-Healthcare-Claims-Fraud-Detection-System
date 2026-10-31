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
- SQL (planned / additional analysis, if implemented)
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
- Anomaly score: Used to rank unusual provider patterns.
- Review status: Providers are classified as Review or Normal based on the model output.

## Power BI Dashboard

The dashboard contains three main sections:

### 1. Executive Risk Overview
- Total Claims
- Flagged Providers
- Total Providers
- Total Claim Payments
- Top 10 Providers by Claim Count
- Provider Review Status

### 2. Provider Investigation
- Provider-level claim details
- Average and maximum claim payments
- Anomaly scores
- Review queue
- Claim volume versus average payment analysis

### 3. Payment Patterns & Model Insights
- Claim Payment Distribution
- Monthly Claim Payments
- Most Unusual Provider Scores

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
git clone https://github.com/YOUR-USERNAME/healthcare-claims-fraud-detection.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the downloaded inpatient claims CSV in the expected data folder or update the file path in the Python script.

Run the Python script:

```bash
python provider_analysis.py
```

The generated output files will be saved in the outputs folder.

## Limitations

- The project uses synthetic Medicare data.
- Anomaly detection identifies unusual patterns, not confirmed fraud.
- Flagged providers require further investigation.
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

Aparna V
