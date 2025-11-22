# PowerShell script to run Streamlit app
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Emotion-Aware Text-to-Speech Tutor" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "The app will open automatically in your default browser!" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the app" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Streamlit in background
Write-Host "Starting Streamlit server..." -ForegroundColor Yellow
$streamlitJob = Start-Job -ScriptBlock {
    streamlit run app.py --server.headless=false --browser.gatherUsageStats=false --server.runOnSave=true
}

# Wait for server to start
Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 4

# Explicitly open browser
Write-Host "Opening browser..." -ForegroundColor Green
Start-Process "http://localhost:8501"

Write-Host ""
Write-Host "Browser should be opening now!" -ForegroundColor Green
Write-Host "App URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the app" -ForegroundColor Yellow
Write-Host ""

# Wait for the job
try {
    Wait-Job $streamlitJob | Out-Null
    Receive-Job $streamlitJob
} catch {
    Write-Host "App stopped." -ForegroundColor Yellow
    Stop-Job $streamlitJob
    Remove-Job $streamlitJob
}

