# ==========================================================
# performance_optimizer.py
# InsightOS Enterprise Performance Optimizer
# ==========================================================

import pandas as pd
import numpy as np
import time


# ==========================================================
# TIMER
# ==========================================================

class PerformanceTimer:

    def __init__(self):

        self.start = None

        self.end = None

    def start_timer(self):

        self.start = time.perf_counter()

    def stop_timer(self):

        self.end = time.perf_counter()

        return round(

            self.end - self.start,

            4

        )


# ==========================================================
# DATASET SIZE
# ==========================================================

def dataset_size(df):

    rows = len(df)

    cols = len(df.columns)

    return {

        "Rows": rows,

        "Columns": cols,

        "Cells": rows * cols

    }


# ==========================================================
# MEMORY USAGE
# ==========================================================

def memory_usage(df):

    memory = (

        df.memory_usage(

            deep=True

        ).sum()

        / 1024

        / 1024

    )

    return round(memory, 2)


# ==========================================================
# MEMORY OPTIMIZATION
# ==========================================================

def optimize_memory(df):

    optimized = df.copy()

    for column in optimized.columns:

        dtype = optimized[column].dtype

        if str(dtype).startswith("int"):

            optimized[column] = pd.to_numeric(

                optimized[column],

                downcast="integer"

            )

        elif str(dtype).startswith("float"):

            optimized[column] = pd.to_numeric(

                optimized[column],

                downcast="float"

            )

        elif dtype == "object":

            unique = optimized[column].nunique()

            total = len(optimized[column])

            if total > 0 and unique / total < 0.5:

                optimized[column] = optimized[column].astype(

                    "category"

                )

    return optimized


# ==========================================================
# SMART SAMPLING
# ==========================================================

def smart_sample(

    df,

    max_rows=10000

):

    if len(df) <= max_rows:

        return df.copy()

    return df.sample(

        max_rows,

        random_state=42

    )


# ==========================================================
# LARGE DATASET CHECK
# ==========================================================

def is_large_dataset(

    df,

    threshold=100000

):

    return len(df) >= threshold


# ==========================================================
# PERFORMANCE SCORE
# ==========================================================

def performance_score(df):

    rows = len(df)

    memory = memory_usage(df)

    score = 100

    if rows > 100000:

        score -= 15

    if rows > 500000:

        score -= 20

    if memory > 100:

        score -= 10

    if memory > 500:

        score -= 15

    return max(score, 0)


# ==========================================================
# DATASET SUMMARY
# ==========================================================

def dataset_summary(df):

    return {

        "Dataset Size":

            dataset_size(df),

        "Memory (MB)":

            memory_usage(df),

        "Large Dataset":

            is_large_dataset(df),

        "Performance Score":

            performance_score(df)

    }


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

def optimization_recommendations(df):

    recommendations = []

    if len(df) > 100000:

        recommendations.append(

            "Enable Smart Sampling."

        )

    if memory_usage(df) > 100:

        recommendations.append(

            "Apply Memory Optimization."

        )

    if len(recommendations) == 0:

        recommendations.append(

            "Dataset is already optimized."

        )

    return recommendations


# ==========================================================
# COMPLETE REPORT
# ==========================================================

def optimization_report(df):

    optimized = optimize_memory(df)

    return {

        "Original Memory":

            memory_usage(df),

        "Optimized Memory":

            memory_usage(optimized),

        "Performance":

            dataset_summary(df),

        "Recommendations":

            optimization_recommendations(df)

    }