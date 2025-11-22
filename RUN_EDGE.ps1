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

# Start Streamlit in background
$streamlitProcess = Start-Process -FilePath "streamlit" -ArgumentList "run", "app.py", "--server.headless=false", "--browser.gatherUsageStats=false" -NoNewWindow -PassThru

# Wait for Streamlit to start
Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Open in default browser (Streamlit should do this automatically, but ensure it opens)
Write-Host "Opening in your default browser..." -ForegroundColor Green
Start-Process "http://localhost:8501"

Write-Host ""
Write-Host "App is running in your default browser!" -ForegroundColor Green
Write-Host "URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""

# Wait for the Streamlit process
try {
    Wait-Process -Id $streamlitProcess.Id
} catch {
    Write-Host "App stopped." -ForegroundColor Yellow
}

