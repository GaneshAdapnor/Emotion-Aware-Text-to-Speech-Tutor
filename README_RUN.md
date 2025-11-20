# 🚀 How to Run - Browser Opens Automatically!

## ✅ Easiest Way - Just Double-Click!

### **OPEN_APP.bat** (Recommended)
1. **Double-click** `OPEN_APP.bat`
2. **Browser opens automatically!** 🎉
3. App loads at `http://localhost:8501`

### **START.bat** (Alternative)
1. **Double-click** `START.bat`
2. Browser opens automatically
3. Same result!

## ⚙️ Configuration

Your app is configured to **automatically open the browser**:
- ✅ `headless = false` in `.streamlit/config.toml`
- ✅ Streamlit will open your default browser
- ✅ No manual steps needed!

## 🎯 What Happens

When you run the app:
1. ✅ Streamlit server starts
2. ✅ **Browser window opens automatically**
3. ✅ App loads at `http://localhost:8501`
4. ✅ First time: May take 1-2 minutes (downloading emotion model)

## 📝 Command Line (Alternative)

If you prefer command line:
```powershell
streamlit run app.py
```

The browser will **still open automatically** because `headless = false` is set in the config!

## 🔧 Troubleshooting

### Browser doesn't open?
- Manually go to: `http://localhost:8501`
- Check if port 8501 is in use
- Try: `streamlit run app.py --server.port 8502`

### App won't start?
- Install dependencies: `pip install -r requirements.txt`
- Check Streamlit: `pip install streamlit`

---

**Just double-click `OPEN_APP.bat` and the browser opens automatically!** 🎉

