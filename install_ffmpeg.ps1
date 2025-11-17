# FFmpeg Installation Script
# This script downloads and installs FFmpeg on Windows

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FFmpeg Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Note: Some operations may require administrator privileges." -ForegroundColor Yellow
    Write-Host ""
}

# Set paths
$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$downloadPath = "$env:TEMP\ffmpeg.zip"
$extractPath = "C:\ffmpeg"
$binPath = "$extractPath\bin"

# Step 1: Download FFmpeg
Write-Host "[1/4] Downloading FFmpeg..." -ForegroundColor Yellow
if (Test-Path $downloadPath) {
    Write-Host "       Found existing download, skipping..." -ForegroundColor Gray
} else {
    try {
        Invoke-WebRequest -Uri $ffmpegUrl -OutFile $downloadPath -UseBasicParsing
        $fileSize = (Get-Item $downloadPath).Length / 1MB
        Write-Host "       Download complete! ($([math]::Round($fileSize, 2)) MB)" -ForegroundColor Green
    } catch {
        Write-Host "       Error downloading FFmpeg: $_" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Extract FFmpeg
Write-Host "[2/4] Extracting FFmpeg..." -ForegroundColor Yellow
try {
    # Remove existing installation if present
    if (Test-Path $extractPath) {
        Write-Host "       Removing existing installation..." -ForegroundColor Gray
        Remove-Item $extractPath -Recurse -Force
    }
    
    # Extract to temp location first
    $tempExtract = "$env:TEMP\ffmpeg-extract"
    if (Test-Path $tempExtract) {
        Remove-Item $tempExtract -Recurse -Force
    }
    
    Expand-Archive -Path $downloadPath -DestinationPath $tempExtract -Force
    
    # Find the extracted folder (usually named ffmpeg-version-essentials)
    $extractedFolder = Get-ChildItem $tempExtract -Directory | Where-Object { $_.Name -like "ffmpeg-*" } | Select-Object -First 1
    
    if ($extractedFolder) {
        # Move to final location
        Move-Item $extractedFolder.FullName $extractPath -Force
        Write-Host "       Extracted to $extractPath" -ForegroundColor Green
    } else {
        Write-Host "       Error: Could not find extracted folder" -ForegroundColor Red
        exit 1
    }
    
    # Clean up temp extract folder
    Remove-Item $tempExtract -ErrorAction SilentlyContinue
} catch {
    Write-Host "       Error extracting FFmpeg: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Verify installation
Write-Host "[3/4] Verifying installation..." -ForegroundColor Yellow
$ffmpegExe = "$binPath\ffmpeg.exe"
if (Test-Path $ffmpegExe) {
    $version = & $ffmpegExe -version 2>&1 | Select-Object -First 1
    Write-Host "       FFmpeg found: $version" -ForegroundColor Green
} else {
    Write-Host "       Error: ffmpeg.exe not found at $ffmpegExe" -ForegroundColor Red
    exit 1
}

# Step 4: Add to PATH
Write-Host "[4/4] Adding FFmpeg to PATH..." -ForegroundColor Yellow

# Add to user PATH (doesn't require admin)
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$binPath*") {
    try {
        $newPath = $userPath + ";$binPath"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "       Added to User PATH" -ForegroundColor Green
        
        # Also add to current session
        $env:Path += ";$binPath"
        Write-Host "       Added to current session PATH" -ForegroundColor Green
    } catch {
        Write-Host "       Warning: Could not modify User PATH: $_" -ForegroundColor Yellow
        Write-Host "       You may need to add $binPath manually to your PATH" -ForegroundColor Yellow
    }
} else {
    Write-Host "       Already in User PATH" -ForegroundColor Gray
}

# Try to add to system PATH (requires admin)
if ($isAdmin) {
    $systemPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($systemPath -notlike "*$binPath*") {
        try {
            $newSystemPath = $systemPath + ";$binPath"
            [Environment]::SetEnvironmentVariable("Path", $newSystemPath, "Machine")
            Write-Host "       Added to System PATH (requires restart)" -ForegroundColor Green
        } catch {
            Write-Host "       Could not modify System PATH: $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "       Already in System PATH" -ForegroundColor Gray
    }
} else {
    Write-Host "       Skipping System PATH (requires admin privileges)" -ForegroundColor Gray
}

# Clean up download
Write-Host ""
Write-Host "Cleaning up..." -ForegroundColor Yellow
Remove-Item $downloadPath -ErrorAction SilentlyContinue

# Final verification
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "FFmpeg has been installed to: $extractPath" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Please restart your terminal/command prompt" -ForegroundColor Yellow
Write-Host "          and Streamlit app for PATH changes to take effect." -ForegroundColor Yellow
Write-Host ""
Write-Host "To verify installation, run: ffmpeg -version" -ForegroundColor Cyan
Write-Host ""

