# 🎵 FFmpeg Installation Guide

## ⚠️ Important: FFmpeg is Optional!

**You don't need FFmpeg to use this app!** Basic text-to-speech works perfectly without it.

FFmpeg is only needed for:
- Advanced audio effects (pitch adjustments)
- Speed modifications
- Volume changes
- Complex audio processing

---

## 🪟 Windows Installation

### Option 1: Automatic (Recommended)

If you have **Chocolatey** installed:
```powershell
choco install ffmpeg
```

**Don't have Chocolatey?** Install it first:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString("https://community.chocolatey.org/install.ps1"))
```

### Option 2: Use Our Helper Script

1. Right-click `install_ffmpeg_simple.ps1`
2. Select "Run with PowerShell"
3. Follow the prompts

### Option 3: Manual Installation

1. **Download FFmpeg:**
   - Visit: https://www.gyan.dev/ffmpeg/builds/
   - Download: **ffmpeg-release-essentials.zip**

2. **Extract:**
   - Extract to `C:\ffmpeg` (or any location you prefer)

3. **Add to PATH:**
   - Press `Win + X` → **System** → **Advanced system settings**
   - Click **Environment Variables**
   - Under **System variables**, find **Path** and click **Edit**
   - Click **New** and add: `C:\ffmpeg\bin`
   - Click **OK** on all dialogs

4. **Verify:**
   - Close and reopen your terminal
   - Run: `ffmpeg -version`
   - You should see version information

---

## 🍎 macOS Installation

```bash
brew install ffmpeg
```

If you don't have Homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ffmpeg
```

---

## 🐧 Linux Installation

### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### Fedora:
```bash
sudo dnf install ffmpeg
```

### Arch Linux:
```bash
sudo pacman -S ffmpeg
```

---

## ✅ Verify Installation

After installing, verify it works:

```bash
ffmpeg -version
```

You should see version information. If you see "command not found", make sure:
1. You added FFmpeg to your PATH
2. You restarted your terminal
3. You restarted your Streamlit app

---

## 🔄 After Installation

1. **Close your Streamlit app** (if running)
2. **Restart your terminal**
3. **Run the app again:**
   ```bash
   streamlit run app.py
   ```
4. You should now see: **✅ FFmpeg detected - Full audio processing available!**

---

## ❓ Troubleshooting

### "FFmpeg not found" after installation?
- Make sure you added it to PATH
- Restart your terminal
- Restart Streamlit app
- Verify with: `ffmpeg -version`

### Still having issues?
- Check the PATH variable includes FFmpeg's bin directory
- Try the full path: `C:\ffmpeg\bin\ffmpeg.exe -version`
- On Windows, you may need to restart your computer

---

**Remember:** FFmpeg is optional! The app works great without it for basic text-to-speech! 🎉

