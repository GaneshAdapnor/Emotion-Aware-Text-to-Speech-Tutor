# 🚀 Streamlit Cloud Deployment Guide

This guide will help you deploy your Emotion-Aware Text-to-Speech Tutor app to Streamlit Cloud.

## Prerequisites

1. **GitHub Account**: Your code needs to be in a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

If you haven't already, push your code to a GitHub repository:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Prepare for Streamlit Cloud deployment"

# Add your GitHub repository as remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)
2. **Sign in**: Use your GitHub account to sign in
3. **New App**: Click "New app"
4. **Select Repository**: Choose your repository from the dropdown
5. **Select Branch**: Choose `main` (or your default branch)
6. **Main file path**: Enter `app.py`
7. **App URL**: Choose a custom subdomain (optional)
8. **Click "Deploy"**

### 3. Wait for Deployment

- Streamlit Cloud will automatically:
  - Install dependencies from `requirements.txt`
  - Use Python version from `runtime.txt` (3.11)
  - Build and deploy your app
  - This usually takes 2-5 minutes

### 4. Access Your App

Once deployed, you'll get a URL like:
```
https://YOUR_APP_NAME.streamlit.app
```

## Important Notes for Streamlit Cloud

### ✅ What Works on Streamlit Cloud

- ✅ Emotion detection (HuggingFace models)
- ✅ Text-to-Speech (gTTS)
- ✅ Translation (deep-translator)
- ✅ Document processing (PDF, DOCX)
- ✅ PDF report generation
- ✅ Basic audio playback

### ⚠️ Limitations on Streamlit Cloud

- ⚠️ **FFmpeg**: Not available on Streamlit Cloud, so advanced audio effects (pitch/speed adjustments) won't work
- ⚠️ **pyttsx3**: May not work on Streamlit Cloud (system TTS not available)
- ⚠️ **File System**: Temporary files are cleaned up automatically

### 🔧 Configuration Files

The app includes:
- `requirements.txt` - All Python dependencies
- `runtime.txt` - Python version (3.11)
- `.streamlit/config.toml` - Streamlit configuration

### 📝 Environment Variables (Optional)

If you need to set environment variables:
1. Go to your app settings on Streamlit Cloud
2. Click "Advanced settings"
3. Add environment variables if needed

## Troubleshooting

### App Won't Deploy

1. **Check requirements.txt**: Ensure all dependencies are listed
2. **Check runtime.txt**: Ensure Python version is correct (3.11)
3. **Check logs**: View deployment logs in Streamlit Cloud dashboard

### App Deploys but Shows Errors

1. **Check app logs**: View logs in Streamlit Cloud dashboard
2. **Test locally first**: Run `streamlit run app.py` locally to catch errors
3. **Check dependencies**: Some packages might need version adjustments

### Model Download Issues

- The emotion detection model downloads automatically on first use
- This may take a few minutes on first load
- Ensure your app has internet access

## Updating Your App

1. **Make changes** to your code locally
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
3. **Streamlit Cloud auto-deploys** - Your app will automatically update!

## Support

- **Streamlit Cloud Docs**: [docs.streamlit.io/streamlit-cloud](https://docs.streamlit.io/streamlit-cloud)
- **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)

---

**Ready to deploy?** Push your code to GitHub and follow the steps above! 🚀

