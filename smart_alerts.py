# ==========================================================
# smart_alerts.py
# InsightOS Smart Business Alerts
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# HIGH MISSING VALUE ALERT
# ==========================================================

def missing_value_alert(df):

    missing = int(df.isnull().sum().sum())

    percentage = round(

        (missing / df.size) * 100,

        2

    )

    if percentage >= 20:

        return {

            "Level": "🔴 Critical",

            "Message": f"Dataset has {percentage}% missing values."

        }

    elif percentage >= 5:

        return {

            "Level": "🟡 Warning",

            "Message": f"Dataset has {percentage}% missing values."

        }

    return {

        "Level": "🟢 Healthy",

        "Message": "Missing values are within acceptable limits."

    }


# ==========================================================
# DUPLICATE ALERT
# ==========================================================

def duplicate_alert(df):

    duplicates = int(df.duplicated().sum())

    if duplicates == 0:

        return {

            "Level": "🟢 Healthy",

            "Message": "No duplicate rows detected."

        }

    if duplicates >= 100:

        level = "🔴 Critical"

    else:

        level = "🟡 Warning"

    return {

        "Level": level,

        "Message": f"{duplicates} duplicate rows detected."

    }


# ==========================================================
# OUTLIER ALERT
# ==========================================================

def outlier_alert(df):

    numeric = df.select_dtypes(include=np.number)

    outliers = 0

    for column in numeric.columns:

        q1 = numeric[column].quantile(0.25)

        q3 = numeric[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        outliers += len(

            numeric[

                (numeric[column] < lower)

                |

                (numeric[column] > upper)

            ]

        )

    if outliers == 0:

        return {

            "Level": "🟢 Healthy",

            "Message": "No unusual outliers detected."

        }

    if outliers >= 50:

        level = "🔴 Critical"

    else:

        level = "🟡 Warning"

    return {

        "Level": level,

        "Message": f"{outliers} potential outliers detected."

    }


# ==========================================================
# BUSINESS OPPORTUNITY ALERT
# ==========================================================

def opportunity_alert(df):

    numeric = df.select_dtypes(include=np.number)

    if numeric.empty:

        return {

            "Level": "🔵 Info",

            "Message": "No numeric business metrics available."

        }

    metric = numeric.sum().idxmax()

    value = numeric.sum().max()

    return {

        "Level": "🔵 Opportunity",

        "Message":

            f"'{metric}' is the strongest performing metric "

            f"({value:,.2f})."

    }


# ==========================================================
# PERFORMANCE ALERT
# ==========================================================

def performance_alert(df):

    rows = len(df)

    if rows > 500000:

        return {

            "Level": "🟡 Warning",

            "Message":

                "Large dataset detected. "

                "Smart Sampling is recommended."

        }

    return {

        "Level": "🟢 Healthy",

        "Message": "Dataset size is optimal."

    }


# ==========================================================
# ALERT PRIORITY
# ==========================================================

def alert_priority(alerts):

    if any(

        a["Level"] == "🔴 Critical"

        for a in alerts

    ):

        return "High"

    if any(

        a["Level"] == "🟡 Warning"

        for a in alerts

    ):

        return "Medium"

    return "Low"


# ==========================================================
# COMPLETE ALERT REPORT
# ==========================================================

def generate_alerts(df):

    alerts = [

        missing_value_alert(df),

        duplicate_alert(df),

        outlier_alert(df),

        opportunity_alert(df),

        performance_alert(df)

    ]

    return {

        "Priority":

            alert_priority(alerts),

        "Alerts":

            alerts

    }