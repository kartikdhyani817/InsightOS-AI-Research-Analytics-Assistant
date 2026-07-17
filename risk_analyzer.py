# ==========================================================
# risk_analyzer.py
# InsightOS AI Risk Analyzer
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def numeric_columns(df):

    return df.select_dtypes(include=np.number).columns.tolist()


# ==========================================================
# MISSING VALUE RISK
# ==========================================================

def missing_value_risk(df):

    missing = int(df.isnull().sum().sum())

    percentage = round(

        (missing / df.size) * 100,

        2

    )

    if percentage >= 20:

        level = "High"

    elif percentage >= 5:

        level = "Medium"

    else:

        level = "Low"

    return {

        "Risk": level,

        "Missing Values": missing,

        "Missing %": percentage

    }


# ==========================================================
# DUPLICATE RISK
# ==========================================================

def duplicate_risk(df):

    duplicates = int(df.duplicated().sum())

    if duplicates >= 100:

        level = "High"

    elif duplicates > 0:

        level = "Medium"

    else:

        level = "Low"

    return {

        "Risk": level,

        "Duplicate Rows": duplicates

    }


# ==========================================================
# DECLINING METRICS
# ==========================================================

def declining_metrics(df):

    declining = []

    for column in numeric_columns(df):

        series = df[column].dropna()

        if len(series) < 2:

            continue

        first = float(series.iloc[0])

        last = float(series.iloc[-1])

        if last < first:

            change = round(

                ((last - first) / abs(first)) * 100,

                2

            )

            declining.append({

                "Metric": column,

                "Decline (%)": change

            })

    return pd.DataFrame(declining)


# ==========================================================
# OUTLIER DETECTION
# ==========================================================

def outlier_summary(df):

    summary = []

    for column in numeric_columns(df):

        q1 = df[column].quantile(0.25)

        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        outliers = df[

            (df[column] < lower)

            |

            (df[column] > upper)

        ]

        summary.append({

            "Metric": column,

            "Outliers": len(outliers)

        })

    return pd.DataFrame(summary)


# ==========================================================
# DATA HEALTH SCORE
# ==========================================================

def health_score(df):

    score = 100

    score -= min(

        int(df.isnull().sum().sum()),

        20

    )

    score -= min(

        int(df.duplicated().sum()),

        10

    )

    outliers = outlier_summary(df)

    score -= min(

        int(outliers["Outliers"].sum()),

        20

    )

    return max(score, 0)


# ==========================================================
# AI RISK RECOMMENDATIONS
# ==========================================================

def recommendations(df):

    advice = []

    if df.isnull().sum().sum() > 0:

        advice.append(

            "Review missing values before reporting."

        )

    if df.duplicated().sum() > 0:

        advice.append(

            "Remove duplicate records."

        )

    decline = declining_metrics(df)

    if not decline.empty:

        advice.append(

            "Investigate declining business metrics."

        )

    outliers = outlier_summary(df)

    if outliers["Outliers"].sum() > 0:

        advice.append(

            "Validate extreme values before analysis."

        )

    if len(advice) == 0:

        advice.append(

            "No significant business risks detected."

        )

    return advice


# ==========================================================
# COMPLETE RISK REPORT
# ==========================================================

def generate_risk_report(df):

    return {

        "Health Score":

            health_score(df),

        "Missing Value Risk":

            missing_value_risk(df),

        "Duplicate Risk":

            duplicate_risk(df),

        "Declining Metrics":

            declining_metrics(df),

        "Outlier Summary":

            outlier_summary(df),

        "Recommendations":

            recommendations(df)

    }