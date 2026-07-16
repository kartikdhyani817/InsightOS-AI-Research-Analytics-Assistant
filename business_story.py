# ==========================================================
# business_story.py
# InsightOS AI Business Story Generator
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def numeric_columns(df):

    return df.select_dtypes(

        include=np.number

    ).columns.tolist()


# ==========================================================
# DATASET OVERVIEW
# ==========================================================

def overview_story(df):

    rows = len(df)

    cols = len(df.columns)

    missing = int(df.isnull().sum().sum())

    return (
        f"The dataset contains {rows:,} records across "
        f"{cols} columns. "
        f"A total of {missing} missing values were detected."
    )


# ==========================================================
# TOP METRIC STORY
# ==========================================================

def top_metric_story(df):

    numeric = numeric_columns(df)

    if len(numeric) == 0:

        return "No numeric metrics were found."

    totals = df[numeric].sum()

    metric = totals.idxmax()

    value = totals.max()

    return (
        f"The highest overall business metric is "
        f"'{metric}' with a total value of "
        f"{value:,.2f}."
    )


# ==========================================================
# TREND STORY
# ==========================================================

def trend_story(df):

    numeric = numeric_columns(df)

    if len(numeric) == 0:

        return "Trend analysis is unavailable."

    column = numeric[0]

    first = df[column].iloc[0]

    last = df[column].iloc[-1]

    if last > first:

        trend = "an increasing"

    elif last < first:

        trend = "a decreasing"

    else:

        trend = "a stable"

    return (
        f"The metric '{column}' shows "
        f"{trend} trend throughout the dataset."
    )


# ==========================================================
# DATA QUALITY STORY
# ==========================================================

def quality_story(df):

    duplicates = int(df.duplicated().sum())

    missing = int(df.isnull().sum().sum())

    if duplicates == 0 and missing == 0:

        return (
            "The dataset appears clean with no duplicate "
            "records or missing values."
        )

    messages = []

    if duplicates > 0:

        messages.append(

            f"{duplicates} duplicate rows"

        )

    if missing > 0:

        messages.append(

            f"{missing} missing values"

        )

    return (
        "The dataset contains "

        + " and ".join(messages)

        + " that should be reviewed before reporting."
    )


# ==========================================================
# AI RECOMMENDATION
# ==========================================================

def recommendation_story(df):

    recommendations = [

        "Monitor the highest-performing KPI regularly.",

        "Review missing values before business reporting.",

        "Track trends using interactive dashboards.",

        "Automate executive reports for stakeholders."

    ]

    return recommendations


# ==========================================================
# EXECUTIVE STORY
# ==========================================================

def executive_story(df):

    story = []

    story.append(

        overview_story(df)

    )

    story.append(

        top_metric_story(df)

    )

    story.append(

        trend_story(df)

    )

    story.append(

        quality_story(df)

    )

    return "\n\n".join(story)


# ==========================================================
# COMPLETE BUSINESS STORY
# ==========================================================

def generate_business_story(df):

    return {

        "Executive Story":

            executive_story(df),

        "Recommendations":

            recommendation_story(df)

    }