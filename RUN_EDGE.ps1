# PowerShell script to run Streamlit app
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Emotion-Aware Text-to-Speech Tutor" -ForegroundColor Green
Write-Host " Opening in your default browser" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "The app will open automatically in your default browser!" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the app" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run Streamlit with auto-open browser (overrides config.toml headless setting)
# The --server.headless=false flag ensures browser opens automatically in default browser
streamlit run app.py --server.headless=false --browser.gatherUsageStats=false --server.runOnSave=true

