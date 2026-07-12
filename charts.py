import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# BAR CHART
# =====================================================

def create_bar_chart(df, column):

    fig = px.bar(

        df,

        x=column,

        title=f"{column} Distribution"

    )

    fig.update_layout(

        template="plotly_white"

    )

    return fig


# =====================================================
# LINE CHART
# =====================================================

def create_line_chart(df, column):

    fig = px.line(

        df,

        y=column,

        title=f"{column} Trend"

    )

    fig.update_layout(

        template="plotly_white"

    )

    return fig


# =====================================================
# HISTOGRAM
# =====================================================

def create_histogram(df, column):

    fig = px.histogram(

        df,

        x=column,

        nbins=30,

        title=f"{column} Histogram"

    )

    fig.update_layout(

        template="plotly_white"

    )

    return fig


# =====================================================
# BOX PLOT
# =====================================================

def create_box_plot(df, column):

    fig = px.box(

        df,

        y=column,

        title=f"{column} Box Plot"

    )

    fig.update_layout(

        template="plotly_white"

    )

    return fig


# =====================================================
# PIE CHART
# =====================================================

def create_pie_chart(df, column):

    values = df[column].value_counts()

    fig = px.pie(

        values=values.values,

        names=values.index,

        title=f"{column} Distribution"

    )

    return fig


# =====================================================
# SCATTER PLOT
# =====================================================

def create_scatter_plot(df, x_column, y_column):

    fig = px.scatter(

        df,

        x=x_column,

        y=y_column,

        title=f"{x_column} vs {y_column}"

    )

    fig.update_layout(

        template="plotly_white"

    )

    return fig


# =====================================================
# CORRELATION HEATMAP
# =====================================================

def create_correlation_heatmap(df):

    numeric = df.select_dtypes(include="number")

    corr = numeric.corr()

    fig = px.imshow(

        corr,

        text_auto=True,

        color_continuous_scale="Blues",

        title="Correlation Heatmap"

    )

    return fig


# =====================================================
# MISSING VALUES
# =====================================================

def create_missing_values_chart(df):

    missing = df.isnull().sum()

    fig = px.bar(

        x=missing.index,

        y=missing.values,

        labels={

            "x": "Columns",

            "y": "Missing Values"

        },

        title="Missing Values"

    )

    fig.update_layout(

        template="plotly_white"

    )

    return fig


# =====================================================
# KPI CARD
# =====================================================

def calculate_dataset_kpis(df):

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

        )

    }