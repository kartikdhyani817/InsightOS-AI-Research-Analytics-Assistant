import pandas as pd


# =====================================================
# LOAD CSV
# =====================================================

def load_csv(file):

    encodings = [

        "utf-8",

        "latin-1",

        "cp1252"

    ]

    for encoding in encodings:

        try:

            file.seek(0)

            return pd.read_csv(

                file,

                encoding=encoding,

                low_memory=False

            )

        except Exception:

            continue

    raise Exception(

        "Unable to read the CSV file."

    )


# =====================================================
# DATASET SUMMARY
# =====================================================

def dataset_summary(df):

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Missing Values": int(df.isnull().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum())

    }


# =====================================================
# COLUMN INFORMATION
# =====================================================

def column_information(df):

    info = pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str),

        "Missing": df.isnull().sum().values,

        "Unique": df.nunique().values

    })

    return info


# =====================================================
# DATASET PROFILE
# =====================================================

def dataset_profile(df):

    memory = round(

        df.memory_usage(

            deep=True

        ).sum() / (1024 * 1024),

        2

    )

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Memory (MB)": memory,

        "Numeric Columns": len(

            df.select_dtypes(

                include="number"

            ).columns

        ),

        "Categorical Columns": len(

            df.select_dtypes(

                exclude="number"

            ).columns

        ),

        "Missing Values": int(

            df.isnull().sum().sum()

        ),

        "Duplicate Rows": int(

            df.duplicated().sum()

        )

    }


# =====================================================
# DATA QUALITY SCORE
# =====================================================

def data_quality_score(df):

    total = len(df) * len(df.columns)

    if total == 0:

        return 0

    missing = int(

        df.isnull().sum().sum()

    )

    duplicate = int(

        df.duplicated().sum()

    )

    score = 100

    score -= (missing / total) * 100

    score -= (duplicate / max(len(df), 1)) * 10

    score = max(

        0,

        min(100, round(score))

    )

    return score


# =====================================================
# NUMERIC SUMMARY
# =====================================================

def numeric_summary(df):

    numeric = df.select_dtypes(

        include="number"

    )

    if numeric.empty:

        return pd.DataFrame()

    return numeric.describe().transpose()


# =====================================================
# MISSING VALUE REPORT
# =====================================================

def missing_value_report(df):

    report = pd.DataFrame({

        "Column": df.columns,

        "Missing": df.isnull().sum().values,

        "Percentage":

            (

                df.isnull().sum()

                / len(df)

                * 100

            ).round(2).values

    })

    return report.sort_values(

        "Missing",

        ascending=False

    )


# =====================================================
# DATA TYPES
# =====================================================

def datatype_summary(df):

    return pd.DataFrame({

        "Data Type":

            df.dtypes.value_counts().index.astype(str),

        "Count":

            df.dtypes.value_counts().values

    })


# =====================================================
# TOP CATEGORIES
# =====================================================

def top_categories(df, column, limit=10):

    return (

        df[column]

        .value_counts()

        .head(limit)

    )


# =====================================================
# MEMORY USAGE
# =====================================================

def memory_usage(df):

    usage = df.memory_usage(

        deep=True

    )

    return pd.DataFrame({

        "Column": usage.index,

        "Memory (Bytes)": usage.values

    })