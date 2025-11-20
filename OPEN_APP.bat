@echo off
title Emotion-Aware Text-to-Speech Tutor
color 0B
cls

echo.
echo ========================================
echo   Emotion-Aware Text-to-Speech Tutor
echo ========================================
echo.
echo   Starting app...
echo   Browser window will open automatically!
echo.
echo   Press Ctrl+C to stop the app
echo ========================================
echo.

REM Start Streamlit - browser opens automatically with headless=false
streamlit run app.py

