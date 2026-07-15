# ==========================================================
# chart_explainer.py
# InsightOS Chart Explanation Engine
# ==========================================================

import pandas as pd


# ==========================================================
# HISTOGRAM
# ==========================================================

def explain_histogram(df, column):

    if column not in df.columns:

        return "Selected column was not found."

    mean = df[column].mean()
    median = df[column].median()

    if mean > median:

        shape = "right-skewed"

    elif mean < median:

        shape = "left-skewed"

    else:

        shape = "approximately symmetric"

    return (
        f"The histogram of '{column}' appears {shape}. "
        f"The average value is {mean:.2f} while the median is {median:.2f}. "
        "This helps identify the distribution and potential outliers."
    )


# ==========================================================
# BAR CHART
# ==========================================================

def explain_bar_chart(df, column):

    if column not in df.columns:

        return "Selected column was not found."

    top_value = df[column].max()

    return (
        f"The bar chart compares values across '{column}'. "
        f"The highest observed value is {top_value:.2f}. "
        "Bar charts are useful for comparing categories or magnitudes."
    )


# ==========================================================
# LINE CHART
# ==========================================================

def explain_line_chart(df, column):

    if column not in df.columns:

        return "Selected column was not found."

    first = df[column].iloc[0]
    last = df[column].iloc[-1]

    if last > first:

        trend = "an upward trend"

    elif last < first:

        trend = "a downward trend"

    else:

        trend = "a relatively stable trend"

    return (
        f"The line chart shows {trend} in '{column}'. "
        "Line charts are effective for identifying trends over time or ordered observations."
    )


# ==========================================================
# SCATTER PLOT
# ==========================================================

def explain_scatter_plot(df, x_column, y_column):

    correlation = df[x_column].corr(df[y_column])

    if correlation >= 0.7:

        relation = "a strong positive"

    elif correlation >= 0.3:

        relation = "a moderate positive"

    elif correlation <= -0.7:

        relation = "a strong negative"

    elif correlation <= -0.3:

        relation = "a moderate negative"

    else:

        relation = "little or no"

    return (
        f"The scatter plot indicates {relation} correlation "
        f"between '{x_column}' and '{y_column}'. "
        f"Correlation coefficient = {correlation:.2f}."
    )


# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

def explain_heatmap(df):

    numeric = df.select_dtypes(include="number")

    if numeric.shape[1] < 2:

        return "Not enough numeric columns to compute correlations."

    corr = numeric.corr().abs()

    corr.values[
        range(len(corr)),
        range(len(corr))
    ] = 0

    highest = corr.stack().idxmax()

    value = corr.stack().max()

    return (
        f"The strongest relationship is between "
        f"'{highest[0]}' and '{highest[1]}' "
        f"with correlation {value:.2f}."
    )


# ==========================================================
# UNIVERSAL EXPLAINER
# ==========================================================

def explain_chart(chart_type, df, *columns):

    chart = chart_type.lower()

    if chart == "histogram":

        return explain_histogram(df, columns[0])

    elif chart == "bar":

        return explain_bar_chart(df, columns[0])

    elif chart == "line":

        return explain_line_chart(df, columns[0])

    elif chart == "scatter":

        return explain_scatter_plot(

            df,

            columns[0],

            columns[1]

        )

    elif chart == "heatmap":

        return explain_heatmap(df)

    return "Explanation unavailable."