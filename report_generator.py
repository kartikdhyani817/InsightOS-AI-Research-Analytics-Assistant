from datetime import datetime


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def generate_executive_summary(df):

    summary = []

    summary.append(
        f"Dataset contains {len(df)} rows and {len(df.columns)} columns."
    )

    summary.append(
        f"Missing values: {int(df.isnull().sum().sum())}"
    )

    summary.append(
        f"Duplicate rows: {int(df.duplicated().sum())}"
    )

    numeric_columns = df.select_dtypes(include="number").columns

    summary.append(
        f"Numeric columns: {len(numeric_columns)}"
    )

    return "\n".join(summary)


# =====================================================
# DATA QUALITY REPORT
# =====================================================

def data_quality_report(df):

    report = {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Missing Values": int(df.isnull().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum()),

        "Numeric Columns": len(
            df.select_dtypes(include="number").columns
        ),

        "Categorical Columns": len(
            df.select_dtypes(include="object").columns
        )

    }

    return report


# =====================================================
# COLUMN REPORT
# =====================================================

def column_report(df):

    report = []

    for column in df.columns:

        report.append({

            "Column": column,

            "Type": str(df[column].dtype),

            "Missing": int(df[column].isnull().sum()),

            "Unique": int(df[column].nunique())

        })

    return report


# =====================================================
# AI REPORT TEMPLATE
# =====================================================

def build_ai_prompt(df):

    prompt = f"""

You are a Senior Business Analyst.

Dataset Shape:
Rows : {len(df)}

Columns : {len(df.columns)}

Columns:
{list(df.columns)}

First Five Rows:

{df.head().to_string()}

Generate:

1. Executive Summary

2. Business Insights

3. Data Quality Assessment

4. Risks

5. Recommendations

Use professional business language.

"""

    return prompt


# =====================================================
# SIMPLE REPORT
# =====================================================

def generate_text_report(df):

    report = []

    report.append("=" * 60)

    report.append("INSIGHTOS DATA ANALYSIS REPORT")

    report.append("=" * 60)

    report.append("")

    report.append(

        f"Generated: {datetime.now()}"

    )

    report.append("")

    report.append(generate_executive_summary(df))

    report.append("")

    report.append("Columns")

    report.append("-" * 30)

    report.extend(df.columns.tolist())

    return "\n".join(report)