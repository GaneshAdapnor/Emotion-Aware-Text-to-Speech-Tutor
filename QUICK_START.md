# Quick Start Guide

## Run the App Locally

### Option 1: Double-click the script (Easiest)
- **Windows**: Double-click `run.bat`
- The app will automatically open in your browser at `http://localhost:8501`

### Option 2: Use PowerShell
```powershell
.\run.ps1
```

### Option 3: Manual command
```bash
streamlit run app.py
```

## What to Expect

1. The app will start loading
2. Your default browser will automatically open
3. You'll see the Emotion-Aware Text-to-Speech Tutor interface
4. First time loading may take a minute (downloading emotion model)

## Features Available

✅ **Text Input** - Paste or type your text
✅ **File Upload** - Upload PDF, DOCX, TXT, or MD files
✅ **Emotion Analysis** - Automatically detects emotions in text
✅ **Translation** - Translate to multiple languages
✅ **Speech Generation** - Generate emotional speech
✅ **Export Reports** - Download PDF or CSV reports

## Troubleshooting

### App won't open in browser
- Check if port 8501 is already in use
- Try: `streamlit run app.py --server.port 8502`

### Dependencies missing
```bash
pip install -r requirements.txt
```

### FFmpeg not found
- Audio processing features require FFmpeg
- See `SETUP_FFMPEG.md` for installation instructions
- Basic TTS will still work without FFmpeg

---

**Enjoy your Emotion-Aware Text-to-Speech Tutor!** 🎙️

