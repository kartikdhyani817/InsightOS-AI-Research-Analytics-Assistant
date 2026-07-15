# ==========================================================
# business_summary.py
# InsightOS Executive Business Summary Generator
# ==========================================================

import pandas as pd


# ==========================================================
# DATASET OVERVIEW
# ==========================================================

def dataset_overview(df):

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Missing Values": int(df.isnull().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum())

    }


# ==========================================================
# NUMERIC SUMMARY
# ==========================================================

def numeric_highlights(df):

    numeric = df.select_dtypes(include="number")

    highlights = []

    for column in numeric.columns:

        highlights.append({

            "Column": column,

            "Average": round(float(numeric[column].mean()), 2),

            "Maximum": round(float(numeric[column].max()), 2),

            "Minimum": round(float(numeric[column].min()), 2)

        })

    return highlights


# ==========================================================
# KEY FINDINGS
# ==========================================================

def key_findings(df):

    findings = []

    overview = dataset_overview(df)

    findings.append(

        f"The dataset contains {overview['Rows']} rows and {overview['Columns']} columns."

    )

    if overview["Missing Values"] > 0:

        findings.append(

            f"There are {overview['Missing Values']} missing values that should be reviewed."

        )

    else:

        findings.append(

            "No missing values were detected."

        )

    if overview["Duplicate Rows"] > 0:

        findings.append(

            f"{overview['Duplicate Rows']} duplicate rows were identified."

        )

    else:

        findings.append(

            "No duplicate rows were found."

        )

    return findings


# ==========================================================
# OPPORTUNITIES
# ==========================================================

def opportunities(df):

    opportunities = [

        "Use dashboard KPIs to monitor business performance.",

        "Track high-value metrics regularly.",

        "Create automated reports for decision-makers.",

        "Monitor trends to identify growth opportunities."

    ]

    return opportunities


# ==========================================================
# RISKS
# ==========================================================

def risks(df):

    risk_list = []

    missing = int(df.isnull().sum().sum())

    duplicates = int(df.duplicated().sum())

    if missing > 0:

        risk_list.append(

            "Missing values may reduce analysis accuracy."

        )

    if duplicates > 0:

        risk_list.append(

            "Duplicate records may distort business metrics."

        )

    if len(risk_list) == 0:

        risk_list.append(

            "No significant data-quality risks detected."

        )

    return risk_list


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

def recommendations(df):

    recommendations = [

        "Validate the dataset before business reporting.",

        "Review missing values and outliers.",

        "Track KPIs through interactive dashboards.",

        "Use AI-generated insights for executive reporting."

    ]

    return recommendations


# ==========================================================
# NEXT STEPS
# ==========================================================

def next_steps(df):

    return [

        "Monitor KPIs regularly.",

        "Automate dashboard refreshes.",

        "Schedule executive reports.",

        "Expand predictive analytics using machine learning."

    ]


# ==========================================================
# COMPLETE BUSINESS SUMMARY
# ==========================================================

def generate_business_summary(df):

    return {

        "Overview": dataset_overview(df),

        "Highlights": numeric_highlights(df),

        "Key Findings": key_findings(df),

        "Opportunities": opportunities(df),

        "Risks": risks(df),

        "Recommendations": recommendations(df),

        "Next Steps": next_steps(df)

    }