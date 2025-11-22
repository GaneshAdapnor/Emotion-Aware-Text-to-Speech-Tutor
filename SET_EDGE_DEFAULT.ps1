# PowerShell script to ensure Streamlit uses system default browser
Write-Host "Configuring Streamlit to use your system default browser..." -ForegroundColor Yellow

# Remove any BROWSER environment variable to use system default
$currentBrowser = [System.Environment]::GetEnvironmentVariable("BROWSER", "User")
if ($currentBrowser) {
    [System.Environment]::SetEnvironmentVariable("BROWSER", $null, "User")
    Write-Host "Removed custom browser setting - will use system default." -ForegroundColor Green
} else {
    Write-Host "No custom browser setting found - will use system default." -ForegroundColor Green
}

Write-Host ""
Write-Host "Streamlit will now use your system default browser!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run the app using:" -ForegroundColor Yellow
Write-Host "  - START.bat (double-click)" -ForegroundColor White
Write-Host "  - run.ps1 (PowerShell)" -ForegroundColor White
Write-Host ""
Write-Host "The app will automatically open in your default browser!" -ForegroundColor Green
Write-Host ""
