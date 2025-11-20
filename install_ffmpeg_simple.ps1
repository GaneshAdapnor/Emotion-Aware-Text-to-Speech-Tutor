# Simple FFmpeg Installer for Windows
# This script helps you install FFmpeg easily

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FFmpeg Installation Helper" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if FFmpeg is already installed
$ffmpegCheck = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpegCheck) {
    Write-Host "✅ FFmpeg is already installed!" -ForegroundColor Green
    Write-Host "Version: " -NoNewline
    ffmpeg -version | Select-Object -First 1
    exit 0
}

Write-Host "FFmpeg is not installed." -ForegroundColor Yellow
Write-Host ""
Write-Host "Choose installation method:" -ForegroundColor Cyan
Write-Host "1. Automatic (using Chocolatey) - Recommended" -ForegroundColor White
Write-Host "2. Manual download instructions" -ForegroundColor White
Write-Host "3. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-3)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "Installing FFmpeg using Chocolatey..." -ForegroundColor Yellow
    
    # Check if Chocolatey is installed
    $chocoCheck = Get-Command choco -ErrorAction SilentlyContinue
    if (-not $chocoCheck) {
        Write-Host "❌ Chocolatey is not installed." -ForegroundColor Red
        Write-Host ""
        Write-Host "To install Chocolatey, run this command as Administrator:" -ForegroundColor Yellow
        Write-Host 'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString("https://community.chocolatey.org/install.ps1"))' -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Then run this script again and choose option 1." -ForegroundColor Yellow
        pause
        exit
    }
    
    Write-Host "Running: choco install ffmpeg -y" -ForegroundColor Cyan
    choco install ffmpeg -y
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ FFmpeg installed successfully!" -ForegroundColor Green
        Write-Host "Please restart your Streamlit app." -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "❌ Installation failed. Try manual installation (option 2)." -ForegroundColor Red
    }
    
} elseif ($choice -eq "2") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Manual Installation Instructions" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Download FFmpeg:" -ForegroundColor Yellow
    Write-Host "   Visit: https://www.gyan.dev/ffmpeg/builds/" -ForegroundColor Cyan
    Write-Host "   Download: ffmpeg-release-essentials.zip" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Extract to C:\ffmpeg" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "3. Add to PATH:" -ForegroundColor Yellow
    Write-Host "   - Press Win + X → System → Advanced system settings" -ForegroundColor White
    Write-Host "   - Click 'Environment Variables'" -ForegroundColor White
    Write-Host "   - Under 'System variables', find 'Path' and click 'Edit'" -ForegroundColor White
    Write-Host "   - Click 'New' and add: C:\ffmpeg\bin" -ForegroundColor White
    Write-Host "   - Click OK on all dialogs" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Restart your terminal and verify:" -ForegroundColor Yellow
    Write-Host "   ffmpeg -version" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "5. Restart your Streamlit app" -ForegroundColor Yellow
    Write-Host ""
    
    # Open the download page
    $openBrowser = Read-Host "Open download page in browser? (Y/N)"
    if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
        Start-Process "https://www.gyan.dev/ffmpeg/builds/"
    }
    
} else {
    Write-Host "Exiting..." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
pause

