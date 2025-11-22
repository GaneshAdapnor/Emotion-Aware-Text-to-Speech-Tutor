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

REM Start Streamlit with auto-open browser (overrides config.toml headless setting)
REM The --server.headless=false flag ensures browser opens automatically
streamlit run app.py --server.headless=false --browser.gatherUsageStats=false --server.runOnSave=true

echo.
echo   Browser should be opening now!
echo   If not, go to: http://localhost:8501
echo.
echo   App is running... Press Ctrl+C in the Streamlit window to stop
echo.

REM Keep window open
pause

