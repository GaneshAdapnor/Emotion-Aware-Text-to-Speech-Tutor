# 🚀 How to Run the App

## Easiest Way - Double Click!

### Option 1: START.bat (Recommended)
1. **Double-click** `START.bat` in your project folder
2. The app will automatically:
   - Start Streamlit
   - Open your default browser
   - Navigate to `http://localhost:8501`

### Option 2: run.bat
1. **Double-click** `run.bat`
2. Same as above - browser opens automatically!

## Command Line Options

### PowerShell
```powershell
.\run.ps1
```

### Direct Command
```bash
streamlit run app.py
```

## What Happens

When you run the app:
1. ✅ Streamlit server starts
2. ✅ Your default browser opens automatically
3. ✅ App loads at `http://localhost:8501`
4. ✅ First time may take 1-2 minutes (downloading emotion model)

## Configuration

The app is configured to:
- ✅ Open browser automatically (`headless = false`)
- ✅ Use port 8501
- ✅ Show helpful error messages

## Troubleshooting

### Browser doesn't open automatically?
- Manually go to: `http://localhost:8501`
- Check if port 8501 is already in use
- Try: `streamlit run app.py --server.port 8502`

### App won't start?
- Make sure Streamlit is installed: `pip install streamlit`
- Check dependencies: `pip install -r requirements.txt`

---

**Just double-click `START.bat` and you're ready to go!** 🎉

