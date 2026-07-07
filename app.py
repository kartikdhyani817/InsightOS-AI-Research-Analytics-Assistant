import streamlit as st
import pandas as pd

from utils import format_file_size, load_csv

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="InsightOS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main-title{
    font-size:52px;
    font-weight:700;
    color:#2563EB;
}

.sub-title{
    font-size:20px;
    color:#555;
    margin-bottom:20px;
}

.card{

    background:#F8FAFC;
    padding:22px;
    border-radius:15px;
    border:1px solid #E5E7EB;
    text-align:center;

}

.metric{

    font-size:34px;
    font-weight:bold;
    color:#2563EB;

}

.metric-title{

    font-size:16px;
    color:#666;

}

.footer{

    text-align:center;
    color:gray;
    margin-top:40px;

}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

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

st.sidebar.info(
    "Upload your documents and datasets to unlock AI-powered insights."
)

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

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
InsightOS is an AI-powered platform that allows you to upload documents and datasets,
chat with them using Artificial Intelligence, generate analytics dashboards,
and create executive reports — all from one workspace.
"""
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
<div class="card">
<h2>📂</h2>
<h3>Multi File Upload</h3>
<p>Upload CSV, PDF, TXT and DOCX files.</p>
</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
<div class="card">
<h2>🤖</h2>
<h3>AI Assistant</h3>
<p>Ask questions in natural language and receive intelligent answers.</p>
</div>
""",
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
<div class="card">
<h2>📊</h2>
<h3>Analytics</h3>
<p>Create dashboards, charts and downloadable reports instantly.</p>
</div>
""",
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("🚀 Planned Features")

    feature1, feature2 = st.columns(2)

    with feature1:

        st.success("✔ AI Chat with Documents")

        st.success("✔ PDF & DOCX Understanding")

        st.success("✔ CSV Analytics")

        st.success("✔ Interactive Dashboards")

    with feature2:

        st.success("✔ Retrieval-Augmented Generation (RAG)")

        st.success("✔ AI Report Generation")

        st.success("✔ Executive PDF Reports")

        st.success("✔ Cloud Deployment")

    st.divider()

    st.markdown(
        '<p class="footer">Developed using Python • Streamlit • Gemini AI • LangChain</p>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------
# UPLOAD FILES PAGE
# ---------------------------------------------------

elif page == "📂 Upload Files":

    st.title("📂 Upload Files")

    st.write(
        "Upload CSV, PDF, TXT or DOCX files to start your analysis."
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

    if uploaded_file is not None:

        st.session_state.uploaded_file = uploaded_file

        st.subheader("📄 File Details")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Filename", uploaded_file.name)

        with col2:
            st.metric("File Type", uploaded_file.type)

        with col3:
            st.metric(
                "Size",
                format_file_size(uploaded_file.size)
            )

        st.divider()

        # ---------------- CSV ----------------

        if uploaded_file.name.lower().endswith(".csv"):

            try:

                df = load_csv(uploaded_file)

                st.session_state.dataframe = df

                st.success("✅ CSV loaded successfully!")

                st.write("### Dataset Preview")

                st.dataframe(
                    df,
                    use_container_width=True
                )

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric("Rows", len(df))

                with c2:
                    st.metric("Columns", len(df.columns))

                with c3:
                    st.metric(
                        "Missing Values",
                        int(df.isnull().sum().sum())
                    )

            except Exception as e:

                st.error(f"Unable to load CSV.\n\n{e}")

        # ---------------- TXT ----------------

        elif uploaded_file.name.lower().endswith(".txt"):

            try:

                uploaded_file.seek(0)

                text = uploaded_file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                st.success("✅ TXT loaded successfully!")

                st.text_area(

                    "Preview",

                    text[:5000],

                    height=300

                )

            except Exception as e:

                st.error(e)

        # ---------------- PDF ----------------

        elif uploaded_file.name.lower().endswith(".pdf"):

            st.success("✅ PDF uploaded successfully!")

            st.info(
                "PDF text extraction will be implemented in Day 3."
            )

        # ---------------- DOCX ----------------

        elif uploaded_file.name.lower().endswith(".docx"):

            st.success("✅ DOCX uploaded successfully!")

            st.info(
                "DOCX extraction will be implemented in Day 3."
            )

    else:

        st.info("Please upload a file to continue.")


# ---------------------------------------------------
# AI CHAT PAGE
# ---------------------------------------------------

elif page == "💬 AI Chat":

    st.title("🤖 AI Chat")

    if st.session_state.uploaded_file is None:

        st.warning("Please upload a file first.")

    else:

        st.success(
            f"Current File: {st.session_state.uploaded_file.name}"
        )

        user_question = st.text_input(
            "Ask a question about your uploaded document"
        )

        if st.button("Ask AI"):

            if user_question.strip() == "":

                st.warning("Please enter a question.")

            else:

                st.info(
                    "Gemini AI integration will be added in the next phase."
                )

# ---------------------------------------------------
# ANALYTICS PAGE
# ---------------------------------------------------

elif page == "📊 Analytics":

    st.title("📊 Analytics Dashboard")

    if st.session_state.dataframe is None:

        st.warning("Upload a CSV dataset first.")

    else:

        df = st.session_state.dataframe

        st.success("Dataset Loaded Successfully")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", len(df))

        with col2:
            st.metric("Columns", len(df.columns))

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        st.divider()

        st.subheader("Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("Column Information")

        info = pd.DataFrame({

            "Column": df.columns,

            "Data Type": df.dtypes.astype(str),

            "Missing Values": df.isnull().sum()

        })

        st.dataframe(
            info,
            use_container_width=True
        )

# ---------------------------------------------------
# REPORTS PAGE
# ---------------------------------------------------

elif page == "📄 Reports":

    st.title("📄 Reports")

    if st.session_state.uploaded_file is None:

        st.warning("Upload a file first.")

    else:

        st.success(
            f"Report will be generated for {st.session_state.uploaded_file.name}"
        )

        st.info(
            "PDF report generation will be implemented in the next phase."
        )

# ---------------------------------------------------
# SETTINGS PAGE
# ---------------------------------------------------

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.subheader("Application")

    st.write("Version: **1.0.0**")

    st.write("Developer: **Kartik Dhyani**")

    st.write("Framework: **Streamlit**")

    st.write("AI Model: **Google Gemini (Upcoming)**")

    st.divider()

    st.subheader("Project Status")

    st.success("InsightOS is under active development.")




