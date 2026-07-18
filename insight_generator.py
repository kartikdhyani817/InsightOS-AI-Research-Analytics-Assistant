# ==========================================================
# insight_generator.py
# InsightOS Enterprise Insight Generator
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def numeric_columns(df):

    return df.select_dtypes(include=np.number).columns.tolist()


# ==========================================================
# TOP METRIC
# ==========================================================

def top_metric(df):

    numeric = numeric_columns(df)

    if len(numeric) == 0:
        return None

    totals = df[numeric].sum()

    metric = totals.idxmax()

    return {

        "Metric": metric,

        "Value": round(float(totals.max()), 2)

    }


# ==========================================================
# LOWEST METRIC
# ==========================================================

def lowest_metric(df):

    numeric = numeric_columns(df)

    if len(numeric) == 0:
        return None

    totals = df[numeric].sum()

    metric = totals.idxmin()

    return {

        "Metric": metric,

        "Value": round(float(totals.min()), 2)

    }


# ==========================================================
# MISSING VALUE INSIGHT
# ==========================================================

def missing_value_insight(df):

    missing = int(df.isnull().sum().sum())

    if missing == 0:

        return "Dataset contains no missing values."

    return (

        f"Dataset contains {missing} missing values. "

        "Review before making business decisions."

    )


# ==========================================================
# DUPLICATE INSIGHT
# ==========================================================

def duplicate_insight(df):

    duplicates = int(df.duplicated().sum())

    if duplicates == 0:

        return "No duplicate records detected."

    return (

        f"{duplicates} duplicate rows detected. "

        "Cleaning is recommended."

    )


# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

def executive_insights(df):

    insights = []

    top = top_metric(df)

    if top:

        insights.append(

            f"'{top['Metric']}' is currently the strongest business metric "

            f"with a total value of {top['Value']:,.2f}."

        )

    low = lowest_metric(df)

    if low:

        insights.append(

            f"'{low['Metric']}' is the weakest metric "

            f"with a total value of {low['Value']:,.2f}."

        )

    insights.append(

        missing_value_insight(df)

    )

    insights.append(

        duplicate_insight(df)

    )

    return insights


# ==========================================================
# AI SUMMARY
# ==========================================================

def ai_summary(df):

    rows = len(df)

    cols = len(df.columns)

    numeric = len(

        numeric_columns(df)

    )

    return (

        f"The uploaded dataset contains "

        f"{rows:,} rows and "

        f"{cols} columns. "

        f"{numeric} numeric business metrics "

        f"were identified for analysis."

    )


# ==========================================================
# COMPLETE REPORT
# ==========================================================

def generate_insight_report(df):

    return {

        "Summary":

            ai_summary(df),

        "Insights":

            executive_insights(df)

    }