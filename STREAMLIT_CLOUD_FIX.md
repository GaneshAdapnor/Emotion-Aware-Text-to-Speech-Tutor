# Streamlit Cloud Requirements Fix

## Common Installation Issues

If you're getting "Error installing requirements" on Streamlit Cloud, try these fixes:

### 1. **Check the Logs**
- Click "Manage App" in Streamlit Cloud
- Check the "Logs" tab for specific error messages
- Common errors:
  - Package version conflicts
  - Missing system dependencies
  - Memory/timeout issues during installation

### 2. **Optimized Requirements**
The current `requirements.txt` has been optimized:
- Removed `pyttsx3` (doesn't work well on Linux/Streamlit Cloud)
- Simplified version constraints
- All packages are compatible with Streamlit Cloud

### 3. **If Torch Installation Fails**
If torch is causing issues, you can try:
- Use CPU-only torch (already configured in app.py)
- The app will automatically use CPU mode

### 4. **Alternative: Minimal Requirements**
If issues persist, try installing only essential packages first:

```txt
streamlit>=1.28.0
transformers>=4.35.0
torch>=2.0.0
gtts>=2.4.0
numpy>=1.24.0
requests>=2.31.0
pdfplumber>=0.10.0
python-docx>=1.1.0
reportlab>=4.0.0
pandas>=2.0.0
deep-translator>=1.11.4
```

Then add optional packages one by one.

### 5. **Check Python Version**
- Current: Python 3.10.11 (in runtime.txt)
- Streamlit Cloud supports: 3.8, 3.9, 3.10, 3.11
- If 3.10.11 doesn't work, try: `python-3.10` or `python-3.11`

### 6. **Deployment Tips**
- First deployment may take 5-10 minutes (downloading models)
- Be patient during initial setup
- Check logs if it takes longer than 15 minutes

## Current Configuration
- ✅ Removed pyttsx3 (Linux incompatible)
- ✅ Simplified version constraints
- ✅ Python 3.10.11 specified
- ✅ All imports have fallback handling

