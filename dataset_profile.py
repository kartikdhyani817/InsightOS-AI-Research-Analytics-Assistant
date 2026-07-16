# ==========================================================
# dataset_profile.py
# InsightOS Enterprise Dataset Profiler
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# BASIC PROFILE
# ==========================================================

def basic_profile(df):

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Memory Usage (MB)": round(

            df.memory_usage(deep=True).sum()

            / (1024 * 1024),

            2

        ),

        "Duplicate Rows": int(

            df.duplicated().sum()

        )

    }


# ==========================================================
# COLUMN PROFILE
# ==========================================================

def column_profile(df):

    profile = []

    for column in df.columns:

        profile.append({

            "Column": column,

            "Type": str(df[column].dtype),

            "Missing": int(df[column].isnull().sum()),

            "Unique": int(df[column].nunique()),

            "Missing %": round(

                (

                    df[column].isnull().sum()

                    / len(df)

                ) * 100,

                2

            )

        })

    return pd.DataFrame(profile)


# ==========================================================
# NUMERIC PROFILE
# ==========================================================

def numeric_profile(df):

    numeric = df.select_dtypes(include=np.number)

    if numeric.empty:

        return pd.DataFrame()

    profile = pd.DataFrame({

        "Mean": numeric.mean(),

        "Median": numeric.median(),

        "Std": numeric.std(),

        "Minimum": numeric.min(),

        "Maximum": numeric.max(),

        "Missing": numeric.isnull().sum()

    })

    return profile.round(2)


# ==========================================================
# CATEGORICAL PROFILE
# ==========================================================

def categorical_profile(df):

    categorical = df.select_dtypes(

        include=["object", "category"]

    )

    rows = []

    for column in categorical.columns:

        rows.append({

            "Column": column,

            "Unique Categories": categorical[column].nunique(),

            "Most Frequent":

                categorical[column].mode().iloc[0]

                if not categorical[column].mode().empty

                else None,

            "Frequency":

                int(

                    categorical[column]

                    .value_counts()

                    .iloc[0]

                )

                if not categorical[column]

                .value_counts()

                .empty

                else 0

        })

    return pd.DataFrame(rows)


# ==========================================================
# MEMORY PROFILE
# ==========================================================

def memory_profile(df):

    memory = []

    for column in df.columns:

        memory.append({

            "Column": column,

            "Memory (KB)": round(

                df[column]

                .memory_usage(

                    deep=True

                )

                / 1024,

                2

            )

        })

    return pd.DataFrame(memory)


# ==========================================================
# COMPLETE PROFILE
# ==========================================================

def generate_dataset_profile(df):

    return {

        "Basic":

            basic_profile(df),

        "Columns":

            column_profile(df),

        "Numeric":

            numeric_profile(df),

        "Categorical":

            categorical_profile(df),

        "Memory":

            memory_profile(df)

    }