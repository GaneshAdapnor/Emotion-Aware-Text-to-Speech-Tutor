# PowerShell script to run Streamlit app
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Emotion-Aware Text-to-Speech Tutor" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "The app will open automatically in your browser!" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the app" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run Streamlit (it will automatically open in browser)
streamlit run app.py --server.headless=false --browser.gatherUsageStats=false

