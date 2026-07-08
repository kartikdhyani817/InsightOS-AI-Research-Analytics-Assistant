# 🧠 InsightOS – AI Research & Analytics Assistant

InsightOS is an AI-powered research and analytics platform that enables users to upload documents and datasets, explore their contents, and prepare them for intelligent AI-driven analysis. The application is being developed as a modern workspace where data analytics and Artificial Intelligence come together to simplify document understanding and business insights.

With a clean Streamlit interface and modular architecture, InsightOS is designed to support multiple file formats, interactive analytics, AI-powered conversations, and automated report generation.

---

# 🚀 What's New (Day 3)

Today's development focused on transforming the application from a basic file uploader into a structured document processing platform.

### ✅ Document Processing

* Added PDF text extraction using PyPDF2
* Extracted and displayed PDF metadata (page count & encryption status)
* Added extracted text preview for uploaded PDF files
* Stored extracted document text in session state for future AI interaction

### ✅ CSV Processing

* Moved CSV handling into a dedicated `csv_processor.py` module
* Improved CSV loading with support for multiple encodings
* Added dataset summary functions
* Added reusable column information utilities

### ✅ Application Improvements

* Rebuilt the application using a clean modular architecture
* Improved code organization for easier maintenance
* Added professional analytics page
* Added AI Chat interface foundation
* Added Reports and Settings pages
* Improved session state management

---

# ✨ Current Features

* 📂 Upload CSV, PDF, TXT, and DOCX files
* 📄 Extract text from PDF documents
* 📊 Dataset preview and analytics
* 📈 Dataset statistics and column information
* 🤖 AI Chat interface (ready for Gemini integration)
* 📑 Professional multi-page Streamlit interface
* ⚙ Modular project structure for scalability

---

# 🛠️ Technology Stack

### Frontend

* Streamlit

### Programming

* Python

### Data Analysis

* Pandas
* NumPy

### Document Processing

* PyPDF2
* PyPDF
* Python-Docx

### Visualization

* Plotly
* Matplotlib

### Artificial Intelligence *(Upcoming)*

* Google Gemini API
* LangChain

### Future Components

* FAISS / ChromaDB
* ReportLab
* Retrieval-Augmented Generation (RAG)

---

# 📅 Development Progress

## ✅ Completed

* Project initialization
* Professional Streamlit UI
* Sidebar navigation
* Multi-format file upload
* CSV preview
* Dataset statistics
* PDF text extraction
* PDF metadata extraction
* Analytics dashboard
* AI Chat interface
* Reports page
* Settings page
* Modular codebase

## 🚧 In Progress

* DOCX text extraction
* Google Gemini integration
* AI-powered document question answering
* Executive report generation

## 🔜 Planned

* Retrieval-Augmented Generation (RAG)
* AI document summarization
* Interactive visualizations
* Downloadable PDF reports
* Cloud deployment optimization
* User authentication

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Kartik Dhyani**

Passionate about Artificial Intelligence, Data Analytics, Data Engineering, and building intelligent software solutions that transform raw data into actionable insights.

