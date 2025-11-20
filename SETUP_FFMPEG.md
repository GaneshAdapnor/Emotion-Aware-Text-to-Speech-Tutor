# FFmpeg Setup Guide

## Why FFmpeg is Needed

FFmpeg is required for `pydub` to properly process audio files (MP3, WAV, etc.). Without it, some audio operations may fail.

## Installation

### Windows

1. **Download FFmpeg:**
   - Visit: https://www.gyan.dev/ffmpeg/builds/
   - Download the "ffmpeg-release-essentials.zip" file

2. **Extract and Install:**
   - Extract the ZIP file to a location like `C:\ffmpeg`
   - Add to PATH:
     - Open System Properties → Environment Variables
     - Edit "Path" variable
     - Add: `C:\ffmpeg\bin`
     - Click OK to save

3. **Verify Installation:**
   ```powershell
   ffmpeg -version
   ```

### Alternative: Using Chocolatey (Windows)
```powershell
choco install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

### Linux
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

## Verify Installation

After installing, restart your terminal and run:
```bash
ffmpeg -version
```

If you see version information, FFmpeg is installed correctly.

## Note

The app may work without FFmpeg for basic operations, but for full functionality (especially audio format conversion and processing), FFmpeg is recommended.









