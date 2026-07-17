# ==========================================================
# recommendation_engine.py
# InsightOS AI Recommendation Engine
# ==========================================================

from forecast_engine import forecast_all_metrics
from trend_analyzer import analyze_all_metrics
from opportunity_detector import generate_opportunity_report
from risk_analyzer import generate_risk_report


# ==========================================================
# FORECAST RECOMMENDATIONS
# ==========================================================

def forecast_recommendations(df):

    recommendations = []

    forecasts = forecast_all_metrics(df)

    for item in forecasts:

        if item is None:
            continue

        if item["Trend"] == "Increasing":

            recommendations.append(

                f"Increase investment in '{item['Metric']}' because it shows positive future growth."

            )

        elif item["Trend"] == "Decreasing":

            recommendations.append(

                f"Monitor '{item['Metric']}' closely because the forecast indicates a decline."

            )

    return recommendations


# ==========================================================
# TREND RECOMMENDATIONS
# ==========================================================

def trend_recommendations(df):

    recommendations = []

    trends = analyze_all_metrics(df)

    for item in trends:

        if item["Trend"] == "Strong Growth":

            recommendations.append(

                f"Expand business around '{item['Metric']}' due to strong growth."

            )

        elif item["Trend"] == "Strong Decline":

            recommendations.append(

                f"Review business strategy for '{item['Metric']}' because of significant decline."

            )

    return recommendations


# ==========================================================
# OPPORTUNITY RECOMMENDATIONS
# ==========================================================

def opportunity_recommendations(df):

    report = generate_opportunity_report(df)

    return report["Business Opportunities"]


# ==========================================================
# RISK RECOMMENDATIONS
# ==========================================================

def risk_recommendations(df):

    report = generate_risk_report(df)

    return report["Recommendations"]


# ==========================================================
# EXECUTIVE RECOMMENDATIONS
# ==========================================================

def executive_recommendations(df):

    recommendations = []

    recommendations.extend(

        forecast_recommendations(df)

    )

    recommendations.extend(

        trend_recommendations(df)

    )

    recommendations.extend(

        opportunity_recommendations(df)

    )

    recommendations.extend(

        risk_recommendations(df)

    )

    unique = []

    for recommendation in recommendations:

        if recommendation not in unique:

            unique.append(recommendation)

    return unique


# ==========================================================
# PRIORITY SCORE
# ==========================================================

def priority_score(recommendations):

    if len(recommendations) >= 10:

        return "High"

    elif len(recommendations) >= 5:

        return "Medium"

    return "Low"


# ==========================================================
# COMPLETE AI REPORT
# ==========================================================

def generate_recommendation_report(df):

    recommendations = executive_recommendations(df)

    return {

        "Priority":

            priority_score(recommendations),

        "Total Recommendations":

            len(recommendations),

        "Recommendations":

            recommendations

    }