# PowerShell script to run Streamlit app in Microsoft Edge
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Emotion-Aware Text-to-Speech Tutor" -ForegroundColor Green
Write-Host " Opening in Microsoft Edge" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set Edge as the browser
$env:BROWSER = "msedge"

Write-Host "Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "The app will open automatically in Microsoft Edge!" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the app" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Streamlit in background
$streamlitProcess = Start-Process -FilePath "streamlit" -ArgumentList "run", "app.py", "--server.headless=false", "--browser.gatherUsageStats=false" -NoNewWindow -PassThru

# Wait for Streamlit to start
Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Open in Microsoft Edge
Write-Host "Opening in Microsoft Edge..." -ForegroundColor Green
Start-Process "msedge" -ArgumentList "http://localhost:8501"

Write-Host ""
Write-Host "App is running in Microsoft Edge!" -ForegroundColor Green
Write-Host "URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""

# Wait for the Streamlit process
try {
    Wait-Process -Id $streamlitProcess.Id
} catch {
    Write-Host "App stopped." -ForegroundColor Yellow
}

