# ==========================================================
# dashboard_templates.py
# InsightOS Enterprise Dashboard Templates
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# AVAILABLE TEMPLATES
# ==========================================================

TEMPLATES = {

    "Executive Dashboard": {

        "description": "Overall business health with KPIs and executive insights.",

        "charts": [

            "KPI Cards",

            "Line Chart",

            "Bar Chart",

            "Pie Chart"

        ]

    },

    "Sales Dashboard": {

        "description": "Revenue, sales trends, profit and quantity analysis.",

        "charts": [

            "Revenue Trend",

            "Sales by Category",

            "Profit Analysis",

            "Top Products"

        ]

    },

    "Marketing Dashboard": {

        "description": "Campaign performance and marketing analytics.",

        "charts": [

            "Campaign ROI",

            "Channel Performance",

            "Lead Analysis"

        ]

    },

    "Finance Dashboard": {

        "description": "Financial performance and profitability.",

        "charts": [

            "Revenue",

            "Profit",

            "Expenses",

            "Cash Flow"

        ]

    },

    "HR Dashboard": {

        "description": "Employee and workforce analytics.",

        "charts": [

            "Department Distribution",

            "Employee Trends",

            "Salary Analysis"

        ]

    },

    "Operations Dashboard": {

        "description": "Operational performance monitoring.",

        "charts": [

            "Operational KPIs",

            "Process Efficiency",

            "Inventory"

        ]

    }

}


# ==========================================================
# COLUMN DETECTION
# ==========================================================

def detect_keywords(df):

    columns = [

        c.lower()

        for c in df.columns

    ]

    return columns


# ==========================================================
# TEMPLATE DETECTION
# ==========================================================

def suggest_template(df):

    columns = detect_keywords(df)

    text = " ".join(columns)

    if any(

        word in text

        for word in [

            "sales",

            "revenue",

            "profit",

            "quantity"

        ]

    ):

        return "Sales Dashboard"

    if any(

        word in text

        for word in [

            "marketing",

            "campaign",

            "channel",

            "click"

        ]

    ):

        return "Marketing Dashboard"

    if any(

        word in text

        for word in [

            "employee",

            "salary",

            "department",

            "hr"

        ]

    ):

        return "HR Dashboard"

    if any(

        word in text

        for word in [

            "expense",

            "finance",

            "budget",

            "cash"

        ]

    ):

        return "Finance Dashboard"

    if any(

        word in text

        for word in [

            "inventory",

            "operation",

            "warehouse",

            "stock"

        ]

    ):

        return "Operations Dashboard"

    return "Executive Dashboard"


# ==========================================================
# TEMPLATE DETAILS
# ==========================================================

def get_template(df):

    name = suggest_template(df)

    return {

        "Template": name,

        **TEMPLATES[name]

    }


# ==========================================================
# ALL TEMPLATES
# ==========================================================

def available_templates():

    return list(

        TEMPLATES.keys()

    )


# ==========================================================
# TEMPLATE REPORT
# ==========================================================

def generate_template_report(df):

    selected = get_template(df)

    return {

        "Suggested Template":

            selected,

        "Available Templates":

            available_templates()

    }