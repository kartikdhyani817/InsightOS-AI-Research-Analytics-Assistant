from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from reportlab.lib import colors
from reportlab.lib.units import inch

from datetime import datetime


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def executive_summary(df):

    summary = {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Missing Values": int(df.isnull().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum()),

        "Numeric Columns": len(

            df.select_dtypes(include="number").columns

        )

    }

    return summary


# =====================================================
# COLUMN REPORT
# =====================================================

def column_summary(df):

    data = []

    for column in df.columns:

        data.append(

            [

                column,

                str(df[column].dtype),

                int(df[column].isnull().sum()),

                int(df[column].nunique())

            ]

        )

    return data


# =====================================================
# CREATE PDF REPORT
# =====================================================

def generate_pdf_report(

    df,

    filename="InsightOS_Report.pdf"

):

    doc = SimpleDocTemplate(

        filename

    )

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(

        "InsightOS AI Business Intelligence Report",

        styles["Title"]

    )

    story.append(title)

    story.append(Spacer(1, 0.3 * inch))

    generated = Paragraph(

        f"Generated : {datetime.now()}",

        styles["Normal"]

    )

    story.append(generated)

    story.append(Spacer(1, 0.25 * inch))

    story.append(

        Paragraph(

            "Executive Summary",

            styles["Heading2"]

        )

    )

    summary = executive_summary(df)

    for key, value in summary.items():

        story.append(

            Paragraph(

                f"<b>{key}</b> : {value}",

                styles["BodyText"]

            )

        )

    story.append(

        Spacer(1, 0.25 * inch)

    )

    story.append(

        Paragraph(

            "Column Information",

            styles["Heading2"]

        )

    )

    table_data = [

        [

            "Column",

            "Type",

            "Missing",

            "Unique"

        ]

    ]

    table_data.extend(

        column_summary(df)

    )

    table = Table(table_data)

    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                ("ALIGN", (0, 0), (-1, -1), "CENTER")

            ]

        )

    )

    story.append(table)

    story.append(

        Spacer(1, 0.3 * inch)

    )

    story.append(

        Paragraph(

            "Generated using InsightOS",

            styles["Italic"]

        )

    )

    doc.build(story)

    return filename


# =====================================================
# AI REPORT PROMPT
# =====================================================

def build_ai_report_prompt(df):

    prompt = f"""

You are an experienced Business Intelligence Consultant.

Dataset Information

Rows : {len(df)}

Columns : {len(df.columns)}

Column Names

{list(df.columns)}

Generate

1. Executive Summary

2. Key Findings

3. Business Insights

4. Risks

5. Opportunities

6. Recommendations

"""

    return prompt
# =====================================================
# LEGACY FUNCTIONS (Backward Compatibility)
# =====================================================

def generate_executive_summary(df):
    return executive_summary(df)


def generate_text_report(df):

    report = []

    report.append("InsightOS Executive Report")
    report.append("=" * 50)

    summary = executive_summary(df)

    for key, value in summary.items():
        report.append(f"{key}: {value}")

    report.append("")
    report.append("Columns:")
    report.extend(df.columns.tolist())

    return "\n".join(report)