import pandas as pd


# =====================================================
# SEARCH IN DATAFRAME
# =====================================================

def search_dataframe(df, query):

    if df is None or df.empty:
        return pd.DataFrame()

    query = str(query).lower()

    mask = df.astype(str).apply(
        lambda col: col.str.lower().str.contains(query, na=False)
    )

    return df[mask.any(axis=1)]


# =====================================================
# SEARCH IN DOCUMENT
# =====================================================

def search_document(text, query):

    if not text:
        return []

    query = query.lower()

    lines = text.split("\n")

    results = []

    for index, line in enumerate(lines):

        if query in line.lower():

            results.append({

                "Line": index + 1,

                "Text": line.strip()

            })

    return results


# =====================================================
# GLOBAL SEARCH
# =====================================================

def global_search(dataframe=None, document_text="", query=""):

    result = {

        "dataframe": None,

        "document": None

    }

    if dataframe is not None:

        result["dataframe"] = search_dataframe(

            dataframe,

            query

        )

    if document_text:

        result["document"] = search_document(

            document_text,

            query

        )

    return result


# =====================================================
# DATAFRAME COLUMN SEARCH
# =====================================================

def search_columns(df, query):

    if df is None:

        return []

    query = query.lower()

    return [

        column

        for column in df.columns

        if query in column.lower()

    ]


# =====================================================
# TOP MATCHES
# =====================================================

def top_matches(df, query, limit=10):

    results = search_dataframe(df, query)

    if results.empty:

        return results

    return results.head(limit)