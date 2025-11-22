@echo off
title Emotion-Aware Text-to-Speech Tutor - Microsoft Edge
color 0A
cls

echo.
echo ========================================
echo   Emotion-Aware Text-to-Speech Tutor
echo   Opening in Microsoft Edge
echo ========================================
echo.
echo   Starting Streamlit...
echo.

REM Set Edge as default browser for this session
set BROWSER=msedge

REM Start Streamlit in background
start /B streamlit run app.py --server.headless=false --browser.gatherUsageStats=false

REM Wait for Streamlit to start
echo   Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Open in Microsoft Edge specifically
echo   Opening in Microsoft Edge...
start msedge http://localhost:8501

echo.
echo   App is running in Microsoft Edge!
echo   URL: http://localhost:8501
echo.
echo   Press Ctrl+C in the Streamlit window to stop
echo ========================================
echo.

REM Keep window open
pause

