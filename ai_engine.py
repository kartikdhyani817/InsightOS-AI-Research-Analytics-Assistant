import google.generativeai as genai

# =====================================================
# CONFIGURE GEMINI
# =====================================================

def configure_gemini(api_key):

    try:

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        return model

    except Exception as e:

        raise Exception(
            f"Gemini Configuration Error:\n{e}"
        )


# =====================================================
# GENERATE RESPONSE
# =====================================================

def generate_ai_response(
    api_key,
    document_text,
    question
):

    try:

        model = configure_gemini(api_key)

        prompt = f"""
You are InsightOS, an AI Research and Analytics Assistant.

Your task is to answer ONLY from the uploaded document.

If the answer is not available inside the document,
reply with:

'I could not find that information in the uploaded document.'

-------------------------

DOCUMENT

{document_text}

-------------------------

USER QUESTION

{question}

-------------------------

Answer professionally using bullet points whenever possible.
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Error:\n{e}"


# =====================================================
# DATASET SUMMARY
# =====================================================

def summarize_dataset(
    api_key,
    dataframe
):

    try:

        model = configure_gemini(api_key)

        prompt = f"""
You are an expert Data Analyst.

Below is the first few rows of a dataset.

{dataframe.head(20).to_string()}

Provide:

1. Dataset overview

2. Important observations

3. Possible business insights

4. Data quality issues

5. Recommendations

Keep the answer concise.
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Error:\n{e}"