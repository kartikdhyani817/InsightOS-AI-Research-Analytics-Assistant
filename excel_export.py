# ==========================================================
# excel_export.py
# InsightOS Excel Report Generator
# ==========================================================

from io import BytesIO
import pandas as pd


# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

def executive_summary(df):

    return pd.DataFrame({

        "Metric": [

            "Rows",

            "Columns",

            "Missing Values",

            "Duplicate Rows"

        ],

        "Value": [

            len(df),

            len(df.columns),

            int(df.isnull().sum().sum()),

            int(df.duplicated().sum())

        ]

    })


# ==========================================================
# COLUMN INFORMATION
# ==========================================================

def column_information(df):

    return pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str),

        "Missing Values": df.isnull().sum().values,

        "Unique Values": df.nunique().values

    })


# ==========================================================
# NUMERIC SUMMARY
# ==========================================================

def numeric_summary(df):

    numeric = df.select_dtypes(include="number")

    if numeric.empty:

        return pd.DataFrame()

    return numeric.describe().transpose()


# ==========================================================
# MISSING VALUE REPORT
# ==========================================================

def missing_value_report(df):

    report = pd.DataFrame({

        "Column": df.columns,

        "Missing Values": df.isnull().sum().values,

        "Percentage": (

            df.isnull().sum()

            / len(df)

            * 100

        ).round(2).values

    })

    return report.sort_values(

        "Missing Values",

        ascending=False

    )


# ==========================================================
# EXPORT EXCEL
# ==========================================================

def export_excel_report(df):

    output = BytesIO()

    with pd.ExcelWriter(

        output,

        engine="openpyxl"

    ) as writer:

        executive_summary(df).to_excel(

            writer,

            sheet_name="Executive Summary",

            index=False

        )

        column_information(df).to_excel(

            writer,

            sheet_name="Columns",

            index=False

        )

        numeric_summary(df).to_excel(

            writer,

            sheet_name="Statistics"

        )

        missing_value_report(df).to_excel(

            writer,

            sheet_name="Missing Values",

            index=False

        )

        df.head(1000).to_excel(

            writer,

            sheet_name="Dataset Preview",

            index=False

        )

    output.seek(0)

    return output