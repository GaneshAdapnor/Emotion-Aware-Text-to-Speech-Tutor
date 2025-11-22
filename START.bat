@echo off
title Emotion-Aware Text-to-Speech Tutor
color 0A
cls

echo.
echo ========================================
echo   Emotion-Aware Text-to-Speech Tutor
echo ========================================
echo.
echo   Starting Streamlit...
echo   Browser will open automatically!
echo.
echo   Press Ctrl+C to stop the app
echo ========================================
echo.

REM Set Edge as default browser for this session
set BROWSER=msedge

REM Start Streamlit in background and wait for server to start
start /B streamlit run app.py --server.headless=false --browser.gatherUsageStats=false

REM Wait a few seconds for Streamlit to start
timeout /t 3 /nobreak >nul

REM Explicitly open in Microsoft Edge
start msedge http://localhost:8501

echo.
echo   Browser should be opening now!
echo   If not, go to: http://localhost:8501
echo.
echo   App is running... Press Ctrl+C in the Streamlit window to stop
echo.

REM Keep window open
pause

