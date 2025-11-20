# Deploy to Streamlit Cloud - Quick Guide

## Prerequisites

1. **GitHub Account** - Your code needs to be on GitHub
2. **Streamlit Cloud Account** - Sign up at [share.streamlit.io](https://share.streamlit.io)

## Deployment Steps

### Step 1: Push Your Code to GitHub

If you haven't already, initialize git and push your code:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Streamlit Cloud deployment"

# Add your GitHub repository as remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"** button
4. Fill in the deployment form:
   - **Repository**: Select your repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
5. Click **"Deploy"**

### Step 3: Wait for Deployment

- Streamlit Cloud will automatically install dependencies from `requirements.txt`
- First deployment may take 5-10 minutes
- You'll see progress in the deployment logs
- Once complete, you'll get a public URL like: `https://your-app-name.streamlit.app`

## Important Notes

### ✅ What Works on Streamlit Cloud

- Document upload (PDF, DOCX, TXT, MD)
- Text extraction
- Emotion analysis
- Translation
- PDF report generation
- CSV export
- Basic speech generation (using gTTS)

### ⚠️ Limitations on Streamlit Cloud

- **FFmpeg is NOT available** - Advanced audio processing won't work
- Audio effects (pitch, speed, volume adjustments) require FFmpeg
- The app will gracefully handle this and use basic TTS instead

### 🔧 If Deployment Fails

1. **Check the logs** in Streamlit Cloud dashboard
2. **Common issues**:
   - Package version conflicts → Try `requirements-minimal-v2.txt`
   - Memory issues → Remove heavy packages temporarily
   - Import errors → Check all dependencies are listed

3. **Try minimal requirements**:
   ```bash
   # Copy minimal requirements
   cp requirements-minimal-v2.txt requirements.txt
   git add requirements.txt
   git commit -m "Use minimal requirements"
   git push
   ```

## Configuration Files

Your deployment uses:
- `app.py` - Main application file
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version (3.11)
- `.streamlit/config.toml` - Streamlit configuration

## Updating Your App

After making changes:

```bash
git add .
git commit -m "Update app"
git push
```

Streamlit Cloud will automatically redeploy your app!

## Troubleshooting

### App won't start
- Check logs for error messages
- Verify `app.py` is in the root directory
- Ensure all imports are available in `requirements.txt`

### Dependencies fail to install
- Try using `requirements-minimal-v2.txt`
- Remove version constraints
- Check Streamlit Cloud status: https://status.streamlit.io/

### Model loading fails
- First load may take time (downloading models)
- Check internet connectivity in logs
- Model is cached after first load

## Support

- Streamlit Community: https://discuss.streamlit.io/
- Streamlit Docs: https://docs.streamlit.io/
- Check deployment logs in Streamlit Cloud dashboard

---

**Your app will be live at:** `https://YOUR-APP-NAME.streamlit.app`

Happy deploying! 🚀

