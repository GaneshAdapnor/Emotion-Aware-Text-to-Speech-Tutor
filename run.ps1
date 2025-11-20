# PowerShell script to run Streamlit app
Write-Host "Starting Emotion-Aware Text-to-Speech Tutor..." -ForegroundColor Green
Write-Host ""

# Run Streamlit (it will automatically open in browser)
streamlit run app.py --server.headless=false

