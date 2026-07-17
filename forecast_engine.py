# ==========================================================
# forecast_engine.py
# InsightOS AI Forecast Engine
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def get_numeric_columns(df):

    return df.select_dtypes(include=np.number).columns.tolist()


# ==========================================================
# SIMPLE MOVING AVERAGE
# ==========================================================

def moving_average_forecast(series, window=5):

    series = pd.Series(series).dropna()

    if len(series) < window:
        return None

    return round(series.tail(window).mean(), 2)


# ==========================================================
# LINEAR TREND FORECAST
# ==========================================================

def linear_forecast(series, periods=5):

    series = pd.Series(series).dropna()

    if len(series) < 2:
        return []

    x = np.arange(len(series))

    slope, intercept = np.polyfit(x, series, 1)

    future = []

    for i in range(periods):

        prediction = slope * (len(series) + i) + intercept

        future.append(round(float(prediction), 2))

    return future


# ==========================================================
# GROWTH RATE
# ==========================================================

def growth_rate(series):

    series = pd.Series(series).dropna()

    if len(series) < 2:
        return 0

    first = series.iloc[0]
    last = series.iloc[-1]

    if first == 0:
        return 0

    growth = ((last - first) / abs(first)) * 100

    return round(float(growth), 2)


# ==========================================================
# TREND
# ==========================================================

def trend_direction(series):

    growth = growth_rate(series)

    if growth > 5:
        return "Increasing"

    if growth < -5:
        return "Decreasing"

    return "Stable"


# ==========================================================
# CONFIDENCE SCORE
# ==========================================================

def confidence_score(series):

    series = pd.Series(series).dropna()

    if len(series) < 5:
        return 50

    std = float(series.std())

    mean = float(series.mean())

    if mean == 0:
        return 60

    variability = abs(std / mean)

    score = max(40, min(95, 100 - variability * 100))

    return round(score, 1)


# ==========================================================
# FORECAST METRIC
# ==========================================================

def forecast_metric(df, column, periods=5):

    if column not in df.columns:

        return None

    series = df[column]

    return {

        "Metric": column,

        "Trend": trend_direction(series),

        "Growth (%)": growth_rate(series),

        "Moving Average":

            moving_average_forecast(series),

        "Forecast":

            linear_forecast(

                series,

                periods

            ),

        "Confidence":

            confidence_score(series)

    }


# ==========================================================
# FORECAST ALL NUMERIC METRICS
# ==========================================================

def forecast_all_metrics(df, periods=5):

    forecasts = []

    for column in get_numeric_columns(df):

        forecasts.append(

            forecast_metric(

                df,

                column,

                periods

            )

        )

    return forecasts


# ==========================================================
# AI SUMMARY
# ==========================================================

def forecast_summary(df):

    forecasts = forecast_all_metrics(df)

    summary = []

    for item in forecasts:

        summary.append(

            f"{item['Metric']} is "

            f"{item['Trend'].lower()} "

            f"(Growth: {item['Growth (%)']}%). "

            f"Forecast confidence: "

            f"{item['Confidence']}%."

        )

    return summary