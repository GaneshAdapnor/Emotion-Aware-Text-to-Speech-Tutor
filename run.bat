@echo off
echo ========================================
echo  Emotion-Aware Text-to-Speech Tutor
echo ========================================
echo.
echo Starting Streamlit app...
echo The app will open automatically in your browser!
echo.
echo Press Ctrl+C to stop the app
echo ========================================
echo.

REM Run Streamlit with explicit browser opening
streamlit run app.py --server.headless=false --server.runOnSave=true

pause

