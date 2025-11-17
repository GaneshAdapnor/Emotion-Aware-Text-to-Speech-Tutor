# Troubleshooting Streamlit Cloud Deployment

## If Requirements Installation Fails

### Step 1: Check the Actual Error
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click "Manage app" → "Logs"
4. Look for the specific error message in the installation logs

### Step 2: Common Issues and Solutions

#### Issue: Torch Installation Fails
**Solution:** Torch is very large (~2GB). Try this alternative requirements.txt:

```txt
streamlit>=1.28.0
transformers>=4.35.0
--index-url https://download.pytorch.org/whl/cpu
torch>=2.0.0
gtts>=2.4.0
numpy>=1.24.0
scipy>=1.11.0
requests>=2.31.0
pdfplumber>=0.10.0
python-docx>=1.1.0
reportlab>=4.0.0
pandas>=2.0.0
deep-translator>=1.11.4
```

#### Issue: Package Version Conflicts
**Solution:** Use the minimal requirements file:

1. Rename `requirements.txt` to `requirements-full.txt`
2. Rename `requirements-minimal.txt` to `requirements.txt`
3. Push and redeploy

#### Issue: Memory/Timeout During Installation
**Solution:** 
- Remove optional packages: `pydub`, `soundfile`, `scipy`
- The app will work without them (with limited audio features)

#### Issue: Python Version
**Solution:** Try different Python versions in `runtime.txt`:
- `python-3.10` (most compatible)
- `python-3.11`
- `python-3.9`

### Step 3: Minimal Working Configuration

If all else fails, use this minimal `requirements.txt`:

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

This removes:
- `pydub` (optional, app handles missing gracefully)
- `soundfile` (optional)
- `scipy` (optional)
- `PyPDF2` (optional, pdfplumber is primary)
- `Pillow` (usually comes with other packages)

### Step 4: Install in Stages

If you need all packages, you can modify the app to install them programmatically, but this is not recommended for Streamlit Cloud.

## Getting Help

1. **Check Streamlit Cloud Status**: https://status.streamlit.io/
2. **Streamlit Forums**: https://discuss.streamlit.io/
3. **GitHub Issues**: Check if others have similar issues

## Current Configuration

- Python: 3.10.11
- All packages have fallback handling in app.py
- App will work with minimal packages (just slower/limited features)

