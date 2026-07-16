# ==========================================================
# data_quality.py
# InsightOS Enterprise Data Quality Analyzer
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# BASIC INFORMATION
# ==========================================================

def dataset_information(df):

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Memory (MB)": round(

            df.memory_usage(deep=True).sum()

            / (1024 * 1024),

            2

        )

    }


# ==========================================================
# MISSING VALUES
# ==========================================================

def missing_values(df):

    missing = df.isnull().sum()

    percent = (

        df.isnull().sum()

        / len(df)

        * 100

    ).round(2)

    report = pd.DataFrame({

        "Missing Values": missing,

        "Missing %": percent

    })

    return report


# ==========================================================
# DUPLICATES
# ==========================================================

def duplicate_information(df):

    duplicates = int(

        df.duplicated().sum()

    )

    return {

        "Duplicate Rows": duplicates

    }


# ==========================================================
# CONSTANT COLUMNS
# ==========================================================

def constant_columns(df):

    columns = []

    for column in df.columns:

        if df[column].nunique(

            dropna=False

        ) <= 1:

            columns.append(column)

    return columns


# ==========================================================
# EMPTY COLUMNS
# ==========================================================

def empty_columns(df):

    columns = []

    for column in df.columns:

        if df[column].isnull().all():

            columns.append(column)

    return columns


# ==========================================================
# HIGH CARDINALITY
# ==========================================================

def high_cardinality_columns(

    df,

    threshold=0.80

):

    columns = []

    for column in df.columns:

        ratio = (

            df[column].nunique()

            / len(df)

        )

        if ratio >= threshold:

            columns.append(column)

    return columns


# ==========================================================
# DATA TYPES
# ==========================================================

def datatype_summary(df):

    summary = []

    for column in df.columns:

        summary.append({

            "Column": column,

            "Type": str(df[column].dtype)

        })

    return pd.DataFrame(summary)


# ==========================================================
# QUALITY SCORE
# ==========================================================

def quality_score(df):

    score = 100

    missing = int(

        df.isnull().sum().sum()

    )

    duplicates = int(

        df.duplicated().sum()

    )

    constant = len(

        constant_columns(df)

    )

    empty = len(

        empty_columns(df)

    )

    score -= min(

        missing,

        20

    )

    score -= min(

        duplicates,

        15

    )

    score -= constant * 3

    score -= empty * 5

    score = max(

        score,

        0

    )

    return score


# ==========================================================
# QUALITY REPORT
# ==========================================================

def generate_quality_report(df):

    report = {

        "Information":

            dataset_information(df),

        "Missing":

            missing_values(df),

        "Duplicates":

            duplicate_information(df),

        "Constant Columns":

            constant_columns(df),

        "Empty Columns":

            empty_columns(df),

        "High Cardinality":

            high_cardinality_columns(df),

        "Data Types":

            datatype_summary(df),

        "Quality Score":

            quality_score(df)

    }

    return report