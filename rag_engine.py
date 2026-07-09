import re


# =====================================================
# TEXT CLEANING
# =====================================================

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# CHUNK DOCUMENT
# =====================================================

def chunk_document(

    text,

    chunk_size=500,

    overlap=100

):

    text = clean_text(text)

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


# =====================================================
# KEYWORD SEARCH
# =====================================================

def search_chunks(

    chunks,

    query

):

    results = []

    query = query.lower()

    for chunk in chunks:

        if query in chunk.lower():

            results.append(chunk)

    return results


# =====================================================
# BEST CONTEXT
# =====================================================

def get_best_context(

    document_text,

    query

):

    chunks = chunk_document(document_text)

    matches = search_chunks(

        chunks,

        query

    )

    if matches:

        return "\n\n".join(matches[:3])

    return document_text[:2000]