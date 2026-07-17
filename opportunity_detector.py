# ==========================================================
# opportunity_detector.py
# InsightOS AI Opportunity Detector
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def numeric_columns(df):

    return df.select_dtypes(include=np.number).columns.tolist()


# ==========================================================
# TOP PERFORMING METRICS
# ==========================================================

def top_metrics(df, top_n=5):

    numeric = numeric_columns(df)

    if len(numeric) == 0:

        return pd.DataFrame()

    totals = []

    for column in numeric:

        totals.append({

            "Metric": column,

            "Total": round(float(df[column].sum()), 2),

            "Average": round(float(df[column].mean()), 2)

        })

    result = pd.DataFrame(totals)

    result = result.sort_values(

        by="Total",

        ascending=False

    )

    return result.head(top_n)


# ==========================================================
# FASTEST GROWING METRICS
# ==========================================================

def growing_metrics(df):

    numeric = numeric_columns(df)

    growth = []

    for column in numeric:

        series = df[column].dropna()

        if len(series) < 2:

            continue

        first = float(series.iloc[0])

        last = float(series.iloc[-1])

        if first == 0:

            continue

        percent = (

            (last - first)

            / abs(first)

        ) * 100

        growth.append({

            "Metric": column,

            "Growth (%)": round(percent, 2)

        })

    result = pd.DataFrame(growth)

    if result.empty:

        return result

    return result.sort_values(

        by="Growth (%)",

        ascending=False

    )


# ==========================================================
# HIGH VALUE METRICS
# ==========================================================

def high_value_metrics(df):

    numeric = numeric_columns(df)

    metrics = []

    for column in numeric:

        avg = float(df[column].mean())

        std = float(df[column].std())

        metrics.append({

            "Metric": column,

            "Average": round(avg, 2),

            "Variation": round(std, 2)

        })

    return pd.DataFrame(metrics)


# ==========================================================
# BUSINESS OPPORTUNITIES
# ==========================================================

def business_opportunities(df):

    opportunities = []

    top = top_metrics(df, 3)

    for _, row in top.iterrows():

        opportunities.append(

            f"'{row['Metric']}' is a high-performing metric. Consider increasing focus on this area."

        )

    growth = growing_metrics(df)

    if not growth.empty:

        best = growth.iloc[0]

        opportunities.append(

            f"'{best['Metric']}' has grown by {best['Growth (%)']}%. It represents a strong growth opportunity."

        )

    return opportunities


# ==========================================================
# REVENUE DRIVER
# ==========================================================

def revenue_driver(df):

    numeric = numeric_columns(df)

    if len(numeric) == 0:

        return None

    totals = {

        col: df[col].sum()

        for col in numeric

    }

    metric = max(

        totals,

        key=totals.get

    )

    return {

        "Primary Driver": metric,

        "Contribution": round(

            float(totals[metric]),

            2

        )

    }


# ==========================================================
# OPPORTUNITY SCORE
# ==========================================================

def opportunity_score(df):

    numeric = len(

        numeric_columns(df)

    )

    score = min(

        100,

        60 + numeric * 5

    )

    return score


# ==========================================================
# COMPLETE OPPORTUNITY REPORT
# ==========================================================

def generate_opportunity_report(df):

    return {

        "Opportunity Score":

            opportunity_score(df),

        "Top Metrics":

            top_metrics(df),

        "Growing Metrics":

            growing_metrics(df),

        "High Value Metrics":

            high_value_metrics(df),

        "Revenue Driver":

            revenue_driver(df),

        "Business Opportunities":

            business_opportunities(df)

    }