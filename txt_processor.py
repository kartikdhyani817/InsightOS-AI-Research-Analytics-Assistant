# =====================================================
# TXT PROCESSOR
# =====================================================

SUPPORTED_ENCODINGS = [

    "utf-8",

    "utf-8-sig",

    "cp1252",

    "latin1",

    "ISO-8859-1"

]


# =====================================================
# READ TXT FILE
# =====================================================

def extract_txt_text(uploaded_file):
    """
    Reads a TXT file using multiple encodings.
    """

    for encoding in SUPPORTED_ENCODINGS:

        try:

            uploaded_file.seek(0)

            text = uploaded_file.read().decode(

                encoding,

                errors="ignore"

            )

            return text

        except Exception:

            continue

    return "Unable to read this TXT file."


# =====================================================
# FILE INFORMATION
# =====================================================

def get_txt_information(text):

    info = {

        "Characters": len(text),

        "Words": len(text.split()),

        "Lines": len(text.splitlines())

    }

    return info


# =====================================================
# PREVIEW
# =====================================================

def preview_txt(text, characters=3000):

    return text[:characters]


# =====================================================
# SEARCH TEXT
# =====================================================

def search_text(text, keyword):

    if not keyword:

        return []

    lines = text.splitlines()

    results = []

    for line_number, line in enumerate(lines, start=1):

        if keyword.lower() in line.lower():

            results.append(

                {

                    "Line": line_number,

                    "Content": line

                }

            )

    return results


# =====================================================
# TEXT STATISTICS
# =====================================================

def text_statistics(text):

    return {

        "Characters": len(text),

        "Words": len(text.split()),

        "Lines": len(text.splitlines()),

        "Paragraphs": len(

            [

                p

                for p in text.split("\n\n")

                if p.strip()

            ]

        )

    }