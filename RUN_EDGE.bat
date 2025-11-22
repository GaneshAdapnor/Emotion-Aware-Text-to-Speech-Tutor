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

REM Start Streamlit with auto-open browser (overrides config.toml headless setting)
REM The --server.headless=false flag ensures browser opens automatically
streamlit run app.py --server.headless=false --browser.gatherUsageStats=false --server.runOnSave=true

echo.
echo   App is running in your default browser!
echo   URL: http://localhost:8501
echo.
echo   Press Ctrl+C in the Streamlit window to stop
echo ========================================
echo.

REM Keep window open
pause

