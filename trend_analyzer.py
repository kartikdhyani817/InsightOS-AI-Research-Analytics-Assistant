# ==========================================================
# trend_analyzer.py
# InsightOS AI Trend Analyzer
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def get_numeric_columns(df):

    return df.select_dtypes(include=np.number).columns.tolist()


# ==========================================================
# GROWTH PERCENTAGE
# ==========================================================

def growth_percentage(series):

    series = pd.Series(series).dropna()

    if len(series) < 2:
        return 0

    first = float(series.iloc[0])
    last = float(series.iloc[-1])

    if first == 0:
        return 0

    growth = ((last - first) / abs(first)) * 100

    return round(growth, 2)


# ==========================================================
# TREND TYPE
# ==========================================================

def trend_type(series):

    growth = growth_percentage(series)

    if growth >= 20:
        return "Strong Growth"

    elif growth >= 5:
        return "Moderate Growth"

    elif growth <= -20:
        return "Strong Decline"

    elif growth <= -5:
        return "Moderate Decline"

    return "Stable"


# ==========================================================
# TREND STRENGTH
# ==========================================================

def trend_strength(series):

    series = pd.Series(series).dropna()

    if len(series) < 2:
        return 0

    x = np.arange(len(series))

    slope, intercept = np.polyfit(x, series, 1)

    return round(float(abs(slope)), 2)


# ==========================================================
# MOMENTUM
# ==========================================================

def momentum(series):

    series = pd.Series(series).dropna()

    if len(series) < 3:
        return "Unknown"

    recent = series.tail(3).mean()
    previous = series.head(3).mean()

    if recent > previous:
        return "Positive"

    elif recent < previous:
        return "Negative"

    return "Neutral"


# ==========================================================
# ANALYZE SINGLE METRIC
# ==========================================================

def analyze_metric(df, column):

    if column not in df.columns:
        return None

    series = df[column]

    return {

        "Metric": column,

        "Growth (%)": growth_percentage(series),

        "Trend": trend_type(series),

        "Trend Strength": trend_strength(series),

        "Momentum": momentum(series)

    }


# ==========================================================
# ANALYZE ALL METRICS
# ==========================================================

def analyze_all_metrics(df):

    results = []

    for column in get_numeric_columns(df):

        results.append(

            analyze_metric(

                df,

                column

            )

        )

    return results


# ==========================================================
# TOP GROWING METRIC
# ==========================================================

def top_growing_metric(df):

    analysis = analyze_all_metrics(df)

    if len(analysis) == 0:
        return None

    return max(

        analysis,

        key=lambda x: x["Growth (%)"]

    )


# ==========================================================
# FASTEST DECLINING METRIC
# ==========================================================

def top_declining_metric(df):

    analysis = analyze_all_metrics(df)

    if len(analysis) == 0:
        return None

    return min(

        analysis,

        key=lambda x: x["Growth (%)"]

    )


# ==========================================================
# AI TREND SUMMARY
# ==========================================================

def trend_summary(df):

    analysis = analyze_all_metrics(df)

    summary = []

    for item in analysis:

        summary.append(

            f"{item['Metric']} shows "

            f"{item['Trend'].lower()} "

            f"with {item['Momentum'].lower()} momentum."

        )

    return summary