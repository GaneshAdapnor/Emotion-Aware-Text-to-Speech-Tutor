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

REM Start Streamlit in background with auto-open browser
start /B streamlit run app.py --server.headless=false --browser.gatherUsageStats=false --server.runOnSave=true

REM Wait for Streamlit server to start
echo   Waiting for server to start...
timeout /t 4 /nobreak >nul

REM Explicitly open browser in default browser
echo   Opening browser...
start http://localhost:8501

echo.
echo   Browser should be opening now!
echo   If not, go to: http://localhost:8501
echo.
echo   App is running... Check the Streamlit window for status
echo   Press any key to close this window (app will keep running)
echo.

REM Keep window open briefly then close
timeout /t 2 /nobreak >nul

