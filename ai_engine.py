import google.generativeai as genai


# =====================================================
# CONFIGURE GEMINI
# =====================================================

def configure_gemini(api_key):

    genai.configure(api_key=api_key)

    return genai.GenerativeModel("gemini-2.5-flash")


# =====================================================
# GENERATE AI RESPONSE
# =====================================================

def generate_ai_response(api_key, context, question):

    model = configure_gemini(api_key)

    prompt = f"""
You are InsightOS, an AI-powered Business Intelligence Assistant.

Context:
{context}

User Question:
{question}

Instructions:
- Answer clearly and professionally.
- Use only the provided context.
- If the answer is unavailable, state that clearly.
- Use bullet points where appropriate.
"""

    response = model.generate_content(prompt)

    return response.text


# =====================================================
# DATASET SUMMARY
# =====================================================

def summarize_dataset(api_key, df):

    model = configure_gemini(api_key)

    prompt = f"""
You are a Senior Data Analyst.

Dataset Information

Rows: {len(df)}
Columns: {len(df.columns)}

Columns:
{list(df.columns)}

First 10 Rows:
{df.head(10).to_string()}

Generate:
1. Executive Summary
2. Key Insights
3. Data Quality Review
4. Business Recommendations
"""

    response = model.generate_content(prompt)

    return response.text


# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

def executive_insights(api_key, df):

    model = configure_gemini(api_key)

    prompt = f"""
You are a Chief Business Intelligence Consultant.

Dataset Shape:
Rows = {len(df)}
Columns = {len(df.columns)}

Column Names:
{list(df.columns)}

Provide:

- Top 5 Business Insights
- Opportunities
- Risks
- Executive Recommendations

Keep the response concise and professional.
"""

    response = model.generate_content(prompt)

    return response.text


# =====================================================
# DATASET HEALTH SCORE
# =====================================================

def dataset_health_score(df):

    total_cells = len(df) * len(df.columns)

    missing = int(df.isnull().sum().sum())

    duplicate = int(df.duplicated().sum())

    if total_cells == 0:
        return 0

    score = 100

    score -= (missing / total_cells) * 100

    score -= (duplicate / max(len(df), 1)) * 10

    score = max(0, min(100, round(score)))

    return score


# =====================================================
# KPI SUMMARY
# =====================================================

def kpi_summary(df):

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Missing Values": int(df.isnull().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum()),

        "Numeric Columns": len(

            df.select_dtypes(include="number").columns

        ),

        "Categorical Columns": len(

            df.select_dtypes(include="object").columns

        ),

        "Dataset Health": dataset_health_score(df)

    }