import streamlit as st

st.set_page_config(
    page_title="InsightOS",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>

.main-title{
    font-size:48px;
    font-weight:bold;
    color:#2563EB;
}

.sub-title{
    font-size:20px;
    color:#555555;
}

.feature-card{
    padding:20px;
    border-radius:15px;
    background:#F5F7FA;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("🧠 InsightOS")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📂 Upload Files",
        "💬 AI Chat",
        "📊 Analytics",
        "📄 Reports",
        "⚙ Settings"
    ]
)

if page=="🏠 Home":

    st.markdown(
        '<p class="main-title">InsightOS</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sub-title">AI Research & Analytics Assistant</p>',
        unsafe_allow_html=True
    )

    st.write("---")

    col1,col2,col3=st.columns(3)

    with col1:
        st.info("📂 Upload PDFs, CSVs and Text Files")

    with col2:
        st.success("🤖 Chat with your documents using AI")

    with col3:
        st.warning("📊 Generate analytics and reports")

    st.write("---")

    st.header("About")

    st.write("""
InsightOS is an AI-powered platform that allows users to upload documents and datasets,
analyze information, ask questions in natural language,
generate visualizations, and create executive reports.

This project combines Artificial Intelligence,
Data Analytics,
and Retrieval-Augmented Generation (RAG)
into one intelligent workspace.
""")