# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np

# CSV
from csv_processor import (
    load_csv,
    dataset_summary,
    dataset_profile,
    column_information,
    numeric_summary,
    missing_value_report,
    datatype_summary,
    memory_usage,
    data_quality_score
)

# PDF
from pdf_processor import (
    extract_pdf_text,
    get_pdf_information
)

# DOCX
from docx_processor import (
    extract_docx_text,
    get_docx_information
)

# TXT
from txt_processor import (
    extract_txt_text,
    get_txt_information
)

# AI
from ai_engine import (
    generate_ai_response,
    summarize_dataset,
    executive_insights,
    dataset_health_score,
    kpi_summary
)

# SEARCH
from search_engine import (
    global_search,
    search_columns,
    top_matches
)

# CHAT
from chat_manager import (
    initialize_chat,
    add_message,
    clear_chat,
    export_chat,
    chat_statistics
)

# REPORTS
from report_generator import (
    executive_summary,
    column_summary,
    generate_pdf_report,
    build_ai_report_prompt
)

# CHARTS
from charts import *

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(

    page_title="InsightOS",

    page_icon="🧠",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULT_SESSION = {

    "uploaded_file": None,

    "dataframe": None,

    "document_text": "",

    "chat_history": initialize_chat(),

    "gemini_api_key": "",

    "ai_response": "",

    "current_page": "Home",

    "pdf_info": {},

    "docx_info": {},

    "txt_info": {},

    "report": ""

}

for key, value in DEFAULT_SESSION.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

html,
body,
[class*="css"]{

    font-family:Arial,sans-serif;

}

.block-container{

    padding-top:1.8rem;

    padding-bottom:2rem;

}

.main-title{

    font-size:42px;

    font-weight:700;

    color:#2563EB;

}

.subtitle{

    font-size:18px;

    color:#6B7280;

}

.metric-card{

    background:white;

    border-radius:14px;

    border:1px solid #E5E7EB;

    padding:18px;

    box-shadow:0 2px 8px rgba(0,0,0,0.05);

}

.feature-card{

    background:#FFFFFF;

    border-radius:15px;

    border:1px solid #E5E7EB;

    padding:20px;

    box-shadow:0 3px 10px rgba(0,0,0,0.05);

}

.footer{

    text-align:center;

    color:gray;

    font-size:14px;

    padding:20px;

}

</style>
""",
    unsafe_allow_html=True
)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def format_file_size(size):

    if size < 1024:
        return f"{size} B"

    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"

    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"

    else:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"


def reset_uploaded_data():

    st.session_state.dataframe = None

    st.session_state.document_text = ""

    st.session_state.pdf_info = {}

    st.session_state.docx_info = {}

    st.session_state.txt_info = {}

    st.session_state.ai_response = ""

    st.session_state.report = ""


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("# 🧠 InsightOS")

    st.caption("AI Business Intelligence Platform")

    st.divider()

    st.subheader("Navigation")

    page = st.radio(

        "",

        [

            "🏠 Home",

            "📂 Upload Files",

            "📊 Analytics",

            "💬 AI Chat",

            "📄 Reports",

            "🔍 Search",

            "⚙️ Settings"

        ],

        label_visibility="collapsed"

    )

    st.session_state.current_page = page

    st.divider()

    st.subheader("Gemini API")

    api_key = st.text_input(

        "API Key",

        value=st.session_state.gemini_api_key,

        type="password",

        placeholder="Paste Gemini API Key"

    )

    st.session_state.gemini_api_key = api_key

    st.divider()

    st.subheader("Current Session")

    if st.session_state.uploaded_file is not None:

        st.success("File Loaded")

        st.write(

            f"**Name:** {st.session_state.uploaded_file.name}"

        )

        st.write(

            f"**Size:** {format_file_size(st.session_state.uploaded_file.size)}"

        )

    else:

        st.info("No file uploaded")

    st.divider()

    stats = chat_statistics(

        st.session_state.chat_history

    )

    st.metric(

        "Chat Messages",

        stats["Total Messages"]

    )

    st.metric(

        "Quality Score",

        "Ready"

        if st.session_state.dataframe is None

        else

        f"{data_quality_score(st.session_state.dataframe)}%"

    )

    st.divider()

    if st.button(

        "🗑 Clear Session",

        use_container_width=True

    ):

        uploaded = None

        api = st.session_state.gemini_api_key

        st.session_state.clear()

        for key, value in DEFAULT_SESSION.items():

            st.session_state[key] = value

        st.session_state.gemini_api_key = api

        st.session_state.uploaded_file = uploaded

        st.rerun()

# ==========================================================
# PAGE HEADER
# ==========================================================

st.markdown(

    '<div class="main-title">🧠 InsightOS</div>',

    unsafe_allow_html=True

)

st.markdown(

    '<div class="subtitle">AI Powered Research & Business Intelligence Platform</div>',

    unsafe_allow_html=True

)

st.divider()

# ==========================================================
# HOME PAGE
# ==========================================================

if page == "🏠 Home":

    st.markdown("## Welcome to InsightOS 👋")

    st.write(
        """
InsightOS is an **AI-powered Business Intelligence Platform** that helps you analyze datasets,
understand documents, generate business insights, and create professional reports using Google Gemini AI.
"""
    )

    st.divider()

    # ======================================================
    # FEATURE CARDS
    # ======================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
<div class="feature-card">

<h4>📂 Smart File Processing</h4>

Supports

- CSV
- PDF
- DOCX
- TXT

Upload and analyze files instantly.

</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
<div class="feature-card">

<h4>🤖 AI Assistant</h4>

Ask questions about

- Documents
- Datasets

Receive AI-powered business insights.

</div>
""",
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
<div class="feature-card">

<h4>📊 Business Intelligence</h4>

Generate

- KPIs
- Charts
- Reports
- Executive Summaries

within seconds.

</div>
""",
            unsafe_allow_html=True
        )

    st.divider()

    # ======================================================
    # PLATFORM OVERVIEW
    # ======================================================

    st.subheader("🚀 Platform Overview")

    a, b, c, d = st.columns(4)

    with a:

        st.metric(

            "Supported Files",

            "4"

        )

    with b:

        st.metric(

            "AI Powered",

            "Gemini"

        )

    with c:

        st.metric(

            "Analytics",

            "Interactive"

        )

    with d:

        st.metric(

            "Reports",

            "PDF"

        )

    st.divider()

    # ======================================================
    # TECHNOLOGY STACK
    # ======================================================

    st.subheader("🛠 Technology Stack")

    tech1, tech2 = st.columns(2)

    with tech1:

        st.markdown(
            """
### Backend

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
"""
        )

    with tech2:

        st.markdown(
            """
### Artificial Intelligence

- Google Gemini
- RAG
- Business Intelligence
- Executive Reporting
"""
        )

    st.divider()

    # ======================================================
    # QUICK START
    # ======================================================

    st.subheader("📖 Quick Start")

    st.info(
        """
1. Go to **📂 Upload Files**
2. Upload a CSV, PDF, DOCX, or TXT file
3. Open **📊 Analytics** to explore your data
4. Use **💬 AI Chat** to ask questions
5. Generate professional reports from **📄 Reports**
6. Search across your data using **🔍 Search**
"""
    )

    st.divider()

    # ======================================================
    # PROJECT FEATURES
    # ======================================================

    st.subheader("✨ Key Features")

    left, right = st.columns(2)

    with left:

        st.success("✅ Interactive Dashboard")
        st.success("✅ AI Executive Insights")
        st.success("✅ Universal Search")
        st.success("✅ Data Profiling")
        st.success("✅ KPI Cards")

    with right:

        st.success("✅ PDF Reports")
        st.success("✅ Chat History")
        st.success("✅ Multi-format Upload")
        st.success("✅ Plotly Visualizations")
        st.success("✅ Business Intelligence")

    st.divider()

    st.caption(
        "InsightOS v3.0 • AI-Powered Business Intelligence Platform"
    )

# ==========================================================
# UPLOAD FILES PAGE
# ==========================================================

elif page == "📂 Upload Files":

    st.header("📂 Upload Files")

    st.write(
        "Upload a CSV dataset or a document (PDF, DOCX, TXT) to begin analysis."
    )

    uploaded_file = st.file_uploader(

        "Choose a file",

        type=[

            "csv",

            "pdf",

            "docx",

            "txt"

        ]

    )

    if uploaded_file is not None:

        if (

            st.session_state.uploaded_file is None

            or

            uploaded_file.name != st.session_state.uploaded_file.name

        ):

            reset_uploaded_data()

            st.session_state.uploaded_file = uploaded_file

        extension = uploaded_file.name.split(".")[-1].lower()

        try:

            # ==================================================
            # CSV
            # ==================================================

            if extension == "csv":

                with st.spinner("Loading CSV dataset..."):

                    df = load_csv(uploaded_file)

                    st.session_state.dataframe = df

                st.success("CSV dataset loaded successfully.")

                c1, c2, c3, c4 = st.columns(4)

                summary = dataset_summary(df)

                with c1:
                    st.metric("Rows", summary["Rows"])

                with c2:
                    st.metric("Columns", summary["Columns"])

                with c3:
                    st.metric("Missing", summary["Missing Values"])

                with c4:
                    st.metric("Duplicates", summary["Duplicate Rows"])

                st.divider()

                st.subheader("Dataset Preview")

                st.dataframe(

                    df.head(20),

                    use_container_width=True

                )

            # ==================================================
            # PDF
            # ==================================================

            elif extension == "pdf":

                with st.spinner("Reading PDF..."):

                    text = extract_pdf_text(uploaded_file)

                    info = get_pdf_information(uploaded_file)

                st.session_state.document_text = text

                st.session_state.pdf_info = info

                st.success("PDF loaded successfully.")

                st.subheader("PDF Information")

                st.json(info)

                st.divider()

                st.subheader("Preview")

                st.text_area(

                    "Extracted Text",

                    text[:5000],

                    height=350

                )

            # ==================================================
            # DOCX
            # ==================================================

            elif extension == "docx":

                with st.spinner("Reading DOCX..."):

                    text = extract_docx_text(uploaded_file)

                    info = get_docx_information(uploaded_file)

                st.session_state.document_text = text

                st.session_state.docx_info = info

                st.success("DOCX loaded successfully.")

                st.subheader("Document Information")

                st.json(info)

                st.divider()

                st.text_area(

                    "Extracted Text",

                    text[:5000],

                    height=350

                )

            # ==================================================
            # TXT
            # ==================================================

            elif extension == "txt":

                with st.spinner("Reading TXT..."):

                    text = extract_txt_text(uploaded_file)

                    info = get_txt_information(uploaded_file)

                st.session_state.document_text = text

                st.session_state.txt_info = info

                st.success("TXT file loaded successfully.")

                st.subheader("File Information")

                st.json(info)

                st.divider()

                st.text_area(

                    "File Contents",

                    text[:5000],

                    height=350

                )

        except Exception as e:

            st.error(

                f"Error loading file: {e}"

            )

    else:

        st.info("No file uploaded.")

        st.markdown(
            """
### Supported Formats

- 📊 CSV (Business datasets)
- 📄 PDF (Reports & Documents)
- 📝 DOCX (Word Documents)
- 📃 TXT (Text Files)

Upload a supported file to continue.
"""
        )

# ==========================================================
# ANALYTICS PAGE
# ==========================================================

elif page == "📊 Analytics":

    st.header("📊 Executive Analytics Dashboard")

    if st.session_state.dataframe is None:

        st.warning("Please upload a CSV dataset first.")

    else:

        df = st.session_state.dataframe

        # ==================================================
        # DATASET PROFILE
        # ==================================================

        profile = dataset_profile(df)

        quality = data_quality_score(df)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Rows", profile["Rows"])

        with c2:
            st.metric("Columns", profile["Columns"])

        with c3:
            st.metric("Memory", f'{profile["Memory (MB)"]} MB')

        with c4:
            st.metric("Quality", f"{quality}%")

        st.divider()

        # ==================================================
        # DATA PREVIEW
        # ==================================================

        st.subheader("Dataset Preview")

        st.dataframe(

            df,

            use_container_width=True,

            height=350

        )

        st.divider()

        # ==================================================
        # ANALYTICS TABS
        # ==================================================

        tab1, tab2, tab3, tab4 = st.tabs(

            [

                "📊 Statistics",

                "📈 Charts",

                "🧹 Data Quality",

                "🤖 AI Insights"

            ]

        )

        # ==================================================
        # TAB 1
        # ==================================================

        with tab1:

            st.subheader("Numeric Statistics")

            numeric_df = numeric_summary(df)

            if not numeric_df.empty:

                st.dataframe(

                    numeric_df,

                    use_container_width=True

                )

            else:

                st.info("No numeric columns found.")

            st.divider()

            st.subheader("Column Information")

            st.dataframe(

                column_information(df),

                use_container_width=True

            )

        # ==================================================
        # TAB 2
        # ==================================================

        with tab2:

            numeric = df.select_dtypes(

                include="number"

            ).columns.tolist()

            categorical = df.select_dtypes(

                exclude="number"

            ).columns.tolist()

            chart = st.selectbox(

                "Visualization",

                [

                    "Bar Chart",

                    "Line Chart",

                    "Histogram",

                    "Box Plot",

                    "Pie Chart",

                    "Scatter Plot",

                    "Correlation Heatmap"

                ]

            )

            if chart != "Correlation Heatmap":

                if chart == "Pie Chart":

                    if len(categorical) > 0:

                        column = st.selectbox(

                            "Category",

                            categorical

                        )

                        fig = create_pie_chart(

                            df,

                            column

                        )

                        st.plotly_chart(

                            fig,

                            use_container_width=True

                        )

                    else:

                        st.info("No categorical columns available.")

                elif chart == "Scatter Plot":

                    if len(numeric) >= 2:

                        x = st.selectbox(

                            "X Axis",

                            numeric,

                            key="scatter_x"

                        )

                        y = st.selectbox(

                            "Y Axis",

                            numeric,

                            index=1,

                            key="scatter_y"

                        )

                        fig = create_scatter_plot(

                            df,

                            x,

                            y

                        )

                        st.plotly_chart(

                            fig,

                            use_container_width=True

                        )

                    else:

                        st.info("At least two numeric columns are required.")

                else:

                    if len(numeric) > 0:

                        column = st.selectbox(

                            "Numeric Column",

                            numeric

                        )

                        if chart == "Bar Chart":

                            fig = create_bar_chart(df, column)

                        elif chart == "Line Chart":

                            fig = create_line_chart(df, column)

                        elif chart == "Histogram":

                            fig = create_histogram(df, column)

                        else:

                            fig = create_box_plot(df, column)

                        st.plotly_chart(

                            fig,

                            use_container_width=True

                        )

                    else:

                        st.info("No numeric columns available.")

            else:

                fig = create_correlation_heatmap(df)

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

        # ==================================================
        # TAB 3
        # ==================================================

        with tab3:

            st.subheader("Missing Value Report")

            st.dataframe(

                missing_value_report(df),

                use_container_width=True

            )

            st.divider()

            st.subheader("Data Types")

            st.dataframe(

                datatype_summary(df),

                use_container_width=True

            )

            st.divider()

            st.subheader("Memory Usage")

            st.dataframe(

                memory_usage(df),

                use_container_width=True

            )

        # ==================================================
        # TAB 4
        # ==================================================

        with tab4:

            st.subheader("AI Executive Insights")

            if st.button(

                "Generate AI Insights",

                use_container_width=True

            ):

                if st.session_state.gemini_api_key == "":

                    st.error(

                        "Please enter your Gemini API Key."

                    )

                else:

                    with st.spinner(

                        "Analyzing dataset..."

                    ):

                        response = executive_insights(

                            st.session_state.gemini_api_key,

                            df

                        )

                        st.success(response)

# ==========================================================
# ANALYTICS PAGE
# ==========================================================

elif page == "📊 Analytics":

    st.header("📊 Executive Analytics Dashboard")

    if st.session_state.dataframe is None:

        st.warning("Please upload a CSV dataset first.")

    else:

        df = st.session_state.dataframe

        # ==================================================
        # DATASET PROFILE
        # ==================================================

        profile = dataset_profile(df)

        quality = data_quality_score(df)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Rows", profile["Rows"])

        with c2:
            st.metric("Columns", profile["Columns"])

        with c3:
            st.metric("Memory", f'{profile["Memory (MB)"]} MB')

        with c4:
            st.metric("Quality", f"{quality}%")

        st.divider()

        # ==================================================
        # DATA PREVIEW
        # ==================================================

        st.subheader("Dataset Preview")

        st.dataframe(

            df,

            use_container_width=True,

            height=350

        )

        st.divider()

        # ==================================================
        # ANALYTICS TABS
        # ==================================================

        tab1, tab2, tab3, tab4 = st.tabs(

            [

                "📊 Statistics",

                "📈 Charts",

                "🧹 Data Quality",

                "🤖 AI Insights"

            ]

        )

        # ==================================================
        # TAB 1
        # ==================================================

        with tab1:

            st.subheader("Numeric Statistics")

            numeric_df = numeric_summary(df)

            if not numeric_df.empty:

                st.dataframe(

                    numeric_df,

                    use_container_width=True

                )

            else:

                st.info("No numeric columns found.")

            st.divider()

            st.subheader("Column Information")

            st.dataframe(

                column_information(df),

                use_container_width=True

            )

        # ==================================================
        # TAB 2
        # ==================================================

        with tab2:

            numeric = df.select_dtypes(

                include="number"

            ).columns.tolist()

            categorical = df.select_dtypes(

                exclude="number"

            ).columns.tolist()

            chart = st.selectbox(

                "Visualization",

                [

                    "Bar Chart",

                    "Line Chart",

                    "Histogram",

                    "Box Plot",

                    "Pie Chart",

                    "Scatter Plot",

                    "Correlation Heatmap"

                ]

            )

            if chart != "Correlation Heatmap":

                if chart == "Pie Chart":

                    if len(categorical) > 0:

                        column = st.selectbox(

                            "Category",

                            categorical

                        )

                        fig = create_pie_chart(

                            df,

                            column

                        )

                        st.plotly_chart(

                            fig,

                            use_container_width=True

                        )

                    else:

                        st.info("No categorical columns available.")

                elif chart == "Scatter Plot":

                    if len(numeric) >= 2:

                        x = st.selectbox(

                            "X Axis",

                            numeric,

                            key="scatter_x"

                        )

                        y = st.selectbox(

                            "Y Axis",

                            numeric,

                            index=1,

                            key="scatter_y"

                        )

                        fig = create_scatter_plot(

                            df,

                            x,

                            y

                        )

                        st.plotly_chart(

                            fig,

                            use_container_width=True

                        )

                    else:

                        st.info("At least two numeric columns are required.")

                else:

                    if len(numeric) > 0:

                        column = st.selectbox(

                            "Numeric Column",

                            numeric

                        )

                        if chart == "Bar Chart":

                            fig = create_bar_chart(df, column)

                        elif chart == "Line Chart":

                            fig = create_line_chart(df, column)

                        elif chart == "Histogram":

                            fig = create_histogram(df, column)

                        else:

                            fig = create_box_plot(df, column)

                        st.plotly_chart(

                            fig,

                            use_container_width=True

                        )

                    else:

                        st.info("No numeric columns available.")

            else:

                fig = create_correlation_heatmap(df)

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

        # ==================================================
        # TAB 3
        # ==================================================

        with tab3:

            st.subheader("Missing Value Report")

            st.dataframe(

                missing_value_report(df),

                use_container_width=True

            )

            st.divider()

            st.subheader("Data Types")

            st.dataframe(

                datatype_summary(df),

                use_container_width=True

            )

            st.divider()

            st.subheader("Memory Usage")

            st.dataframe(

                memory_usage(df),

                use_container_width=True

            )

        # ==================================================
        # TAB 4
        # ==================================================

        with tab4:

            st.subheader("AI Executive Insights")

            if st.button(

                "Generate AI Insights",

                use_container_width=True

            ):

                if st.session_state.gemini_api_key == "":

                    st.error(

                        "Please enter your Gemini API Key."

                    )

                else:

                    with st.spinner(

                        "Analyzing dataset..."

                    ):

                        response = executive_insights(

                            st.session_state.gemini_api_key,

                            df

                        )

                        st.success(response)

# ==========================================================
# SEARCH PAGE
# ==========================================================

elif page == "🔍 Search":

    st.header("🔍 Universal Search")

    if (
        st.session_state.dataframe is None
        and
        st.session_state.document_text == ""
    ):

        st.warning("Please upload a dataset or document first.")

    else:

        search_query = st.text_input(

            "Search anything",

            placeholder="Example: Sales, Revenue, Delhi, Product A..."

        )

        if search_query:

            st.divider()

            # ============================================
            # SEARCH DATASET
            # ============================================

            if st.session_state.dataframe is not None:

                st.subheader("📊 Dataset Results")

                results = top_matches(

                    st.session_state.dataframe,

                    search_query,

                    limit=25

                )

                if len(results) > 0:

                    st.success(

                        f"{len(results)} matching rows found."

                    )

                    st.dataframe(

                        results,

                        use_container_width=True,

                        height=350

                    )

                else:

                    st.info("No matching rows found.")

                st.divider()

                st.subheader("🏷 Matching Columns")

                cols = search_columns(

                    st.session_state.dataframe,

                    search_query

                )

                if len(cols) > 0:

                    st.success(

                        ", ".join(cols)

                    )

                else:

                    st.info(

                        "No matching columns."

                    )

            # ============================================
            # SEARCH DOCUMENT
            # ============================================

            if st.session_state.document_text != "":

                st.divider()

                st.subheader("📄 Document Results")

                search_results = global_search(

                    document_text=st.session_state.document_text,

                    query=search_query

                )

                doc = search_results["document"]

                if doc:

                    st.success(

                        f"{len(doc)} matches found."

                    )

                    for item in doc:

                        st.markdown(

                            f"**Line {item['Line']}**"

                        )

                        st.write(

                            item["Text"]

                        )

                        st.divider()

                else:

                    st.info(

                        "No matches found."

                    )

        else:

            st.info(

                "Enter a keyword to begin searching."

            )

        # ===============================================
        # DATASET EXPLORER
        # ===============================================

        if st.session_state.dataframe is not None:

            st.divider()

            st.subheader("📂 Dataset Explorer")

            df = st.session_state.dataframe

            selected_column = st.selectbox(

                "Select Column",

                df.columns.tolist()

            )

            st.write(

                f"Unique Values: **{df[selected_column].nunique()}**"

            )

            st.dataframe(

                df[[selected_column]].head(100),

                use_container_width=True

            )

# ==========================================================
# SEARCH PAGE
# ==========================================================

elif page == "🔍 Search":

    st.header("🔍 Universal Search")

    if (
        st.session_state.dataframe is None
        and
        st.session_state.document_text == ""
    ):

        st.warning("Please upload a dataset or document first.")

    else:

        search_query = st.text_input(

            "Search anything",

            placeholder="Example: Sales, Revenue, Delhi, Product A..."

        )

        if search_query:

            st.divider()

            # ============================================
            # SEARCH DATASET
            # ============================================

            if st.session_state.dataframe is not None:

                st.subheader("📊 Dataset Results")

                results = top_matches(

                    st.session_state.dataframe,

                    search_query,

                    limit=25

                )

                if len(results) > 0:

                    st.success(

                        f"{len(results)} matching rows found."

                    )

                    st.dataframe(

                        results,

                        use_container_width=True,

                        height=350

                    )

                else:

                    st.info("No matching rows found.")

                st.divider()

                st.subheader("🏷 Matching Columns")

                cols = search_columns(

                    st.session_state.dataframe,

                    search_query

                )

                if len(cols) > 0:

                    st.success(

                        ", ".join(cols)

                    )

                else:

                    st.info(

                        "No matching columns."

                    )

            # ============================================
            # SEARCH DOCUMENT
            # ============================================

            if st.session_state.document_text != "":

                st.divider()

                st.subheader("📄 Document Results")

                search_results = global_search(

                    document_text=st.session_state.document_text,

                    query=search_query

                )

                doc = search_results["document"]

                if doc:

                    st.success(

                        f"{len(doc)} matches found."

                    )

                    for item in doc:

                        st.markdown(

                            f"**Line {item['Line']}**"

                        )

                        st.write(

                            item["Text"]

                        )

                        st.divider()

                else:

                    st.info(

                        "No matches found."

                    )

        else:

            st.info(

                "Enter a keyword to begin searching."

            )

        # ===============================================
        # DATASET EXPLORER
        # ===============================================

        if st.session_state.dataframe is not None:

            st.divider()

            st.subheader("📂 Dataset Explorer")

            df = st.session_state.dataframe

            selected_column = st.selectbox(

                "Select Column",

                df.columns.tolist()

            )

            st.write(

                f"Unique Values: **{df[selected_column].nunique()}**"

            )

            st.dataframe(

                df[[selected_column]].head(100),

                use_container_width=True

            )

# ==========================================================
# FINAL FOOTER
# ==========================================================

st.divider()

footer_col1, footer_col2 = st.columns([3, 1])

with footer_col1:

    st.caption(
        "🧠 InsightOS v3.0 | AI-Powered Business Intelligence Platform"
    )

with footer_col2:

    st.caption("© 2026 Kartik Dhyani")


# ==========================================================
# APPLICATION STATUS
# ==========================================================

if st.session_state.dataframe is not None:

    st.sidebar.success("🟢 Dataset Loaded")

elif st.session_state.document_text != "":

    st.sidebar.success("🟢 Document Loaded")

else:

    st.sidebar.info("📂 Waiting for Upload")


if st.session_state.gemini_api_key != "":

    st.sidebar.success("🤖 Gemini Connected")

else:

    st.sidebar.warning("🔑 Gemini API Missing")


# ==========================================================
# CACHE MANAGEMENT
# ==========================================================

try:

    if st.session_state.dataframe is not None:

        _ = st.session_state.dataframe.shape

except Exception:

    st.session_state.dataframe = None


# ==========================================================
# END OF APPLICATION
# ==========================================================