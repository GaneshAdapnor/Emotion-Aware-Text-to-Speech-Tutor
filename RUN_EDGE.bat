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

REM Start Streamlit in background with auto-open browser
start /B streamlit run app.py --server.headless=false --browser.gatherUsageStats=false --server.runOnSave=true

REM Wait for Streamlit server to start
echo   Waiting for server to start...
timeout /t 4 /nobreak >nul

REM Explicitly open browser in default browser
echo   Opening in your default browser...
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

echo.
echo   App is running in your default browser!
echo   URL: http://localhost:8501
echo.
echo   Press Ctrl+C in the Streamlit window to stop
echo ========================================
echo.

REM Keep window open
pause

