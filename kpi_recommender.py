# ==========================================================
# kpi_recommender.py
# InsightOS AI KPI Recommendation Engine
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
# KEYWORD SCORE
# ==========================================================

def keyword_score(column):

    name = column.lower()

    score = 0

    keywords = {

        "revenue": 100,

        "sales": 95,

        "profit": 90,

        "income": 90,

        "amount": 85,

        "price": 80,

        "cost": 80,

        "margin": 75,

        "quantity": 70,

        "qty": 70,

        "customer": 65,

        "order": 60,

        "units": 60,

        "expense": 55,

        "growth": 55,

        "inventory": 50

    }

    for key, value in keywords.items():

        if key in name:

            score = max(score, value)

    return score


# ==========================================================
# RECOMMEND KPIs
# ==========================================================

def recommend_kpis(df):

    numeric = numeric_columns(df)

    recommendations = []

    for column in numeric:

        recommendations.append({

            "Column": column,

            "Priority": keyword_score(column),

            "Mean": round(df[column].mean(), 2),

            "Sum": round(df[column].sum(), 2),

            "Maximum": round(df[column].max(), 2),

            "Minimum": round(df[column].min(), 2)

        })

    recommendations = sorted(

        recommendations,

        key=lambda x: x["Priority"],

        reverse=True

    )

    return recommendations


# ==========================================================
# BEST KPI
# ==========================================================

def best_kpi(df):

    kpis = recommend_kpis(df)

    if len(kpis) == 0:

        return None

    return kpis[0]


# ==========================================================
# DASHBOARD KPIs
# ==========================================================

def dashboard_kpis(df, top_n=4):

    return recommend_kpis(df)[:top_n]