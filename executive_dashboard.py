# ==========================================================
# executive_dashboard.py
# InsightOS Executive Dashboard Generator
# ==========================================================

import pandas as pd

from data_quality import generate_quality_report
from dataset_profile import generate_dataset_profile
from business_story import generate_business_story
from insight_cards import generate_insight_cards
from kpi_recommender import dashboard_kpis


# ==========================================================
# EXECUTIVE KPI SUMMARY
# ==========================================================

def executive_kpis(df):

    cards = generate_insight_cards(df)

    kpis = dashboard_kpis(df)

    return {

        "Insight Cards": cards,

        "Recommended KPIs": kpis

    }


# ==========================================================
# DATA HEALTH
# ==========================================================

def data_health(df):

    quality = generate_quality_report(df)

    score = quality["Quality Score"]

    if score >= 90:

        status = "Excellent"

    elif score >= 75:

        status = "Good"

    elif score >= 60:

        status = "Average"

    else:

        status = "Poor"

    return {

        "Quality Score": score,

        "Status": status

    }


# ==========================================================
# EXECUTIVE DASHBOARD
# ==========================================================

def generate_executive_dashboard(df):

    dashboard = {

        "Health":

            data_health(df),

        "KPIs":

            executive_kpis(df),

        "Dataset":

            generate_dataset_profile(df),

        "Quality":

            generate_quality_report(df),

        "Business Story":

            generate_business_story(df)

    }

    return dashboard


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

def dashboard_summary(df):

    dashboard = generate_executive_dashboard(df)

    summary = {

        "Health":

            dashboard["Health"],

        "Top KPIs":

            dashboard["KPIs"],

        "Business Story":

            dashboard["Business Story"]

    }

    return summary