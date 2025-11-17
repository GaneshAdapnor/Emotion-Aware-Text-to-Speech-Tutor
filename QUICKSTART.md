# 🚀 Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed.
```bash
python --version
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** The first run will download the emotion detection model (~500MB). Ensure you have:
- Stable internet connection
- At least 2GB free disk space
- 4GB+ RAM recommended

**New Dependencies (PDF & Document Support):**
- `pdfplumber` or `PyPDF2` - For PDF text extraction
- `python-docx` - For Word document (DOCX) processing
- `reportlab` - For PDF report generation
- `pandas` - For CSV export functionality

### Step 4: Install FFmpeg (for audio processing)
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

### Step 5: Run the Application
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 🎯 First Test

1. **Paste text or upload a document:**
   - **Paste text**: Enter text directly in the text area
   - **Upload file**: Upload PDF, DOCX, TXT, or MD files
   - Example text:
     ```
     The discovery was amazing! Scientists were thrilled. However, some felt anxious about the implications.
     ```

2. **Click "Analyze Emotions"** - Wait for analysis (first time may take 30-60 seconds)

3. **Review the emotion table** - See detected emotions for each sentence

4. **Export results** (optional):
   - **Download PDF Report**: Generate a formatted PDF report with analysis results
   - **Download CSV**: Export results as a CSV file for further analysis

5. **Click "Generate Speech"** - Listen to emotion-aware audio

6. **Download the audio** - Save the generated speech file

## 🐛 Troubleshooting

### "Model download failed"
- Check internet connection
- Try again (model downloads on first use)
- Ensure you have enough disk space

### "FFmpeg not found"
- Install FFmpeg (see Step 4 above)
- Restart terminal/command prompt after installation

### "Audio playback doesn't work"
- Check browser audio settings
- Try downloading the audio file instead
- Ensure audio drivers are installed

### "Out of memory"
- Close other applications
- Process text in smaller chunks
- Use a machine with more RAM

### "PDF/DOCX extraction failed"
- Ensure `pdfplumber` or `PyPDF2` is installed for PDF support
- Ensure `python-docx` is installed for DOCX support
- Check if the file is password-protected (not supported)
- Verify the file is not corrupted
- Try a different PDF/DOCX file

### "PDF export not available"
- Install `reportlab` library: `pip install reportlab`
- Restart the Streamlit app after installation
- Check if reportlab is in requirements.txt

## 📝 Example Texts to Try

### Happy/Excited
```
Congratulations! You've won the grand prize! This is absolutely amazing news!
```

### Sad
```
The loss was devastating. Everyone felt the weight of disappointment and sorrow.
```

### Mixed Emotions
```
The results were surprising. Some were happy, others were concerned about the future.
```

### Educational Text
```
The discovery of gravity revolutionized physics. Scientists were thrilled! However, initial reactions showed surprise and curiosity.
```

## 🎓 Next Steps

- **Upload documents**: Try uploading PDF or DOCX files from your computer
- **Export results**: Generate PDF reports or CSV exports for your analysis
- **Experiment with different languages**: Test emotion detection in various languages
- **Adjust settings**: Customize base speech speed and language in the sidebar
- **Generate speech**: Create emotion-aware audio for individual sentences or combined text

## 💡 Tips

- **Document support**: Upload PDF, DOCX, TXT, or MD files for text extraction
- **PDF reports**: Generate professional PDF reports with analysis results and statistics
- **Longer texts**: Process in paragraphs for better emotion detection
- **Quality**: First generation may be slower, subsequent ones are faster
- **Languages**: Emotion detection works best with English; other languages use TTS but emotion mapping may vary
- **Audio quality**: Generated audio is optimized for clarity and emotional expression
- **Export options**: Use CSV export for data analysis in Excel or other tools

---

**Enjoy your Emotion-Aware Text-to-Speech Tutor! 🎙️**

