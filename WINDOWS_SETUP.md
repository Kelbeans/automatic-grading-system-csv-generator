# Windows Setup Guide

Quick guide to run SF10 Grade Automation on Windows.

## Prerequisites

### 1. Install Python
- Download from: https://www.python.org/downloads/
- **IMPORTANT**: Check ✅ **"Add Python to PATH"** during installation
- Minimum version: Python 3.7+

### 2. Download the Project
- Download ZIP from GitHub
- Extract to a folder (e.g., `C:\SF10-Grade-Automation`)

## Running the App

### Option 1: Batch File (Recommended - Easiest)

**Double-click** `START_WEB_APP.bat`

That's it! The browser will open automatically.

### Option 2: PowerShell Script

**Right-click** `START_WEB_APP.ps1` → **"Run with PowerShell"**

If you get an error about execution policy:
1. Open PowerShell as Administrator
2. Run: `Set-ExecutionPolicy RemoteSigned`
3. Type `Y` and press Enter
4. Try again

### Option 3: Command Line

```cmd
cd path\to\automatic-grading-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python sf10_web_app.py
```

## First Time Setup

The first time you run, it will:
1. Create a virtual environment (takes ~30 seconds)
2. Install required packages (takes ~1 minute)
3. Start the web server

After that, it starts instantly!

## Using the App

1. Browser opens to `http://localhost:8080`
2. Drag and drop your grading sheets
3. Click "Generate SF10 Records"
4. Download your files

## Troubleshooting

### "Python is not recognized"
- Python not installed or not in PATH
- Reinstall Python and check "Add Python to PATH"

### "pip is not recognized"
- Run: `python -m pip install --upgrade pip`

### Port 8080 already in use
- Another program is using port 8080
- Close other applications or restart your computer

### "Cannot be loaded because running scripts is disabled"
- This is PowerShell execution policy
- Use Option 1 (.bat file) instead
- Or follow PowerShell setup steps above

## Stopping the Server

Press `CTRL + C` in the terminal window, then close it.

## For Your Wife (Non-Technical User)

1. **Double-click** the file `START_WEB_APP.bat`
2. Wait for browser to open (10-30 seconds)
3. Upload grading sheets
4. Click generate
5. Download files
6. Close browser when done
7. Close the black window (terminal)

That's it! No technical knowledge needed.

## Support

For issues, contact: Kelvin A. Malabanan
GitHub: https://github.com/Kelbeans/automatic-grading-system-csv-generator
