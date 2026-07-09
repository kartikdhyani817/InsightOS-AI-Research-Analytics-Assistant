import streamlit as st
import pandas as pd

from utils import format_file_size

from csv_processor import (
    load_csv,
    dataset_summary,
    column_information
)

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

from ai_engine import (
    generate_ai_response,
    summarize_dataset
)

from rag_engine import (
    get_best_context
)

from report_generator import (
    generate_text_report,
    generate_executive_summary
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
# SESSION STATE
# ==========================================================

session_defaults = {

    "uploaded_file": None,

    "dataframe": None,

    "document_text": "",

    "pdf_info": {},

    "docx_info": {},

    "txt_info": {},

    "gemini_api_key": "",

    "ai_response": "",

    "report": ""

}

for key, value in session_defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

.block-container{

    padding-top:2rem;

}

.main-title{

    font-size:48px;

    font-weight:700;

    color:#2563EB;

}

.subtitle{

    color:#6B7280;

    font-size:18px;

}

.metric-card{

    background:#F9FAFB;

    border:1px solid #E5E7EB;

    border-radius:14px;

    padding:20px;

}

.feature-card{

    background:white;

    border-radius:15px;

    border:1px solid #E5E7EB;

    padding:20px;

    box-shadow:0px 2px 8px rgba(0,0,0,0.05);

}

.footer{

    text-align:center;

    color:gray;

    padding:20px;

    font-size:14px;

}

</style>
""",
    unsafe_allow_html=True
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🧠 InsightOS")

st.sidebar.caption("AI Research & Analytics Assistant")

st.sidebar.divider()

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Home",

        "📂 Upload Files",

        "📊 Analytics",

        "💬 AI Chat",

        "📄 Reports",

        "⚙️ Settings"

    ]

)

st.sidebar.divider()

st.sidebar.subheader("🔑 Gemini API")

api_key = st.sidebar.text_input(

    "API Key",

    type="password",

    value=st.session_state.gemini_api_key

)

st.session_state.gemini_api_key = api_key

if api_key:

    st.sidebar.success("Connected")

else:

    st.sidebar.warning("API Key not entered")

st.sidebar.divider()

if st.session_state.uploaded_file is not None:

    st.sidebar.success(

        f"Loaded\n\n{st.session_state.uploaded_file.name}"

    )

else:

    st.sidebar.info("No file uploaded")

st.sidebar.divider()

st.sidebar.caption("Version 2.0")

# ==========================================================
# HOME PAGE
# ==========================================================

if page == "🏠 Home":

    st.markdown(
        '<p class="main-title">🧠 InsightOS</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">AI Research & Analytics Assistant</p>',
        unsafe_allow_html=True
    )

    st.write(
        """
InsightOS is an AI-powered platform that enables users to upload documents and datasets,
analyze their contents, generate AI-powered insights, and create professional reports.
"""
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            """
<div class="feature-card">

### 📂 Upload Files

Upload CSV, PDF, DOCX and TXT files.

</div>
""",
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
<div class="feature-card">

### 🤖 AI Assistant

Chat with your documents using Gemini AI.

</div>
""",
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
<div class="feature-card">

### 📊 Analytics

Generate insights and visualize your data.

</div>
""",
            unsafe_allow_html=True
        )

    st.divider()

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Supported Files",
            "4"
        )

    with m2:

        st.metric(
            "AI Model",
            "Gemini"
        )

    with m3:

        st.metric(
            "Analytics",
            "Built-in"
        )

    with m4:

        st.metric(
            "Reports",
            "PDF Ready"
        )

# ==========================================================
# UPLOAD PAGE
# ==========================================================

elif page == "📂 Upload Files":

    st.title("📂 Upload Files")

    uploaded_file = st.file_uploader(

        "Upload a document",

        type=[

            "csv",

            "pdf",

            "txt",

            "docx"

        ]

    )

    if uploaded_file is None:

        st.info("Upload a file to begin.")

    else:

        st.session_state.uploaded_file = uploaded_file

        st.success("File uploaded successfully.")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "Filename",

                uploaded_file.name

            )

        with c2:

            st.metric(

                "Type",

                uploaded_file.type

            )

        with c3:

            st.metric(

                "Size",

                format_file_size(uploaded_file.size)

            )

        st.divider()

        # ==================================================
        # CSV
        # ==================================================

        if uploaded_file.name.lower().endswith(".csv"):

            try:

                df = load_csv(uploaded_file)

                st.session_state.dataframe = df

                summary = dataset_summary(df)

                a, b, c, d = st.columns(4)

                with a:

                    st.metric(
                        "Rows",
                        summary["Rows"]
                    )

                with b:

                    st.metric(
                        "Columns",
                        summary["Columns"]
                    )

                with c:

                    st.metric(
                        "Missing",
                        summary["Missing Values"]
                    )

                with d:

                    st.metric(
                        "Duplicates",
                        summary["Duplicate Rows"]
                    )

                st.divider()

                st.subheader("Dataset Preview")

                st.dataframe(
                    df,
                    use_container_width=True
                )

            except Exception as e:

                st.error(str(e))

        # ==================================================
        # PDF
        # ==================================================

        elif uploaded_file.name.lower().endswith(".pdf"):

            info = get_pdf_information(uploaded_file)

            text = extract_pdf_text(uploaded_file)

            st.session_state.document_text = text

            st.session_state.pdf_info = info

            if info is not None:

                a, b = st.columns(2)

                with a:

                    st.metric(
                        "Pages",
                        info["Pages"]
                    )

                with b:

                    st.metric(
                        "Encrypted",
                        str(info["Encrypted"])
                    )

            st.divider()

            st.subheader("PDF Preview")

            st.text_area(

                "Extracted Text",

                text,

                height=350

            )

        # ==================================================
        # DOCX
        # ==================================================

        elif uploaded_file.name.lower().endswith(".docx"):

            text = extract_docx_text(uploaded_file)

            info = get_docx_information(uploaded_file)

            st.session_state.document_text = text

            st.session_state.docx_info = info

            if info is not None:

                a, b, c = st.columns(3)

                with a:

                    st.metric(
                        "Paragraphs",
                        info["Paragraphs"]
                    )

                with b:

                    st.metric(
                        "Tables",
                        info["Tables"]
                    )

                with c:

                    st.metric(
                        "Sections",
                        info["Sections"]
                    )

            st.divider()

            st.subheader("DOCX Preview")

            st.text_area(

                "Extracted Text",

                text,

                height=350

            )

        # ==================================================
        # TXT
        # ==================================================

        elif uploaded_file.name.lower().endswith(".txt"):

            text = extract_txt_text(uploaded_file)

            info = get_txt_information(text)

            st.session_state.document_text = text

            st.session_state.txt_info = info

            a, b, c = st.columns(3)

            with a:

                st.metric(
                    "Characters",
                    info["Characters"]
                )

            with b:

                st.metric(
                    "Words",
                    info["Words"]
                )

            with c:

                st.metric(
                    "Lines",
                    info["Lines"]
                )

            st.divider()

            st.subheader("TXT Preview")

            st.text_area(

                "Extracted Text",

                text,

                height=350

            )

# ==========================================================
# ANALYTICS PAGE
# ==========================================================

elif page == "📊 Analytics":

    st.title("📊 Analytics Dashboard")

    if st.session_state.dataframe is None:

        st.warning("Please upload a CSV file first.")

    else:

        df = st.session_state.dataframe

        summary = dataset_summary(df)

        a, b, c, d = st.columns(4)

        with a:

            st.metric(
                "Rows",
                summary["Rows"]
            )

        with b:

            st.metric(
                "Columns",
                summary["Columns"]
            )

        with c:

            st.metric(
                "Missing Values",
                summary["Missing Values"]
            )

        with d:

            st.metric(
                "Duplicate Rows",
                summary["Duplicate Rows"]
            )

        st.divider()

        st.subheader("Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.divider()

        st.subheader("Column Information")

        column_info = column_information(df)

        st.dataframe(
            column_info,
            use_container_width=True
        )

        st.divider()

        st.subheader("Statistical Summary")

        try:

            st.dataframe(

                df.describe(include="all"),

                use_container_width=True

            )

        except Exception:

            st.info("No statistical summary available.")

        st.divider()

        st.subheader("Missing Values")

        missing = df.isnull().sum()

        st.bar_chart(missing)

# ==========================================================
# AI CHAT PAGE
# ==========================================================

elif page == "💬 AI Chat":

    st.title("🤖 AI Research Assistant")

    if st.session_state.uploaded_file is None:

        st.warning(
            "Please upload a document first."
        )

    else:

        st.success(

            f"Current File : {st.session_state.uploaded_file.name}"

        )

        st.divider()

        if st.session_state.document_text != "":

            c1, c2 = st.columns(2)

            with c1:

                st.metric(

                    "Characters",

                    len(st.session_state.document_text)

                )

            with c2:

                st.metric(

                    "Words",

                    len(

                        st.session_state.document_text.split()

                    )

                )

            st.subheader("Document Preview")

            st.text_area(

                "Preview",

                st.session_state.document_text[:3000],

                height=220

            )

        elif st.session_state.dataframe is not None:

            st.info(

                "CSV dataset loaded successfully."

            )

            st.dataframe(

                st.session_state.dataframe.head(),

                use_container_width=True

            )

        else:

            st.info(

                "No readable document content found."

            )

        st.divider()

        question = st.text_input(

            "Ask InsightOS"

        )

        if st.button(

            "Generate AI Response",

            use_container_width=True

        ):

            if not st.session_state.gemini_api_key:

                st.error(

                    "Please enter your Gemini API Key from the sidebar."

                )

            elif question.strip() == "":

                st.warning(

                    "Please enter a question."

                )

            else:

                with st.spinner(

                    "InsightOS is thinking..."

                ):

                    try:

                        # ==========================================
                        # DATASET SUMMARY
                        # ==========================================

                        if (

                            st.session_state.dataframe

                            is not None

                            and

                            st.session_state.document_text == ""

                        ):

                            answer = summarize_dataset(

                                st.session_state.gemini_api_key,

                                st.session_state.dataframe

                            )

                        # ==========================================
                        # DOCUMENT QA
                        # ==========================================

                        else:

                            context = get_best_context(

                                st.session_state.document_text,

                                question

                            )

                            answer = generate_ai_response(

                                st.session_state.gemini_api_key,

                                context,

                                question

                            )

                        st.session_state.ai_response = answer

                    except Exception as e:

                        st.error(str(e))

        if st.session_state.ai_response != "":

            st.divider()

            st.subheader("AI Response")

            st.write(

                st.session_state.ai_response

            )

# ==========================================================
# REPORTS PAGE
# ==========================================================

elif page == "📄 Reports":

    st.title("📄 AI Reports")

    if (

        st.session_state.dataframe is None

        and

        st.session_state.document_text == ""

    ):

        st.warning(

            "Please upload a document or dataset first."

        )

    else:

        st.subheader("Executive Summary")

        if st.session_state.dataframe is not None:

            summary = generate_executive_summary(

                st.session_state.dataframe

            )

            st.success(summary)

            st.divider()

            if st.button(

                "Generate Full Report",

                use_container_width=True

            ):

                with st.spinner(

                    "Generating report..."

                ):

                    report = generate_text_report(

                        st.session_state.dataframe

                    )

                    st.session_state.report = report

        else:

            st.info(

                "Document report generation will be available after AI analysis."

            )

        if st.session_state.report != "":

            st.divider()

            st.subheader("Generated Report")

            st.text_area(

                "Report",

                st.session_state.report,

                height=350

            )

            st.download_button(

                label="📥 Download Report",

                data=st.session_state.report,

                file_name="InsightOS_Report.txt",

                mime="text/plain",

                use_container_width=True

            )

# ==========================================================
# SETTINGS PAGE
# ==========================================================

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.subheader("Application Information")

    info = {

        "Application": "InsightOS",

        "Version": "2.0",

        "Framework": "Streamlit",

        "Programming Language": "Python",

        "AI Model": "Google Gemini",

        "Document Search": "RAG Enabled"

    }

    st.json(info)

    st.divider()

    st.subheader("Supported File Types")

    st.success("✅ CSV")

    st.success("✅ PDF")

    st.success("✅ DOCX")

    st.success("✅ TXT")

    st.divider()

    st.subheader("Installed Modules")

    st.success("✅ CSV Processor")

    st.success("✅ PDF Processor")

    st.success("✅ DOCX Processor")

    st.success("✅ TXT Processor")

    st.success("✅ AI Engine")

    st.success("✅ RAG Engine")

    st.success("✅ Report Generator")

    st.divider()

    if st.button(

        "Clear Session",

        use_container_width=True

    ):

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        st.success(

            "Session cleared successfully."

        )

        st.rerun()

# ==========================================================
# KPI DASHBOARD
# ==========================================================

if st.session_state.dataframe is not None:

    st.divider()

    st.subheader("📈 Dataset KPIs")

    df = st.session_state.dataframe

    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) > 0:

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(

                "Numeric Columns",

                len(numeric_columns)

            )

        with c2:

            st.metric(

                "Total Cells",

                df.shape[0] * df.shape[1]

            )

        with c3:

            st.metric(

                "Memory Usage",

                f"{round(df.memory_usage(deep=True).sum()/1024,2)} KB"

            )

        with c4:

            st.metric(

                "Complete Rows",

                len(df.dropna())

            )

# ==========================================================
# DATA VISUALIZATION
# ==========================================================

if page == "📊 Analytics":

    if st.session_state.dataframe is not None:

        df = st.session_state.dataframe

        numeric_columns = df.select_dtypes(

            include="number"

        ).columns.tolist()

        if len(numeric_columns) > 0:

            st.divider()

            st.subheader("📊 Interactive Charts")

            chart_type = st.selectbox(

                "Choose Visualization",

                [

                    "Histogram",

                    "Line Chart",

                    "Bar Chart",

                    "Area Chart"

                ]

            )

            column = st.selectbox(

                "Select Numeric Column",

                numeric_columns

            )

            if chart_type == "Histogram":

                st.bar_chart(

                    df[column].value_counts().head(25)

                )

            elif chart_type == "Line Chart":

                st.line_chart(

                    df[column]

                )

            elif chart_type == "Bar Chart":

                st.bar_chart(

                    df[column]

                )

            elif chart_type == "Area Chart":

                st.area_chart(

                    df[column]

                )

        st.divider()

        st.subheader("📋 Dataset Information")

        info_df = pd.DataFrame(

            {

                "Column":

                    df.columns,

                "Data Type":

                    df.dtypes.astype(str),

                "Missing":

                    df.isnull().sum().values,

                "Unique":

                    df.nunique().values

            }

        )

        st.dataframe(

            info_df,

            use_container_width=True

        )

# ==========================================================
# FILE INFORMATION
# ==========================================================

if st.session_state.uploaded_file is not None:

    st.divider()

    with st.expander("📂 Current Session"):

        st.write(

            f"**Filename:** {st.session_state.uploaded_file.name}"

        )

        st.write(

            f"**Size:** {format_file_size(st.session_state.uploaded_file.size)}"

        )

        st.write(

            f"**Type:** {st.session_state.uploaded_file.type}"

        )

# ==========================================================
# ABOUT
# ==========================================================

with st.sidebar:

    st.divider()

    st.markdown("### 🚀 About")

    st.caption(

        """
InsightOS is an AI-powered Research &
Analytics Assistant built using

• Python

• Streamlit

• Pandas

• Google Gemini

• Retrieval-Augmented Generation (RAG)
"""
    )

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
    """
<div class="footer">

<b>🧠 InsightOS - AI Research & Analytics Assistant</b><br>

Built with ❤️ using Python, Streamlit, Pandas, Google Gemini & RAG

<br><br>

© 2026 Kartik Dhyani. All Rights Reserved.

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# GLOBAL EXCEPTION HANDLER
# ==========================================================

try:

    pass

except Exception as e:

    st.error(

        f"Unexpected Error : {e}"

    )

# ==========================================================
# APPLICATION STATUS
# ==========================================================

if st.session_state.uploaded_file is not None:

    st.sidebar.success("Application Ready")

else:

    st.sidebar.info("Waiting for file upload")

# ==========================================================
# DEVELOPMENT ROADMAP
# ==========================================================

with st.sidebar.expander("🛣 Roadmap"):

    st.markdown(
        """
### Completed

- CSV Analytics

- PDF Processing

- DOCX Processing

- TXT Processing

- AI Chat

- Gemini Integration

- Dataset Analytics

- Reports

- RAG Engine

---

### Coming Soon

- FAISS Vector Database

- LangChain Integration

- AI Executive Dashboard

- Power BI Style KPIs

- Interactive Plotly Visualizations

- AI Generated PDF Reports

- Multi-file Chat

- Voice Assistant

- SQL Database Connector

- Excel Analytics

- Authentication

- User Accounts
"""
    )

# ==========================================================
# DEBUG INFORMATION
# ==========================================================

with st.sidebar.expander("⚙ Debug"):

    st.write(

        "Session Variables:",

        len(st.session_state)

    )

    st.write(

        "Current Page:",

        page

    )

    if st.session_state.uploaded_file is not None:

        st.write(

            "Loaded File:",

            st.session_state.uploaded_file.name

        )

# ==========================================================
# END OF APPLICATION
# ==========================================================