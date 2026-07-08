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

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="InsightOS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE
# =====================================================

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "pdf_info" not in st.session_state:
    st.session_state.pdf_info = {}

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main-title{
    font-size:52px;
    font-weight:bold;
    color:#2563EB;
}

.sub-title{
    font-size:20px;
    color:#555555;
    margin-bottom:20px;
}

.card{
    background:#F8FAFC;
    border:1px solid #E5E7EB;
    border-radius:15px;
    padding:25px;
    text-align:center;
}

.metric-box{
    background:#F9FAFB;
    padding:15px;
    border-radius:12px;
    border:1px solid #E5E7EB;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🧠 InsightOS")

st.sidebar.markdown(
    "### AI Research & Analytics Assistant"
)

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Home",

        "📂 Upload Files",

        "💬 AI Chat",

        "📊 Analytics",

        "📄 Reports",

        "⚙️ Settings"

    ]

)

st.sidebar.markdown("---")

st.sidebar.success("Version 1.0")

# =====================================================
# HOME PAGE
# =====================================================

if page == "🏠 Home":

    st.markdown(
        '<p class="main-title">🧠 InsightOS</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sub-title">AI Research & Analytics Assistant</p>',
        unsafe_allow_html=True
    )

    st.write(
        """
InsightOS is an AI-powered platform that allows users to upload documents,
analyze datasets, generate reports, and interact with files using Artificial Intelligence.
"""
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
<div class="card">
<h2>📂</h2>
<h3>Upload Files</h3>
<p>CSV, PDF, DOCX and TXT support</p>
</div>
""", unsafe_allow_html=True)

    with col2:

        st.markdown("""
<div class="card">
<h2>🤖</h2>
<h3>AI Assistant</h3>
<p>Ask questions about your uploaded files.</p>
</div>
""", unsafe_allow_html=True)

    with col3:

        st.markdown("""
<div class="card">
<h2>📊</h2>
<h3>Analytics</h3>
<p>Create dashboards and business insights.</p>
</div>
""", unsafe_allow_html=True)

    st.divider()

    st.subheader("Project Features")

    left, right = st.columns(2)

    with left:

        st.success("✔ Multi-file Upload")

        st.success("✔ AI Chat")

        st.success("✔ PDF Processing")

        st.success("✔ CSV Analytics")

    with right:

        st.success("✔ Executive Reports")

        st.success("✔ Interactive Dashboard")

        st.success("✔ Gemini AI")

        st.success("✔ Cloud Deployment")

    st.divider()

    st.markdown(
        '<p class="footer">Developed by Kartik Dhyani | Python • Streamlit • Gemini AI</p>',
        unsafe_allow_html=True
    )

# =====================================================
# UPLOAD FILES PAGE
# =====================================================

elif page == "📂 Upload Files":

    st.title("📂 Upload Files")

    st.write(
        "Upload CSV, PDF, TXT or DOCX files for analysis."
    )

    uploaded_file = st.file_uploader(

        "Choose a file",

        type=[

            "csv",

            "pdf",

            "txt",

            "docx"

        ]

    )

    if uploaded_file is None:

        st.info("Please upload a file to continue.")

    else:

        st.session_state.uploaded_file = uploaded_file

        st.subheader("📄 File Information")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Filename",
                uploaded_file.name
            )

        with col2:

            st.metric(
                "Type",
                uploaded_file.type
            )

        with col3:

            st.metric(
                "Size",
                format_file_size(uploaded_file.size)
            )

        st.divider()

        # ======================================
        # CSV FILE
        # ======================================

        if uploaded_file.name.lower().endswith(".csv"):

            try:

                df = load_csv(uploaded_file)

                st.session_state.dataframe = df

                summary = dataset_summary(df)

                st.success("✅ CSV loaded successfully.")

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric("Rows", summary["Rows"])

                with c2:
                    st.metric("Columns", summary["Columns"])

                with c3:
                    st.metric(
                        "Missing",
                        summary["Missing Values"]
                    )

                with c4:
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

                st.error(f"Error loading CSV: {e}")

        # ======================================
        # PDF FILE
        # ======================================

        elif uploaded_file.name.lower().endswith(".pdf"):

            pdf_info = get_pdf_information(uploaded_file)

            extracted_text = extract_pdf_text(uploaded_file)

            st.session_state.document_text = extracted_text

            if pdf_info is not None:

                c1, c2 = st.columns(2)

                with c1:
                    st.metric(
                        "Pages",
                        pdf_info["Pages"]
                    )

                with c2:
                    st.metric(
                        "Encrypted",
                        str(pdf_info["Encrypted"])
                    )

            st.divider()

            st.subheader("Extracted Text")

            st.text_area(

                "PDF Preview",

                extracted_text[:5000],

                height=350

            )

        # ======================================
        # TXT FILE
        # ======================================

        elif uploaded_file.name.lower().endswith(".txt"):

            uploaded_file.seek(0)

            text = uploaded_file.read().decode(

                "utf-8",

                errors="ignore"

            )

            st.session_state.document_text = text

            st.success("TXT loaded successfully.")

            st.text_area(

                "TXT Preview",

                text[:5000],

                height=350

            )

        # ======================================
        # DOCX FILE
        # ======================================

        elif uploaded_file.name.lower().endswith(".docx"):

            st.success("DOCX uploaded successfully.")

            st.info(
                "DOCX text extraction will be implemented in the next update."
            )
# =====================================================
# AI CHAT PAGE
# =====================================================

elif page == "💬 AI Chat":

    st.title("🤖 AI Research Assistant")

    if st.session_state.uploaded_file is None:

        st.warning("Please upload a document first.")

    else:

        st.success(
            f"Current File : {st.session_state.uploaded_file.name}"
        )

        if st.session_state.document_text == "":

            st.info(
                "No document text available.\n\nUpload a PDF or TXT file first."
            )

        else:

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Characters",
                    len(st.session_state.document_text)
                )

            with col2:

                st.metric(
                    "Words",
                    len(
                        st.session_state.document_text.split()
                    )
                )

            st.divider()

            st.subheader("Document Preview")

            st.text_area(

                "Extracted Content",

                st.session_state.document_text[:3000],

                height=250

            )

            st.divider()

            question = st.text_input(
                "Ask a question about your document"
            )

            if st.button("Ask AI"):

                if question.strip() == "":

                    st.warning(
                        "Please enter a question."
                    )

                else:

                    st.success("Question Submitted")

                    st.write("### Your Question")

                    st.info(question)

                    st.write("### AI Response")

                    st.warning(
                        "Gemini AI integration will be added in the next development phase."
                    )

# =====================================================
# ANALYTICS PAGE
# =====================================================

elif page == "📊 Analytics":

    st.title("📊 Analytics Dashboard")

    if st.session_state.dataframe is None:

        st.warning(
            "Please upload a CSV dataset first."
        )

    else:

        df = st.session_state.dataframe

        summary = dataset_summary(df)

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Rows",
                summary["Rows"]
            )

        with c2:

            st.metric(
                "Columns",
                summary["Columns"]
            )

        with c3:

            st.metric(
                "Missing Values",
                summary["Missing Values"]
            )

        with c4:

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

        info = column_information(df)

        st.dataframe(
            info,
            use_container_width=True
        )

        st.divider()

        st.subheader("Numeric Summary")

        st.dataframe(
            df.describe(),
            use_container_width=True
        )
# =====================================================
# REPORTS PAGE
# =====================================================

elif page == "📄 Reports":

    st.title("📄 Reports")

    if st.session_state.uploaded_file is None:

        st.warning("Please upload a file first.")

    else:

        st.success(
            f"Current File : {st.session_state.uploaded_file.name}"
        )

        st.write("### Report Status")

        st.info(
            """
Executive report generation will be implemented in the next phase.

Upcoming Features:

• AI Executive Summary

• Key Insights

• Business Recommendations

• Download PDF Report

• Download Word Report

• Charts & Visualizations
"""
        )

        st.button(
            "Generate Report",
            disabled=True,
            use_container_width=True
        )

# =====================================================
# SETTINGS PAGE
# =====================================================

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.subheader("Application")

    st.write("**Application Name:** InsightOS")

    st.write("**Version:** 1.0.0")

    st.write("**Framework:** Streamlit")

    st.write("**Language:** Python")

    st.write("**AI Model:** Google Gemini (Coming Soon)")

    st.divider()

    st.subheader("Project Modules")

    st.success("✔ Multi-format File Upload")

    st.success("✔ CSV Analytics")

    st.success("✔ PDF Text Extraction")

    st.success("✔ Session Management")

    st.success("✔ AI Chat Interface")

    st.success("✔ Analytics Dashboard")

    st.success("✔ Report Generation Module")

    st.divider()

    st.subheader("Developer")

    st.info(
        """
Kartik Dhyani

MSc Data Analytics

InsightOS – AI Research & Analytics Assistant
"""
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
<div style="text-align:center;color:gray;font-size:14px;padding:15px;">

🧠 <b>InsightOS</b> | AI Research & Analytics Assistant

Built using Python, Streamlit, Pandas & Google Gemini

</div>
""",
    unsafe_allow_html=True
)