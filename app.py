# ==========================================================
# STANDARD LIBRARIES
# ==========================================================

import os
import io
import tempfile

# ==========================================================
# THIRD PARTY LIBRARIES
# ==========================================================

import pandas as pd
import numpy as np
import streamlit as st

# ==========================================================
# LOCAL MODULES
# ==========================================================

# Authentication
from auth import (
    authenticate,
    login,
    logout,
    is_logged_in,
    current_user
)

# Theme
from theme import (
    apply_theme,
    theme_switch,
    initialize_theme,
    current_theme
)

# CSV
from csv_processor import (
    load_csv,
    dataset_summary,
    dataset_profile,
    numeric_summary,
    datatype_summary,
    memory_usage,
    missing_value_report,
    column_information,
    data_quality_score
)

# Documents
from pdf_processor import (
    extract_pdf_text,
    get_pdf_information
)

from docx_processor import (
    extract_docx_text,
    get_docx_information
)

from txt_processor import (
    extract_txt_text,
    get_txt_information
)

# Charts
from charts import *

# AI
from ai_engine import (
    generate_ai_response,
    summarize_dataset,
    executive_insights,
    dataset_health_score,
    kpi_summary
)

# Reports
from report_generator import (
    executive_summary,
    column_summary,
    generate_pdf_report,
    build_ai_report_prompt
)

# Search
from search_engine import (
    global_search,
    search_columns,
    top_matches
)

# Chat
from chat_manager import (
    initialize_chat,
    add_message,
    clear_chat,
    export_chat,
    chat_statistics
)

# Excel Export
from excel_export import (
    export_excel_report
)

# Dashboard Builder
from dashboard_builder import (
    build_dashboard,
    generate_kpis,
    recommend_charts,
    dataset_health
)

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
# INITIALIZE THEME
# ==========================================================

initialize_theme()

apply_theme()

# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULT_SESSION = {

    "logged_in": False,

    "uploaded_file": None,

    "dataframe": None,

    "document_text": "",

    "pdf_info": {},

    "docx_info": {},

    "txt_info": {},

    "chat_history": initialize_chat(),

    "gemini_api_key": "",

    "ai_response": "",

    "report": "",

    "dashboard": None

}

for key, value in DEFAULT_SESSION.items():

    if key not in st.session_state:

        st.session_state[key] = value

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


def reset_workspace():

    st.session_state.uploaded_file = None

    st.session_state.dataframe = None

    st.session_state.document_text = ""

    st.session_state.pdf_info = {}

    st.session_state.docx_info = {}

    st.session_state.txt_info = {}

    st.session_state.ai_response = ""

    st.session_state.report = ""

    st.session_state.dashboard = None

    st.session_state.chat_history = initialize_chat()


# ==========================================================
# ADAPTIVE CUSTOM CSS
# ==========================================================

# Streamlit applies parts of its own theme, while the application also uses
# custom HTML cards. These variables keep every custom component readable in
# both light and dark modes.
_dark_mode = current_theme() == "Dark"

_theme_colors = {
    "page": "#0B1220" if _dark_mode else "#F6F8FC",
    "surface": "#111827" if _dark_mode else "#FFFFFF",
    "surface_2": "#172033" if _dark_mode else "#F8FAFC",
    "text": "#F8FAFC" if _dark_mode else "#111827",
    "muted": "#CBD5E1" if _dark_mode else "#5B6472",
    "border": "#334155" if _dark_mode else "#D9E0EA",
    "accent": "#60A5FA" if _dark_mode else "#2563EB",
    "accent_soft": "#1E3A5F" if _dark_mode else "#EAF2FF",
    "input": "#0F172A" if _dark_mode else "#FFFFFF",
    "hover": "#24324A" if _dark_mode else "#EEF4FF",
    "success": "#4ADE80" if _dark_mode else "#15803D",
    "warning": "#FBBF24" if _dark_mode else "#B45309",
    "danger": "#FB7185" if _dark_mode else "#BE123C",
}

st.markdown(
    f"""
<style>
:root {{
    --ios-page: {_theme_colors['page']};
    --ios-surface: {_theme_colors['surface']};
    --ios-surface-2: {_theme_colors['surface_2']};
    --ios-text: {_theme_colors['text']};
    --ios-muted: {_theme_colors['muted']};
    --ios-border: {_theme_colors['border']};
    --ios-accent: {_theme_colors['accent']};
    --ios-accent-soft: {_theme_colors['accent_soft']};
    --ios-input: {_theme_colors['input']};
    --ios-hover: {_theme_colors['hover']};
}}

html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: var(--ios-page) !important;
    color: var(--ios-text) !important;
}}

.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}}

/* Global typography */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp p, .stApp li, .stApp label, .stApp span {{
    color: var(--ios-text);
}}

.main-title {{
    font-size: 42px;
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--ios-accent) !important;
}}

.sub-title {{
    color: var(--ios-muted) !important;
    font-size: 18px;
}}

.feature-card {{
    background: linear-gradient(145deg, var(--ios-surface), var(--ios-surface-2));
    border: 1px solid var(--ios-border);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 15px;
    color: var(--ios-text) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, {"0.20" if _dark_mode else "0.06"});
    transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
}}

.feature-card:hover {{
    transform: translateY(-2px);
    border-color: var(--ios-accent);
    box-shadow: 0 12px 28px rgba(0, 0, 0, {"0.28" if _dark_mode else "0.10"});
}}

.feature-card h1, .feature-card h2, .feature-card h3,
.feature-card h4, .feature-card strong {{
    color: var(--ios-text) !important;
}}

.feature-card p, .feature-card small {{
    color: var(--ios-muted) !important;
}}

.footer {{
    text-align: center;
    color: var(--ios-muted) !important;
    margin-top: 40px;
    font-size: 13px;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: var(--ios-surface) !important;
    border-right: 1px solid var(--ios-border);
}}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    color: var(--ios-text) !important;
}}

/* Metric cards */
div[data-testid="stMetric"] {{
    background: var(--ios-surface) !important;
    border: 1px solid var(--ios-border);
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, {"0.18" if _dark_mode else "0.05"});
}}
[data-testid="stMetricLabel"] *, [data-testid="stMetricValue"] *,
[data-testid="stMetricDelta"] * {{
    color: var(--ios-text) !important;
}}

/* Inputs, text areas and select boxes */
.stTextInput input, .stNumberInput input, .stTextArea textarea,
[data-baseweb="input"] input {{
    background: var(--ios-input) !important;
    color: var(--ios-text) !important;
    border-color: var(--ios-border) !important;
    -webkit-text-fill-color: var(--ios-text) !important;
}}
input::placeholder, textarea::placeholder {{
    color: var(--ios-muted) !important;
    opacity: 1;
}}
[data-baseweb="select"] > div {{
    background: var(--ios-input) !important;
    color: var(--ios-text) !important;
    border-color: var(--ios-border) !important;
}}
[data-baseweb="select"] span {{ color: var(--ios-text) !important; }}
[data-baseweb="popover"], [role="listbox"] {{
    background: var(--ios-surface) !important;
}}
[role="option"] {{
    background: var(--ios-surface) !important;
    color: var(--ios-text) !important;
}}
[role="option"]:hover {{ background: var(--ios-hover) !important; }}

/* Buttons */
.stButton > button, .stDownloadButton > button,
.stFormSubmitButton > button {{
    border: 1px solid var(--ios-border) !important;
    border-radius: 10px !important;
}}
.stButton > button:not([kind="primary"]),
.stDownloadButton > button {{
    background: var(--ios-surface) !important;
    color: var(--ios-text) !important;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    border-color: var(--ios-accent) !important;
    color: var(--ios-accent) !important;
}}

/* Tabs and radio navigation */
button[data-baseweb="tab"] {{ color: var(--ios-muted) !important; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color: var(--ios-accent) !important; }}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {{
    background: var(--ios-hover);
    border-radius: 8px;
}}

/* Expanders, upload areas and chat */
[data-testid="stExpander"], [data-testid="stFileUploaderDropzone"],
[data-testid="stChatMessage"] {{
    background: var(--ios-surface) !important;
    border-color: var(--ios-border) !important;
    color: var(--ios-text) !important;
}}
[data-testid="stFileUploaderDropzone"] * {{ color: var(--ios-text) !important; }}

/* Tables/dataframes */
[data-testid="stDataFrame"], [data-testid="stTable"] {{
    background: var(--ios-surface) !important;
    border: 1px solid var(--ios-border);
    border-radius: 12px;
    overflow: hidden;
}}

/* Code, JSON and dividers */
pre, code {{
    background: var(--ios-input) !important;
    color: var(--ios-text) !important;
}}
hr {{ border-color: var(--ios-border) !important; }}
[data-testid="stCaptionContainer"] {{ color: var(--ios-muted) !important; }}

/* Alerts retain readable text in both modes */
[data-testid="stAlert"] p, [data-testid="stAlert"] div {{
    color: inherit !important;
}}

/* Plotly container blends with the selected theme */
.js-plotly-plot, .plot-container, .svg-container {{
    border-radius: 12px;
}}
</style>
""",
    unsafe_allow_html=True,
)



# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/artificial-intelligence.png",
        width=70
    )

    st.title("InsightOS")

    st.caption("AI Business Intelligence Platform")

    st.divider()

    theme_switch()

    st.divider()

    page = st.radio(

        "Navigation",

        [

            "🏠 Home",

            "📂 Upload Files",

            "📊 Analytics",

            "🤖 AI Chat",

            "📄 Reports",

            "🔍 Search",

            "📊 Auto Dashboard",

            "⚙ Settings"

        ]

    )

    st.divider()

    st.subheader("Session")

    st.write(

        f"👤 **User:** {current_user(st.session_state)}"

    )

    if st.session_state.uploaded_file is not None:

        st.success("Dataset Loaded")

        st.write(

            st.session_state.uploaded_file.name

        )

        st.caption(

            format_file_size(

                st.session_state.uploaded_file.size

            )

        )

    else:

        st.info("No file uploaded")

    st.divider()

    st.subheader("Gemini API")

    st.session_state.gemini_api_key = st.text_input(

        "API Key",

        value=st.session_state.gemini_api_key,

        type="password"

    )

    st.divider()

    if st.button(

        "🗑 Reset Workspace",

        use_container_width=True

    ):

        reset_workspace()

        st.rerun()

    if st.button(

        "🚪 Logout",

        use_container_width=True

    ):

        logout(

            st.session_state

        )

        st.rerun()


# ==========================================================
# APPLICATION HEADER
# ==========================================================

st.markdown(

    '<div class="main-title">🧠 InsightOS</div>',

    unsafe_allow_html=True

)

st.markdown(

    '<div class="sub-title">Enterprise AI Business Intelligence Platform</div>',

    unsafe_allow_html=True

)

st.divider()


# ==========================================================
# GLOBAL STATUS BAR
# ==========================================================

status1, status2, status3 = st.columns(3)

with status1:

    if st.session_state.dataframe is not None:

        st.success("📊 Dataset Ready")

    else:

        st.info("📂 No Dataset")

with status2:

    if st.session_state.gemini_api_key != "":

        st.success("🤖 Gemini Connected")

    else:

        st.warning("🔑 API Missing")

with status3:

    stats = chat_statistics(

        st.session_state.chat_history

    )

    st.info(

        f"💬 {stats['Total Messages']} Messages"

    )

st.divider()

# ==========================================================
# HOME PAGE
# ==========================================================

if page == "🏠 Home":

    st.markdown("## 👋 Welcome to InsightOS")

    st.write(
        """
InsightOS is an **AI-powered Business Intelligence Platform**
that helps you analyze datasets, generate business insights,
build dashboards and create professional reports.
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

<h4>📂 Smart Upload</h4>

• CSV

• PDF

• DOCX

• TXT

Upload multiple business documents and datasets.

</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
<div class="feature-card">

<h4>🤖 AI Assistant</h4>

• Gemini AI

• Executive Insights

• Dataset Summary

• Business Recommendations

</div>
""",
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
<div class="feature-card">

<h4>📊 Analytics</h4>

• Interactive Charts

• KPI Cards

• Reports

• Dashboard Builder

</div>
""",
            unsafe_allow_html=True
        )

    st.divider()

    # ======================================================
    # QUICK STATS
    # ======================================================

    st.subheader("🚀 Platform Overview")

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(

            "Supported Files",

            "4"

        )

    with s2:

        st.metric(

            "AI Engine",

            "Gemini"

        )

    with s3:

        st.metric(

            "Charts",

            "Interactive"

        )

    with s4:

        st.metric(

            "Exports",

            "PDF + Excel"

        )

    st.divider()

    # ======================================================
    # TECHNOLOGY STACK
    # ======================================================

    st.subheader("🛠 Technology Stack")

    left, right = st.columns(2)

    with left:

        st.markdown("""

### Backend

- Python

- Pandas

- NumPy

- Streamlit

- OpenPyXL

""")

    with right:

        st.markdown("""

### Artificial Intelligence

- Google Gemini

- Plotly

- ReportLab

- Business Intelligence

""")

    st.divider()

    # ======================================================
    # GETTING STARTED
    # ======================================================

    st.subheader("📖 Quick Start")

    st.info(
        """
1️⃣ Upload your dataset

2️⃣ Open Analytics

3️⃣ Explore charts

4️⃣ Ask AI questions

5️⃣ Generate Reports

6️⃣ Export PDF or Excel
"""
    )

    st.divider()

    # ======================================================
    # CURRENT SESSION
    # ======================================================

    st.subheader("📂 Current Session")

    if st.session_state.uploaded_file is None:

        st.warning("No dataset or document uploaded.")

    else:

        st.success("Current File")

        st.write(

            f"**Name:** {st.session_state.uploaded_file.name}"

        )

        st.write(

            f"**Size:** {format_file_size(st.session_state.uploaded_file.size)}"

        )

    st.divider()

    st.caption(
        "InsightOS v4.0 • Enterprise AI Business Intelligence Platform"
    )

# ==========================================================
# UPLOAD PAGE
# ==========================================================

elif page == "📂 Upload Files":

    st.header("📂 Upload Files")

    uploaded_file = st.file_uploader(

        "Choose a file",

        type=[

            "csv",

            "pdf",

            "docx",

            "txt"

        ]

    )

    if uploaded_file is None:

        st.info("Upload a CSV, PDF, DOCX or TXT file.")

    else:

        st.session_state.uploaded_file = uploaded_file

        extension = uploaded_file.name.split(".")[-1].lower()

        try:

            # ==================================================
            # CSV FILE
            # ==================================================

            if extension == "csv":

                with st.spinner("Loading dataset..."):

                    df = load_csv(uploaded_file)

                    st.session_state.dataframe = df

                    st.session_state.document_text = ""

                st.success("Dataset loaded successfully.")

                summary = dataset_summary(df)

                c1, c2, c3, c4 = st.columns(4)

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

                    use_container_width=True,

                    height=400

                )

            # ==================================================
            # PDF FILE
            # ==================================================

            elif extension == "pdf":

                with st.spinner("Reading PDF..."):

                    text = extract_pdf_text(uploaded_file)

                    info = get_pdf_information(uploaded_file)

                st.session_state.document_text = text

                st.session_state.pdf_info = info

                st.session_state.dataframe = None

                st.success("PDF loaded successfully.")

                st.subheader("Document Information")

                st.json(info)

                st.subheader("Preview")

                st.text_area(

                    "",

                    text[:5000],

                    height=350

                )

            # ==================================================
            # DOCX FILE
            # ==================================================

            elif extension == "docx":

                with st.spinner("Reading DOCX..."):

                    text = extract_docx_text(uploaded_file)

                    info = get_docx_information(uploaded_file)

                st.session_state.document_text = text

                st.session_state.docx_info = info

                st.session_state.dataframe = None

                st.success("DOCX loaded successfully.")

                st.subheader("Document Information")

                st.json(info)

                st.subheader("Preview")

                st.text_area(

                    "",

                    text[:5000],

                    height=350

                )

            # ==================================================
            # TXT FILE
            # ==================================================

            elif extension == "txt":

                with st.spinner("Reading TXT..."):

                    text = extract_txt_text(uploaded_file)

                    info = get_txt_information(uploaded_file)

                st.session_state.document_text = text

                st.session_state.txt_info = info

                st.session_state.dataframe = None

                st.success("TXT loaded successfully.")

                st.subheader("File Information")

                st.json(info)

                st.subheader("Preview")

                st.text_area(

                    "",

                    text[:5000],

                    height=350

                )

        except Exception as e:

            st.error(

                f"Unable to process file.\n\n{e}"

            )

# ==========================================================
# ANALYTICS PAGE
# ==========================================================

elif page == "📊 Analytics":

    st.header("📊 Analytics Dashboard")

    if st.session_state.dataframe is None:

        st.warning("Please upload a CSV dataset first.")

    else:

        df = st.session_state.dataframe

        profile = dataset_profile(df)

        quality = data_quality_score(df)

        # ==================================================
        # KPI CARDS
        # ==================================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(

                "Rows",

                profile["Rows"]

            )

        with c2:

            st.metric(

                "Columns",

                profile["Columns"]

            )

        with c3:

            st.metric(

                "Memory",

                f"{profile['Memory (MB)']} MB"

            )

        with c4:

            st.metric(

                "Quality",

                f"{quality}%"

            )

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

                "📈 Statistics",

                "📊 Charts",

                "🧹 Data Quality",

                "🤖 AI Insights"

            ]

        )

        # ==================================================
        # STATISTICS
        # ==================================================

        with tab1:

            stats = numeric_summary(df)

            if not stats.empty:

                st.dataframe(

                    stats,

                    use_container_width=True

                )

            else:

                st.info(

                    "No numeric columns available."

                )

            st.divider()

            st.subheader("Column Information")

            st.dataframe(

                column_information(df),

                use_container_width=True

            )

        # ==================================================
        # CHARTS
        # ==================================================

        with tab2:

            numeric = df.select_dtypes(

                include="number"

            ).columns.tolist()

            categorical = df.select_dtypes(

                exclude="number"

            ).columns.tolist()

            chart = st.selectbox(

                "Chart Type",

                [

                    "Histogram",

                    "Box Plot",

                    "Bar Chart",

                    "Line Chart",

                    "Pie Chart",

                    "Scatter Plot",

                    "Correlation Heatmap"

                ]

            )

            if chart == "Histogram":

                if numeric:

                    column = st.selectbox(

                        "Column",

                        numeric,

                        key="hist"

                    )

                    st.plotly_chart(

                        create_histogram(df, column),

                        use_container_width=True

                    )

            elif chart == "Box Plot":

                if numeric:

                    column = st.selectbox(

                        "Column",

                        numeric,

                        key="box"

                    )

                    st.plotly_chart(

                        create_box_plot(df, column),

                        use_container_width=True

                    )

            elif chart == "Bar Chart":

                if numeric:

                    column = st.selectbox(

                        "Column",

                        numeric,

                        key="bar"

                    )

                    st.plotly_chart(

                        create_bar_chart(df, column),

                        use_container_width=True

                    )

            elif chart == "Line Chart":

                if numeric:

                    column = st.selectbox(

                        "Column",

                        numeric,

                        key="line"

                    )

                    st.plotly_chart(

                        create_line_chart(df, column),

                        use_container_width=True

                    )

            elif chart == "Pie Chart":

                if categorical:

                    column = st.selectbox(

                        "Category",

                        categorical,

                        key="pie"

                    )

                    st.plotly_chart(

                        create_pie_chart(df, column),

                        use_container_width=True

                    )

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

                    st.plotly_chart(

                        create_scatter_plot(

                            df,

                            x,

                            y

                        ),

                        use_container_width=True

                    )

            elif chart == "Correlation Heatmap":

                st.plotly_chart(

                    create_correlation_heatmap(df),

                    use_container_width=True

                )

        # ==================================================
        # DATA QUALITY
        # ==================================================

        with tab3:

            st.subheader("Missing Values")

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
        # AI INSIGHTS
        # ==================================================

        with tab4:

            st.subheader("AI Executive Insights")

            if st.button(

                "Generate Insights",

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

                        insight = executive_insights(

                            st.session_state.gemini_api_key,

                            df

                        )

                    st.success(insight)

# ==========================================================
# AI CHAT PAGE
# ==========================================================

elif page == "🤖 AI Chat":

    st.header("🤖 InsightOS AI Assistant")

    if (
        st.session_state.dataframe is None
        and
        st.session_state.document_text == ""
    ):

        st.warning(
            "Please upload a dataset or document first."
        )

    else:

        st.subheader("Conversation")

        # ==================================================
        # DISPLAY CHAT HISTORY
        # ==================================================

        if len(st.session_state.chat_history) == 0:

            st.info(
                "Start asking questions about your dataset or document."
            )

        else:

            for message in st.session_state.chat_history:

                with st.chat_message(message["role"]):

                    st.markdown(

                        message["message"]

                    )

        # ==================================================
        # SUGGESTED QUESTIONS
        # ==================================================

        with st.expander("💡 Suggested Questions"):

            st.markdown("""

- Summarize this dataset.

- What are the key business insights?

- Which columns have missing values?

- Explain the trends.

- Give recommendations.

- Find anomalies.

- Create an executive summary.

""")

        # ==================================================
        # USER INPUT
        # ==================================================

        prompt = st.chat_input(

            "Ask anything..."

        )

        if prompt:

            st.session_state.chat_history = add_message(

                st.session_state.chat_history,

                "user",

                prompt

            )

            with st.chat_message("user"):

                st.markdown(prompt)

            # ==============================================
            # CONTEXT
            # ==============================================

            if st.session_state.dataframe is not None:

                context = (

                    st.session_state.dataframe

                    .head(25)

                    .to_string()

                )

            else:

                context = (

                    st.session_state.document_text[:8000]

                )

            # ==============================================
            # AI RESPONSE
            # ==============================================

            with st.chat_message("assistant"):

                if st.session_state.gemini_api_key == "":

                    response = (

                        "Please enter your Gemini API Key."

                    )

                    st.error(response)

                else:

                    with st.spinner("Thinking..."):

                        response = generate_ai_response(

                            st.session_state.gemini_api_key,

                            context,

                            prompt

                        )

                    st.markdown(response)

            st.session_state.chat_history = add_message(

                st.session_state.chat_history,

                "assistant",

                response

            )

            st.rerun()

        st.divider()

        # ==================================================
        # CHAT TOOLS
        # ==================================================

        col1, col2 = st.columns(2)

        with col1:

            if st.button(

                "🗑 Clear Chat",

                use_container_width=True

            ):

                st.session_state.chat_history = clear_chat()

                st.rerun()

        with col2:

            chat_export = export_chat(

                st.session_state.chat_history

            )

            st.download_button(

                "📥 Export Chat",

                data=chat_export,

                file_name="InsightOS_Chat.txt",

                mime="text/plain",

                use_container_width=True

            )

        st.divider()

        # ==================================================
        # CHAT STATISTICS
        # ==================================================

        stats = chat_statistics(

            st.session_state.chat_history

        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "Total Messages",

                stats["Total Messages"]

            )

        with c2:

            st.metric(

                "User Messages",

                stats["User Messages"]

            )

        with c3:

            st.metric(

                "AI Messages",

                stats["AI Messages"]

            )

# ==========================================================
# REPORTS PAGE
# ==========================================================

elif page == "📄 Reports":

    st.header("📄 Executive Reports")

    if (
        st.session_state.dataframe is None
        and
        st.session_state.document_text == ""
    ):

        st.warning(
            "Please upload a dataset or document first."
        )

    else:

        # ==================================================
        # DATASET REPORT
        # ==================================================

        if st.session_state.dataframe is not None:

            df = st.session_state.dataframe

            st.subheader("📊 Executive Summary")

            summary = executive_summary(df)

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric("Rows", summary["Rows"])

            with col2:

                st.metric("Columns", summary["Columns"])

            with col3:

                st.metric("Missing", summary["Missing Values"])

            with col4:

                st.metric("Duplicates", summary["Duplicate Rows"])

            st.divider()

            # ==================================================
            # COLUMN SUMMARY
            # ==================================================

            st.subheader("📋 Column Profile")

            column_df = pd.DataFrame(

                column_summary(df),

                columns=[

                    "Column",

                    "Data Type",

                    "Missing",

                    "Unique Values"

                ]

            )

            st.dataframe(

                column_df,

                use_container_width=True

            )

            st.divider()

            # ==================================================
            # AI REPORT
            # ==================================================

            st.subheader("🤖 AI Executive Report")

            if st.button(

                "Generate AI Report",

                use_container_width=True

            ):

                if st.session_state.gemini_api_key == "":

                    st.error(

                        "Please enter your Gemini API Key."

                    )

                else:

                    with st.spinner(

                        "Generating report..."

                    ):

                        prompt = build_ai_report_prompt(df)

                        report = generate_ai_response(

                            st.session_state.gemini_api_key,

                            prompt,

                            "Generate a professional executive business report."

                        )

                        st.session_state.report = report

                    st.success(

                        "AI report generated successfully."

                    )

            if st.session_state.report != "":

                st.text_area(

                    "Report Preview",

                    st.session_state.report,

                    height=300

                )

                st.download_button(

                    "📥 Download AI Report",

                    data=st.session_state.report,

                    file_name="InsightOS_AI_Report.txt",

                    mime="text/plain",

                    use_container_width=True

                )

            st.divider()

            # ==================================================
            # PDF REPORT
            # ==================================================

            st.subheader("📄 PDF Report")

            if st.button(

                "Generate PDF",

                use_container_width=True

            ):

                with st.spinner(

                    "Creating PDF..."

                ):

                    pdf_file = generate_pdf_report(df)

                st.download_button(

                    "⬇ Download PDF Report",

                    data=pdf_file,

                    file_name="InsightOS_Report.pdf",

                    mime="application/pdf",

                    use_container_width=True

                )

            st.divider()

            # ==================================================
            # EXCEL REPORT
            # ==================================================

            st.subheader("📊 Excel Report")

            excel_file = export_excel_report(df)

            st.download_button(

                "⬇ Download Excel Report",

                data=excel_file,

                file_name="InsightOS_Report.xlsx",

                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                use_container_width=True

            )

        # ==================================================
        # DOCUMENT REPORT
        # ==================================================

        else:

            st.subheader("📄 Document Preview")

            st.text_area(

                "",

                st.session_state.document_text[:6000],

                height=400

            )

            st.info(

                "Use the AI Chat page to ask questions about the uploaded document."

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

        st.warning(
            "Please upload a dataset or document first."
        )

    else:

        query = st.text_input(

            "Search",

            placeholder="Search columns, values or document text..."

        )

        if query != "":

            # ==================================================
            # DATASET SEARCH
            # ==================================================

            if st.session_state.dataframe is not None:

                st.subheader("📊 Dataset Search")

                results = top_matches(

                    st.session_state.dataframe,

                    query,

                    limit=50

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

                    st.info(

                        "No matching rows found."

                    )

                st.divider()

                # ==============================================
                # COLUMN SEARCH
                # ==============================================

                st.subheader("🏷 Matching Columns")

                matched_columns = search_columns(

                    st.session_state.dataframe,

                    query

                )

                if len(matched_columns) > 0:

                    st.success(

                        ", ".join(matched_columns)

                    )

                else:

                    st.info(

                        "No matching columns."

                    )

            # ==================================================
            # DOCUMENT SEARCH
            # ==================================================

            if st.session_state.document_text != "":

                st.divider()

                st.subheader("📄 Document Search")

                search_result = global_search(

                    document_text=st.session_state.document_text,

                    query=query

                )

                document_matches = search_result["document"]

                if len(document_matches) > 0:

                    st.success(

                        f"{len(document_matches)} matches found."

                    )

                    for item in document_matches:

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

        # ==================================================
        # DATASET EXPLORER
        # ==================================================

        if st.session_state.dataframe is not None:

            st.divider()

            st.subheader("📂 Dataset Explorer")

            df = st.session_state.dataframe

            selected_column = st.selectbox(

                "Select Column",

                df.columns.tolist()

            )

            st.metric(

                "Unique Values",

                df[selected_column].nunique()

            )

            st.dataframe(

                df[[selected_column]].head(100),

                use_container_width=True,

                height=350

            )

            st.divider()

            st.subheader("📈 Column Statistics")

            if pd.api.types.is_numeric_dtype(df[selected_column]):

                c1, c2, c3, c4 = st.columns(4)

                with c1:

                    st.metric(

                        "Mean",

                        round(df[selected_column].mean(), 2)

                    )

                with c2:

                    st.metric(

                        "Median",

                        round(df[selected_column].median(), 2)

                    )

                with c3:

                    st.metric(

                        "Minimum",

                        round(df[selected_column].min(), 2)

                    )

                with c4:

                    st.metric(

                        "Maximum",

                        round(df[selected_column].max(), 2)

                    )

            else:

                st.info(

                    "Statistics available only for numeric columns."

                )

# ==========================================================
# AUTO DASHBOARD PAGE
# ==========================================================

elif page == "📊 Auto Dashboard":

    st.header("📊 AI Auto Dashboard Builder")

    if st.session_state.dataframe is None:

        st.warning(
            "Please upload a CSV dataset first."
        )

    else:

        df = st.session_state.dataframe

        if st.session_state.dashboard is None:

            st.session_state.dashboard = build_dashboard(df)

        dashboard = st.session_state.dashboard

        # ==================================================
        # DATASET HEALTH
        # ==================================================

        st.subheader("❤️ Dataset Health")

        health = dashboard["health"]

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:

            st.metric(

                "Rows",

                health["Rows"]

            )

        with c2:

            st.metric(

                "Columns",

                health["Columns"]

            )

        with c3:

            st.metric(

                "Missing",

                health["Missing Values"]

            )

        with c4:

            st.metric(

                "Duplicates",

                health["Duplicate Rows"]

            )

        with c5:

            st.metric(

                "Health Score",

                f'{health["Health Score"]}%'

            )

        st.divider()

        # ==================================================
        # SMART KPIs
        # ==================================================

        st.subheader("📈 Smart KPI Generator")

        kpis = dashboard["kpis"]

        if len(kpis) == 0:

            st.info(

                "No numeric columns available."

            )

        else:

            selected = st.selectbox(

                "Select Numeric Column",

                [item["Column"] for item in kpis]

            )

            current = next(

                item

                for item in kpis

                if item["Column"] == selected

            )

            a, b, c, d = st.columns(4)

            with a:

                st.metric(

                    "Sum",

                    current["Sum"]

                )

            with b:

                st.metric(

                    "Average",

                    current["Average"]

                )

            with c:

                st.metric(

                    "Maximum",

                    current["Maximum"]

                )

            with d:

                st.metric(

                    "Minimum",

                    current["Minimum"]

                )

        st.divider()

        # ==================================================
        # RECOMMENDED CHARTS
        # ==================================================

        st.subheader("🤖 Recommended Charts")

        recommended = dashboard["recommended_charts"]

        if len(recommended) > 0:

            for chart in recommended:

                st.success(chart)

        else:

            st.info(

                "No chart recommendations available."

            )

        st.divider()

        # ==================================================
        # EXPORT DASHBOARD
        # ==================================================

        st.subheader("📤 Export Dashboard")

        excel_file = export_excel_report(df)

        st.download_button(

            "⬇ Download Excel Dashboard",

            data=excel_file,

            file_name="InsightOS_Dashboard.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )

        st.divider()

        # ==================================================
        # AI SUMMARY
        # ==================================================

        st.subheader("🧠 AI Dataset Summary")

        if st.button(

            "Generate AI Summary",

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

                    summary = summarize_dataset(

                        st.session_state.gemini_api_key,

                        df

                    )

                st.success(summary)

# ==========================================================
# SETTINGS PAGE
# ==========================================================

elif page == "⚙ Settings":

    st.header("⚙ InsightOS Settings")

    # ======================================================
    # API STATUS
    # ======================================================

    st.subheader("🤖 Gemini AI")

    if st.session_state.gemini_api_key != "":

        st.success("Gemini API Connected")

    else:

        st.warning("Gemini API Key Not Added")

    st.divider()

    # ======================================================
    # APPLICATION INFORMATION
    # ======================================================

    st.subheader("📊 Application Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.session_state.dataframe is not None:

            st.metric(

                "Rows",

                len(st.session_state.dataframe)

            )

        else:

            st.metric(

                "Rows",

                0

            )

    with col2:

        if st.session_state.dataframe is not None:

            st.metric(

                "Columns",

                len(st.session_state.dataframe.columns)

            )

        else:

            st.metric(

                "Columns",

                0

            )

    with col3:

        st.metric(

            "Chat Messages",

            len(st.session_state.chat_history)

        )

    with col4:

        if st.session_state.uploaded_file is not None:

            st.metric(

                "File Loaded",

                "Yes"

            )

        else:

            st.metric(

                "File Loaded",

                "No"

            )

    st.divider()

    # ======================================================
    # PLATFORM FEATURES
    # ======================================================

    st.subheader("🚀 Platform Features")

    features = [

        "CSV Analytics",

        "PDF Analysis",

        "DOCX Analysis",

        "TXT Analysis",

        "AI Business Insights",

        "Interactive Charts",

        "Executive Reports",

        "Excel Export",

        "Universal Search",

        "Auto Dashboard",

        "AI Chat Assistant",

        "Dataset Health Score"

    ]

    for feature in features:

        st.success(feature)

    st.divider()

    # ======================================================
    # TECHNOLOGY STACK
    # ======================================================

    st.subheader("🛠 Technology Stack")

    tech1, tech2 = st.columns(2)

    with tech1:

        st.markdown("""

### Backend

- Python

- Pandas

- NumPy

- Streamlit

- OpenPyXL

- ReportLab

""")

    with tech2:

        st.markdown("""

### AI & Visualization

- Google Gemini

- Plotly

- Machine Learning Ready

- Business Intelligence

- Data Analytics

""")

    st.divider()

    # ======================================================
    # VERSION
    # ======================================================

    st.subheader("📦 Version")

    st.info("""

**InsightOS v4.0**

Enterprise AI Business Intelligence Platform

Developer: Kartik Dhyani

Build: Production Ready

Year: 2026

""")

    st.divider()

    # ======================================================
    # ABOUT
    # ======================================================

    st.subheader("ℹ About InsightOS")

    st.write("""

InsightOS is an enterprise-grade Business Intelligence platform
designed to simplify business analytics using Artificial Intelligence.

It enables users to upload datasets and business documents,
generate dashboards, create reports, visualize data,
perform AI-powered analysis, and interact with their data
through natural language.

""")

    st.divider()

    # ======================================================
    # FOOTER
    # ======================================================

    st.markdown("---")

    st.caption(

        "🧠 InsightOS v4.0 | Built with Python • Streamlit • Gemini AI"

    )

    st.caption(

        "© 2026 Kartik Dhyani"

    )

# ==========================================================
# FINAL APPLICATION STATUS
# ==========================================================

if st.session_state.dataframe is not None:

    st.sidebar.success("🟢 Dataset Ready")

elif st.session_state.document_text != "":

    st.sidebar.success("🟢 Document Ready")

else:

    st.sidebar.info("📂 Waiting for Upload")


if st.session_state.gemini_api_key != "":

    st.sidebar.success("🤖 AI Connected")

else:

    st.sidebar.warning("🔑 Gemini API Missing")


# ==========================================================
# PERFORMANCE INFORMATION
# ==========================================================

if st.session_state.dataframe is not None:

    with st.sidebar.expander("📊 Dataset Information"):

        st.write(

            f"Rows: {len(st.session_state.dataframe):,}"

        )

        st.write(

            f"Columns: {len(st.session_state.dataframe.columns)}"

        )

        memory = (

            st.session_state.dataframe.memory_usage(

                deep=True

            ).sum()

            / (1024 * 1024)

        )

        st.write(

            f"Memory: {memory:.2f} MB"

        )


# ==========================================================
# APPLICATION HEALTH
# ==========================================================

try:

    if st.session_state.dataframe is not None:

        _ = st.session_state.dataframe.shape

except Exception:

    st.sidebar.error(

        "Dataset session was reset."

    )

    st.session_state.dataframe = None


# ==========================================================
# APPLICATION FOOTER
# ==========================================================

st.markdown("---")

footer_left, footer_center, footer_right = st.columns(3)

with footer_left:

    st.caption("🧠 InsightOS v4.0")

with footer_center:

    st.caption("Enterprise AI Business Intelligence Platform")

with footer_right:

    st.caption("© 2026 Kartik Dhyani")


# ==========================================================
# END OF APPLICATION
# ==========================================================
