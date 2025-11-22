# PowerShell script to set Microsoft Edge as default browser for Streamlit
Write-Host "Setting Microsoft Edge as default browser for Streamlit..." -ForegroundColor Yellow

# Set Edge as default browser in environment variable (user-level)
[System.Environment]::SetEnvironmentVariable("BROWSER", "msedge", "User")

Write-Host ""
Write-Host "Microsoft Edge is now set as the default browser for Streamlit!" -ForegroundColor Green
Write-Host ""
Write-Host "This setting will persist across sessions." -ForegroundColor Cyan
Write-Host "You can now run the app using:" -ForegroundColor Yellow
Write-Host "  - RUN_EDGE.bat (double-click)" -ForegroundColor White
Write-Host "  - RUN_EDGE.ps1 (PowerShell)" -ForegroundColor White
Write-Host "  - run.ps1 (PowerShell)" -ForegroundColor White
Write-Host "  - START.bat (double-click)" -ForegroundColor White
Write-Host ""
Write-Host "All scripts will now open in Microsoft Edge automatically!" -ForegroundColor Green
Write-Host ""
