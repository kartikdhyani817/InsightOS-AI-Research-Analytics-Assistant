# InsightOS — AI Business Intelligence Platform

InsightOS is a Streamlit-based AI business intelligence platform that converts uploaded datasets and documents into dashboards, executive insights, forecasts, risk assessments, recommendations, and downloadable reports.

## Live Application

**Streamlit App:** `https://insightos-ai-research-analytics-assistant-gwayhlxt2s8xqwewe3zh.streamlit.app/`



## Main Features

- CSV and Excel data analysis
- PDF, DOCX, and TXT processing
- Dataset profiling and data-quality scoring
- Missing-value and duplicate detection
- Cleaning recommendations
- KPI recommendation and executive dashboards
- Interactive charts and chart explanations
- Forecasting and trend analysis
- Opportunity and risk detection
- Smart alerts
- AI-generated summaries and recommendations
- AI chat and search
- PDF and Excel exports
- Responsive light and dark themes

## Tech Stack

Python, Streamlit, Pandas, NumPy, Plotly, Matplotlib, Scikit-learn, Google Gemini, LangChain, FAISS, PyPDF2, python-docx, OpenPyXL, and ReportLab.

## Run Locally

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Secrets

Create `.streamlit/secrets.toml` locally:

```toml
GEMINI_API_KEY = "your-api-key"
```

Never commit real API keys or `secrets.toml`.

## How to Use

1. Open the live app.
2. Upload a supported dataset or document.
3. Explore dashboards, profiles, forecasts, risks, and recommendations.
4. Use AI chat to ask questions.
5. Export reports.


## Deployment

The application is deployed on Streamlit Community Cloud. Pushes to the connected GitHub repository trigger a rebuild.

```bash
git add .
git commit -m "Update InsightOS"
git push
```

## Security Notice



## Limitations

- AI-generated output should be reviewed.
- Forecast quality depends on the uploaded data.
- Very large files may exceed hosting limits.
- The demo login is not intended for sensitive deployments.

## Future Improvements

- Guest mode
- OAuth authentication
- Saved dashboards
- Multi-user workspaces
- Database-backed history
- More forecasting models
- Automated tests
- Docker support

## Author

**Kartik Dhyani**


- Live App: `(https://insightos-ai-research-analytics-assistant-gwayhlxt2s8xqwewe3zh.streamlit.app/)`

## License

MIT License
