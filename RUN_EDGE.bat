@echo off
title Emotion-Aware Text-to-Speech Tutor
color 0A
cls

echo.
echo ========================================
echo   Emotion-Aware Text-to-Speech Tutor
echo   Opening in your default browser
echo ========================================
echo.
echo   Starting Streamlit...
echo.

REM Start Streamlit in background
start /B streamlit run app.py --server.headless=false --browser.gatherUsageStats=false

REM Wait for Streamlit to start
echo   Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Open in default browser
echo   Opening in your default browser...
start http://localhost:8501

echo.
echo   App is running in your default browser!
echo   URL: http://localhost:8501
echo.
echo   Press Ctrl+C in the Streamlit window to stop
echo ========================================
echo.

REM Keep window open
pause

