# ==========================================================
# dashboard_builder.py
# InsightOS Smart Dashboard Builder
# ==========================================================

import pandas as pd


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def get_numeric_columns(df):

    return df.select_dtypes(

        include="number"

    ).columns.tolist()


# ==========================================================
# CATEGORICAL COLUMNS
# ==========================================================

def get_categorical_columns(df):

    return df.select_dtypes(

        exclude="number"

    ).columns.tolist()


# ==========================================================
# DATE COLUMNS
# ==========================================================

def get_date_columns(df):

    date_columns = []

    for column in df.columns:

        try:

            pd.to_datetime(df[column])

            date_columns.append(column)

        except Exception:

            pass

    return date_columns


# ==========================================================
# KPI BUILDER
# ==========================================================

def generate_kpis(df):

    numeric = get_numeric_columns(df)

    kpis = []

    for column in numeric:

        kpis.append({

            "Column": column,

            "Sum": round(df[column].sum(), 2),

            "Average": round(df[column].mean(), 2),

            "Maximum": round(df[column].max(), 2),

            "Minimum": round(df[column].min(), 2)

        })

    return kpis


# ==========================================================
# CHART RECOMMENDATION
# ==========================================================

def recommend_charts(df):

    charts = []

    numeric = get_numeric_columns(df)

    categorical = get_categorical_columns(df)

    dates = get_date_columns(df)

    if len(numeric) >= 1:
        charts.append("Histogram")

        charts.append("Box Plot")

    if len(numeric) >= 2:
        charts.append("Scatter Plot")

        charts.append("Correlation Heatmap")

    if len(categorical) >= 1:
        charts.append("Bar Chart")

        charts.append("Pie Chart")

    if len(dates) >= 1 and len(numeric) >= 1:
        charts.append("Line Chart")

    return charts


# ==========================================================
# DATASET HEALTH
# ==========================================================

def dataset_health(df):

    rows = len(df)

    columns = len(df.columns)

    missing = int(df.isnull().sum().sum())

    duplicates = int(df.duplicated().sum())

    score = 100

    if rows > 0:

        score -= (missing / (rows * columns)) * 100

        score -= (duplicates / rows) * 10

    score = max(

        0,

        min(

            100,

            round(score)

        )

    )

    return {

        "Rows": rows,

        "Columns": columns,

        "Missing Values": missing,

        "Duplicate Rows": duplicates,

        "Health Score": score

    }


# ==========================================================
# AUTO DASHBOARD
# ==========================================================

def build_dashboard(df):

    dashboard = {

        "health": dataset_health(df),

        "kpis": generate_kpis(df),

        "recommended_charts": recommend_charts(df)

    }

    return dashboard