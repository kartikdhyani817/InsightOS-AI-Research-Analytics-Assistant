import pandas as pd


def format_file_size(size):

    if size < 1024:
        return f"{size} Bytes"

    elif size < 1024 * 1024:
        return f"{size/1024:.2f} KB"

    else:
        return f"{size/(1024*1024):.2f} MB"


def load_csv(uploaded_file):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin1",
        "ISO-8859-1"
    ]

    separators = [
        ",",
        ";",
        "\t"
    ]

    for encoding in encodings:
        for sep in separators:

            try:

                uploaded_file.seek(0)

                df = pd.read_csv(
                    uploaded_file,
                    encoding=encoding,
                    sep=sep
                )

                return df

            except Exception:
                continue

    raise Exception(
        "Unable to read this CSV file. Please upload a valid CSV."
    )