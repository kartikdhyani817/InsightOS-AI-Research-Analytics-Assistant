# ==========================================================
# data_cleaner.py
# InsightOS AI Data Cleaning Assistant
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# MISSING VALUE RECOMMENDATIONS
# ==========================================================

def recommend_missing_value_strategy(df):

    recommendations = []

    for column in df.columns:

        missing = df[column].isnull().sum()

        if missing == 0:

            continue

        if pd.api.types.is_numeric_dtype(df[column]):

            recommendations.append({

                "Column": column,

                "Issue": f"{missing} missing values",

                "Recommendation": "Fill using Median"

            })

        else:

            recommendations.append({

                "Column": column,

                "Issue": f"{missing} missing values",

                "Recommendation": "Fill using Mode"

            })

    return pd.DataFrame(recommendations)


# ==========================================================
# DUPLICATE RECOMMENDATIONS
# ==========================================================

def recommend_duplicate_removal(df):

    duplicates = int(df.duplicated().sum())

    return {

        "Duplicate Rows": duplicates,

        "Recommendation":

            "Remove duplicate rows"

            if duplicates > 0

            else "No duplicates found"

    }


# ==========================================================
# EMPTY COLUMN RECOMMENDATIONS
# ==========================================================

def recommend_empty_column_removal(df):

    columns = []

    for column in df.columns:

        if df[column].isnull().all():

            columns.append(column)

    return columns


# ==========================================================
# CONSTANT COLUMN RECOMMENDATIONS
# ==========================================================

def recommend_constant_column_removal(df):

    columns = []

    for column in df.columns:

        if df[column].nunique(dropna=False) <= 1:

            columns.append(column)

    return columns


# ==========================================================
# DATE COLUMN DETECTION
# ==========================================================

def detect_date_columns(df):

    detected = []

    for column in df.columns:

        try:

            pd.to_datetime(

                df[column],

                errors="raise"

            )

            detected.append(column)

        except Exception:

            pass

    return detected


# ==========================================================
# CATEGORICAL COLUMN DETECTION
# ==========================================================

def detect_categorical_columns(df):

    columns = []

    for column in df.columns:

        if (

            df[column].dtype == "object"

            or

            str(df[column].dtype) == "category"

        ):

            columns.append(column)

    return columns


# ==========================================================
# AI CLEANING SUMMARY
# ==========================================================

def cleaning_summary(df):

    return {

        "Missing Value Suggestions":

            recommend_missing_value_strategy(df),

        "Duplicate Suggestions":

            recommend_duplicate_removal(df),

        "Empty Columns":

            recommend_empty_column_removal(df),

        "Constant Columns":

            recommend_constant_column_removal(df),

        "Date Columns":

            detect_date_columns(df),

        "Categorical Columns":

            detect_categorical_columns(df)

    }


# ==========================================================
# APPLY SAFE CLEANING
# ==========================================================

def apply_safe_cleaning(df):

    cleaned = df.copy()

    cleaned = cleaned.drop_duplicates()

    cleaned = cleaned.dropna(

        axis=1,

        how="all"

    )

    return cleaned