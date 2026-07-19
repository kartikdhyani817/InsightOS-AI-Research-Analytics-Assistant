# InsightOS — AI Business Intelligence Platform

InsightOS is a Streamlit-based AI business intelligence platform that converts uploaded datasets and documents into dashboards, executive insights, forecasts, risk assessments, recommendations, and downloadable reports.

## Live Application

**Streamlit App:** `PASTE_YOUR_STREAMLIT_APP_URL_HERE`

### Demo Login

```text
Username: admin
Password: insightos123
```

> These credentials are only for the public portfolio demo. Do not upload confidential or sensitive data.

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
2. Sign in with the demo credentials.
3. Upload a supported dataset or document.
4. Explore dashboards, profiles, forecasts, risks, and recommendations.
5. Use AI chat to ask questions.
6. Export reports.

## Screenshots

Create:

```text
screenshots/
├── login.png
├── dashboard-light.png
├── dashboard-dark.png
├── data-quality.png
├── forecast.png
├── ai-chat.png
└── report-export.png
```

Then add:

```markdown
![InsightOS Dashboard](screenshots/dashboard-light.png)
![InsightOS Dark Theme](screenshots/dashboard-dark.png)
```

## Deployment

The application is deployed on Streamlit Community Cloud. Pushes to the connected GitHub repository trigger a rebuild.

```bash
git add .
git commit -m "Update InsightOS"
git push
```

## Security Notice

The current username and password are demo credentials stored for portfolio access. This is not production-grade authentication.

For production use:

- Store credentials outside the repository.
- Use OAuth or an identity provider.
- Add role-based permissions.
- Validate upload size and type.
- Never process confidential data in the public demo.

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
