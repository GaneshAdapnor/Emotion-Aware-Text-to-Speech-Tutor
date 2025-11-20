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

REM Start Streamlit in background and wait for server to start
start /B streamlit run app.py --server.headless=false

REM Wait a few seconds for Streamlit to start
timeout /t 3 /nobreak >nul

REM Explicitly open browser to ensure it opens
start http://localhost:8501

echo.
echo   Browser should be opening now!
echo   If not, go to: http://localhost:8501
echo.
echo   App is running... Press Ctrl+C in the Streamlit window to stop
echo.

REM Keep window open
pause

