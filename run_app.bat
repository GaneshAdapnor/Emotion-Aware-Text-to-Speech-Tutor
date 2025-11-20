@echo off
title Emotion-Aware Text-to-Speech Tutor
color 0A
cls

echo.
echo ========================================
echo   Emotion-Aware Text-to-Speech Tutor
echo ========================================
echo.
echo   Starting app...
echo   Browser will open automatically!
echo.
echo   Press Ctrl+C to stop
echo ========================================
echo.

REM Start Streamlit - browser opens automatically with headless=false
start "" streamlit run app.py --server.headless=false

echo.
echo App is starting! Check your browser...
echo.

