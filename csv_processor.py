import pandas as pd


def load_csv(uploaded_file):
    """
    Load CSV files with automatic encoding
    and separator detection.
    """

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
        "Unable to read this CSV file."
    )


def dataset_summary(df):
    """
    Returns basic dataset statistics.
    """

    summary = {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Missing Values": int(df.isnull().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum())

    }

    return summary


def column_information(df):
    """
    Returns information about every column.
    """

    info = pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str),

        "Missing Values": df.isnull().sum(),

        "Unique Values": df.nunique()

    })

    return info