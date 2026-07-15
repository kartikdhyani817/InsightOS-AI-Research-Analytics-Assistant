# ==========================================================
# insight_cards.py
# InsightOS AI Insight Cards
# ==========================================================

import pandas as pd


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def numeric_columns(df):

    return df.select_dtypes(

        include="number"

    ).columns.tolist()


# ==========================================================
# MISSING VALUE COLUMN
# ==========================================================

def highest_missing_column(df):

    missing = df.isnull().sum()

    if missing.sum() == 0:

        return {

            "Column": "None",

            "Missing": 0

        }

    column = missing.idxmax()

    return {

        "Column": column,

        "Missing": int(missing.max())

    }


# ==========================================================
# HIGHEST AVERAGE VALUE
# ==========================================================

def highest_average_metric(df):

    numeric = numeric_columns(df)

    if len(numeric) == 0:

        return None

    averages = df[numeric].mean()

    column = averages.idxmax()

    return {

        "Metric": column,

        "Value": round(float(averages.max()), 2)

    }


# ==========================================================
# HIGHEST TOTAL VALUE
# ==========================================================

def highest_total_metric(df):

    numeric = numeric_columns(df)

    if len(numeric) == 0:

        return None

    totals = df[numeric].sum()

    column = totals.idxmax()

    return {

        "Metric": column,

        "Value": round(float(totals.max()), 2)

    }


# ==========================================================
# OUTLIER DETECTION
# ==========================================================

def outlier_summary(df):

    numeric = numeric_columns(df)

    summary = []

    for column in numeric:

        q1 = df[column].quantile(0.25)

        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        count = int(

            (

                (df[column] < lower)

                |

                (df[column] > upper)

            ).sum()

        )

        summary.append({

            "Column": column,

            "Outliers": count

        })

    return pd.DataFrame(summary)


# ==========================================================
# INSIGHT CARDS
# ==========================================================

def generate_insight_cards(df):

    cards = {}

    cards["Highest Average"] = highest_average_metric(df)

    cards["Highest Total"] = highest_total_metric(df)

    cards["Missing Values"] = highest_missing_column(df)

    cards["Outliers"] = outlier_summary(df)

    return cards