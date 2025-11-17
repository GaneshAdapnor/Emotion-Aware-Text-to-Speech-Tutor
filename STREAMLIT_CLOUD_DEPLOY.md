# Streamlit Cloud Deployment Guide

## Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set main file path to: `app.py`
   - Click "Deploy"

## Important Notes

### FFmpeg Limitation
⚠️ **FFmpeg is NOT available on Streamlit Cloud** (system-level dependency)

- ✅ **Will work on Streamlit Cloud:**
  - Document upload (PDF, DOCX, TXT, MD)
  - Text extraction
  - Emotion analysis
  - PDF report generation
  - CSV export

- ❌ **Won't work on Streamlit Cloud:**
  - Audio processing (requires FFmpeg)
  - Speech generation with audio effects

### Workaround for Audio
For Streamlit Cloud deployment, you can:
1. Use the app for emotion analysis and document processing (works perfectly)
2. Generate speech locally for audio features
3. Or use a cloud service with FFmpeg support (e.g., Heroku, Railway, etc.)

## Requirements

All dependencies are in `requirements.txt`:
- Streamlit
- Transformers (emotion detection)
- PDF/DOCX processing libraries
- ReportLab (PDF generation)
- Pandas (CSV export)

## Configuration

The app is configured via `.streamlit/config.toml`:
- Server settings
- Theme customization
- CORS and security settings

## Testing Locally

Before deploying, test locally:
```bash
streamlit run app.py
```

## Deployment Checklist

- [x] All dependencies in `requirements.txt`
- [x] Streamlit config file created
- [x] App handles missing FFmpeg gracefully
- [x] Document processing works
- [x] PDF export works
- [x] Emotion analysis works
- [ ] Test audio features locally (if needed)

## Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Verify all dependencies are in `requirements.txt`
3. Ensure `app.py` is the main file
4. Check for any import errors in logs

---

**Note:** For full audio functionality, consider deploying to platforms that support FFmpeg installation (Heroku, Railway, DigitalOcean, etc.)

