# ==========================================================
# system_monitor.py
# InsightOS Enterprise System Monitor
# ==========================================================

import time
import platform
import pandas as pd


# ==========================================================
# APPLICATION TIMER
# ==========================================================

class AppMonitor:

    def __init__(self):

        self.start_time = time.time()

    def uptime(self):

        return round(

            time.time() - self.start_time,

            2

        )


# ==========================================================
# DATASET STATISTICS
# ==========================================================

def dataset_statistics(df):

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Cells": len(df) * len(df.columns)

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
# DATASET HEALTH
# ==========================================================

def dataset_health(df):

    missing = int(df.isnull().sum().sum())

    duplicates = int(df.duplicated().sum())

    score = 100

    score -= min(missing, 20)

    score -= min(duplicates, 10)

    return max(score, 0)


# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

def system_information():

    return {

        "Platform": platform.system(),

        "Python Version": platform.python_version(),

        "Processor": platform.processor()

    }


# ==========================================================
# FEATURE COUNTERS
# ==========================================================

class FeatureCounter:

    def __init__(self):

        self.ai_requests = 0

        self.reports_generated = 0

        self.exports = 0

        self.charts_created = 0

    def ai_request(self):

        self.ai_requests += 1

    def report(self):

        self.reports_generated += 1

    def export(self):

        self.exports += 1

    def chart(self):

        self.charts_created += 1

    def summary(self):

        return {

            "AI Requests":

                self.ai_requests,

            "Reports":

                self.reports_generated,

            "Exports":

                self.exports,

            "Charts":

                self.charts_created

        }


# ==========================================================
# PERFORMANCE GRADE
# ==========================================================

def performance_grade(df):

    rows = len(df)

    memory = memory_usage(df)

    score = 100

    if rows > 100000:

        score -= 15

    if memory > 100:

        score -= 15

    if score >= 90:

        return "A"

    elif score >= 75:

        return "B"

    elif score >= 60:

        return "C"

    return "D"


# ==========================================================
# COMPLETE SYSTEM REPORT
# ==========================================================

def system_report(df):

    return {

        "Dataset":

            dataset_statistics(df),

        "Memory (MB)":

            memory_usage(df),

        "Health Score":

            dataset_health(df),

        "Performance Grade":

            performance_grade(df),

        "System":

            system_information()

    }