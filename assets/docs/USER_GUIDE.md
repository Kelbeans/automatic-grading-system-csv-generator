# SF10 Grade Automation - User Guide

## 🎯 For Non-Technical Users

This guide will help you generate SF10 files from your grading sheets using a simple drag-and-drop web interface.

---

## 🚀 Starting the System

### Step 1: Open Terminal/Command Prompt

1. Press `Cmd + Space` (Mac) or `Windows Key` (Windows)
2. Type: `terminal` and press Enter

### Step 2: Navigate to the Project

Copy and paste this command:

```bash
cd /Users/dev.kelvin/Documents/automatic\ grading\ system
```

Press Enter.

### Step 3: Start the Web Interface

Copy and paste this command:

```bash
python3 sf10_web_app.py
```

Press Enter.

You should see:
```
SF10 Grade Automation Web Interface
====================================================================
Starting server...
Open your browser to: http://localhost:5000
```

### Step 4: Open Your Browser

1. Open your web browser (Chrome, Safari, Firefox, etc.)
2. Go to: **http://localhost:5000**

You should see a beautiful purple interface with drag-and-drop areas!

---

## 📝 Using the Web Interface

### Uploading Files

**There are TWO upload areas:**

1. **Upload Grading Sheets** (Required)
   - Drag your grading sheet files here
   - You can upload multiple quarters at once
   - Files should have the quarter in the name (e.g., "1st QTR", "2nd QTR")

2. **Upload Existing SF10** (Optional)
   - Only use this if you want to ADD grades to an existing SF10 file
   - Skip this if it's the first time generating

### Example Scenarios

#### Scenario 1: First Quarter Only
1. Drag your "1st QTR GRADE 1 DAISY GRADING SHEET.xlsx" to Area 1
2. Don't upload anything to Area 2
3. Click "Generate SF10"
4. Download your file!

#### Scenario 2: Multiple Quarters at Once
1. Drag all your grading sheets to Area 1:
   - "1st QTR GRADE 1 DAISY GRADING SHEET.xlsx"
   - "2nd QTR GRADE 1 DAISY GRADING SHEET.xlsx"
2. Don't upload anything to Area 2
3. Click "Generate SF10"
4. Download - it will have both Q1 and Q2 filled!

#### Scenario 3: Adding to Existing SF10
1. You already have an SF10 with 1st quarter grades
2. Now you have 2nd quarter grading sheet
3. Drag "2nd QTR GRADING SHEET.xlsx" to Area 1
4. Drag your existing "SF10_All_Students.xlsx" to Area 2
5. Click "Generate SF10"
6. Download - it will have Q1 (from before) + Q2 (new)!

#### Scenario 4: Starting with 2nd Quarter (Missing 1st)
1. You only have 2nd quarter grading sheet
2. Drag "2nd QTR GRADING SHEET.xlsx" to Area 1
3. Don't upload anything to Area 2
4. Click "Generate SF10"
5. Download - Q2 will be filled, Q1 will be empty
6. Later when you get Q1 sheet, use Scenario 3 to add it!

---

## 📥 Downloading Your File

After clicking "Generate SF10":
1. Wait a few seconds (you'll see a loading spinner)
2. A green success message will appear
3. Click the "📥 Download SF10 File" button
4. The file will download as "SF10_All_Students.xlsx"
5. Save it to your desired location

---

## 📂 File Naming Requirements

**IMPORTANT:** Your grading sheet files MUST have the quarter in the filename:

✅ Good Names:
- "1st QTR GRADE 1 DAISY GRADING SHEET.xlsx"
- "2nd Quarter Grading.xlsx"
- "Grade1_3rd_QTR.xlsx"
- "4th QTR grades.xlsx"

❌ Bad Names (won't work):
- "Grading Sheet.xlsx" (no quarter mentioned)
- "Q GRADES.xlsx" (quarter not clear)

The system looks for: **1st**, **2nd**, **3rd**, **4th**, **first**, **second**, **third**, **fourth**

---

## 🛑 Stopping the System

When you're done:
1. Go back to the Terminal window
2. Press `Ctrl + C` (on both Mac and Windows)
3. The server will stop

---

## ❓ Troubleshooting

### "Page Can't Be Reached"
- Make sure the server is running in Terminal
- Check that you went to: http://localhost:5000

### "Could not identify quarter from filename"
- Check your filename includes the quarter (1st, 2nd, 3rd, or 4th)
- Rename the file to include the quarter

### "Error processing files"
- Make sure your grading sheets have the "SUMMARY OF QUARTERLY GRADES" tab
- Check that the template SF10.xlsx file is in the same folder

### Server Won't Start
- Make sure you're in the correct directory
- Make sure Python is installed
- Try running: `pip3 install -r requirements.txt`

---

## 💡 Tips

1. **Always keep a backup** of your original grading sheets
2. **Save downloaded SF10 files** with dates in the name (e.g., "SF10_All_Students_March2024.xlsx")
3. **You can process quarters in any order** - the system is flexible!
4. **Test with one quarter first** before doing all quarters
5. **If something goes wrong**, just close the browser and restart the server

---

## 🎓 What the System Does

1. **Reads your grading sheets** - Gets student names and grades
2. **Creates SF10 records** - One tab per student
3. **Fills in names** - Last name, First name, Middle name
4. **Fills in grades** - Only the quarters you provide
5. **Leaves other quarters blank** - So you can add them later
6. **Combines everything** - Into one convenient Excel file

---

## 📞 Need Help?

If you have any questions or issues:
1. Take a screenshot of the error
2. Note what you were trying to do
3. Contact your system administrator

---

## ✅ Quick Reference

| Task | Steps |
|------|-------|
| Start System | `python3 sf10_web_app.py` in Terminal |
| Open Interface | Go to http://localhost:5000 |
| Upload Files | Drag files to purple boxes |
| Generate | Click "Generate SF10" button |
| Download | Click download button in green message |
| Stop System | Press Ctrl+C in Terminal |

---

**Last Updated:** February 2026

**Version:** 1.0

**Created for:** Amparo Elementary School
