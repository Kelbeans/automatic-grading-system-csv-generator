# SF10 Grade Automation System

A modern web-based automation system for generating SF10 (Learner Permanent Academic Record) files from quarterly grading sheets for DepED schools.

**Developed by Kelvin A. Malabanan** - Software Engineer

## Overview

This system provides both a web interface and command-line tool to automatically generate SF10 files from quarterly grading sheets. It features drag-and-drop file upload, multi-quarter processing, and professional document generation with embedded DepED and Kagawaran ng Edukasyon logos.

## Features

### Web Interface
- **Drag & Drop Upload**: User-friendly interface for non-technical users
- **Multi-Quarter Support**: Process multiple quarters at once (1st, 2nd, 3rd, 4th)
- **Learners Profile Integration**: Optional upload to auto-fill LRN, Birthday, and Sex fields
- **Smart File Detection**: Automatically identifies SF10 files by structure, not filename
- **Backwards Compatible**: Can add quarters to existing SF10 files
- **Professional UI**: Modern design with Poppins font and clean layout

### Core Automation
- **Single Workbook Output**: Generates one Excel file with all students as separate tabs
- **Complete Name Mapping**: Fills Last Name, First Name, and Middle Name in correct fields
- **Learner Profile Auto-Fill**: Optionally auto-fills LRN, Birthday, and Sex from learners profile file
- **Quarter Isolation**: Only fills specified quarters, preserves existing data
- **Logo Embedding**: Automatically adds DepED and Kagawaran ng Edukasyon logos with transparent backgrounds
- **Template Preservation**: Maintains all merged cells and formatting from original SF10 template
- **Subject Mapping**: Correctly maps subjects from grading sheet to SF10:
  - Language
  - Reading and Literacy
  - Mathematics
  - GMRC (Good Manners and Right Conduct)
  - Makabansa

## Requirements

### System Requirements
```
Python 3.7+
Flask==2.3.0
Flask-CORS==4.0.0
pandas==2.0.0
openpyxl==3.1.0
Pillow==10.0.0
```

### Grading Sheet Format

Your grading sheet must have a sheet named **"SUMMARY OF QUARTERLY GRADES "** (with trailing space) with:
- **Column B** (index 1): Student names in format "LASTNAME,FIRSTNAME, MIDDLE"
- **Column F** (index 5): Language grades
- **Column G** (index 6): Reading and Literacy grades
- **Column H** (index 7): Mathematics grades
- **Column I** (index 8): GMRC grades
- **Column J** (index 9): Makabansa grades
- Student data starts at **row 10**

Filename should include quarter identifier: "1st", "2nd", "3rd", or "4th"

## Installation

1. Clone or download the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Production Deployment (Live)

🌐 **Access the live application**: http://54.206.157.216

No installation needed - just visit the URL and start uploading grading sheets!

### Windows Users (Local)

**Easiest method** - Just double-click:
- `START_WEB_APP.bat` (recommended)
- Or `START_WEB_APP.ps1` (PowerShell)

The browser will open automatically to `http://localhost:8080`

📖 **Windows guide**: See [WINDOWS_SETUP.md](WINDOWS_SETUP.md)

### Web Interface (Mac/Linux)

1. Start the web server:
```bash
python sf10_web_app.py
```

2. Open your browser to `http://localhost:8080`

3. Upload your files:
   - **Grading Sheets**: Drag and drop quarterly grading sheets (filename should include "1st", "2nd", "3rd", or "4th")
   - **Learners Profile** (Optional): Upload to auto-fill LRN, Birthday, and Sex fields
   - **Existing SF10** (Optional): Upload an existing SF10 to add more quarters

4. Click "Generate SF10 Records" and download your completed file

### Command Line

```bash
python generate_sf10.py your_grading_sheet.xlsx
```

Example:
```bash
python generate_sf10.py "1st Quarter Grades.xlsx"
```

This will process your grading sheet and generate `SF10_All_Students_Q1.xlsx` in the `output/` directory.

## Project Structure

```
SF10-Grade-Automation/
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD GitHub Actions
├── assets/
│   ├── docs/               # Documentation and templates
│   │   ├── SF10.xlsx       # SF10 template (required)
│   │   └── USER_GUIDE.md   # User guide
│   └── img/                # Logo images
│       ├── 95c51f57-dfdc-418a-bf4c-54acb45308be-removebg-preview.png  # DepED logo
│       └── c128a1b0-b3b3-492b-84f3-6624923eb8b4-removebg-preview.png  # Kagawaran seal
├── static/
│   ├── css/
│   │   └── style.css       # Professional UI styling
│   └── js/
│       └── app.js          # Client-side logic
├── templates/
│   └── index.html          # Web interface
├── terraform/
│   ├── main.tf             # AWS infrastructure
│   ├── variables.tf        # Configuration variables
│   ├── outputs.tf          # Deployment outputs
│   ├── user_data.sh        # Bootstrap script
│   └── README.md           # Deployment guide
├── tests/
│   ├── test_generate_sf10.py
│   ├── test_sf10_detection.py
│   └── test_server.py
├── generate_sf10.py        # Core automation engine
├── sf10_web_app.py         # Flask web application
├── START_WEB_APP.bat       # Windows startup (batch)
├── START_WEB_APP.ps1       # Windows startup (PowerShell)
├── WINDOWS_SETUP.md        # Windows user guide
├── requirements.txt
└── README.md
```

## How It Works

### 1. File Upload & Quarter Detection
- Grading sheets are automatically identified by quarter from filename
- Existing SF10 files are detected by structure (20+ sheets, merged cells, subject indicators)

### 2. Data Processing
The system reads the `SUMMARY OF QUARTERLY GRADES` sheet:
- **Student names** from column B (parsed into Last, First, Middle)
- **Grades** from columns F-J:
  - Column F: Language
  - Column G: Reading and Literacy
  - Column H: Mathematics
  - Column I: GMRC
  - Column J: Makabansa

### 3. SF10 Generation
For each student, the system:
1. Creates a new sheet by copying the SF10 template
2. Fills name fields in row 9:
   - Column E (5): Last Name
   - Column Q (17): First Name
   - Column AP (42): Middle Name
3. Fills learner profile data in row 10 (if profile uploaded):
   - Column J (10): LRN (Learner Reference Number)
   - Column U (21): Birthday
   - Column AS (45): Sex
4. Populates grades in the correct quarter column:
   - **1st Quarter**: Column K (10)
   - **2nd Quarter**: Column L (11)
   - **3rd Quarter**: Column M (12)
   - **4th Quarter**: Column N (13)
5. Embeds DepED and Kagawaran ng Edukasyon logos with exact positioning:
   - **Kagawaran Seal**: 87pt × 90pt at X=43pt, Y=0pt
   - **DepED Logo**: 137pt × 137pt at X=821pt, Y=-24pt
6. Preserves all 497 merged cells from the template

### 4. Multi-Quarter Processing
When adding to an existing SF10:
- Merges new quarter data with existing records
- Updates only the new quarter columns
- Preserves all existing student data
- Maintains formatting and logos

## API Reference

### SF10Generator Class

Main class for SF10 generation.

#### Constructor
```python
SF10Generator(
    grading_sheet_path,
    sf10_template_path,
    output_dir='output',
    learners_profile_path=None  # Optional: path to learners profile file
)
```

#### Key Methods
- `read_student_grades()` - Read student data from grading sheet
- `generate_sf10_for_student(student, quarter)` - Generate SF10 for one student
- `generate_single_workbook_all_students(quarter, output_filename)` - Generate single workbook with all students

### Web Application

#### Endpoints
- `GET /` - Web interface
- `POST /upload` - Process grading sheets and generate SF10
- `GET /download/<filename>` - Download generated file

#### Response Format
```json
{
  "success": true,
  "message": "SF10 generated successfully",
  "quarters": [1, 2],
  "download_url": "/download/SF10_All_Students.xlsx"
}
```

## Testing

Run all unit tests:
```bash
python -m unittest discover tests/ -v
```

Run specific test suite:
```bash
python -m unittest tests.test_generate_sf10 -v
python -m unittest tests.test_sf10_detection -v
```

**Test Coverage**: 25 unit tests covering:
- Name field mapping
- Quarter isolation
- Merged cell preservation
- Multi-quarter processing
- SF10 file detection
- Logo embedding

## Customization

### Change Output Directory
```python
generator = SF10Generator(
    grading_sheet_path='your_file.xlsx',
    sf10_template_path='assets/docs/SF10.xlsx',
    output_dir='custom_output'
)
```

### Process Different Quarters
```python
generator.generate_single_workbook_all_students(
    quarter=3,  # 3rd quarter
    output_filename='SF10_Q3.xlsx'
)
```

## Troubleshooting

### Port 5000 Already in Use (macOS)
The app uses port 8080 to avoid conflicts with AirPlay on macOS.

### Logo Images Not Showing
Ensure PNG logo files are in `assets/img/` directory with transparent backgrounds.

### Test Files Not Found
Tests reference files in `assets/docs/`. Ensure paths are correct.

### Permission Errors
Run with appropriate permissions or check output directory write access.

## Technical Details

### Logo Positioning
- Uses OpenPyXL OneCellAnchor with XDRPositiveSize2D
- Exact EMU (English Metric Units) conversion: 1pt = 12700 EMU
- Transparent PNG images for clean overlay

### File Detection Algorithm
SF10 files are identified by:
- 20+ sheets (one per student)
- Name field at row 9, column 5
- Subject indicators in rows 30-32
- 100+ merged cells

## Deployment

### Production (AWS)

🌐 **Live Application**: http://54.206.157.216

**Current Deployment**:
- **Region**: ap-southeast-2 (Sydney, Australia)
- **Instance**: i-040b8fd5ef5e3bb3d (t3.micro)
- **IP**: 54.206.157.216
- **Stack**: Nginx + Gunicorn + Flask on Ubuntu 22.04
- **Status**: ✅ Running

**Update Deployment**:
```bash
ssh -i ~/.ssh/id_rsa ubuntu@54.206.157.216
cd /home/sf10app
./deploy.sh
```

### Deploy Your Own Instance (Terraform)

**One-command deployment** to AWS with automatic infrastructure provisioning!

```bash
cd terraform
terraform init
terraform apply
```

Features:
- ✅ **Auto-provisions** EC2, Security Groups, Elastic IP
- ✅ **CI/CD ready** - automatic deployments on git push
- ✅ **Free tier eligible** - t3.micro instance (12 months free)
- ✅ **Production-ready** - Nginx + Gunicorn + systemd
- ✅ **Always on** - no spin-down delays
- ✅ **1GB RAM** - handles 40+ students easily

**Cost**: Free for 12 months, then ~$10/month

📖 **Complete guide**: See [terraform/README.md](terraform/README.md)

### Local Development

#### Windows
Double-click `START_WEB_APP.bat` or see [WINDOWS_SETUP.md](WINDOWS_SETUP.md)

#### Mac/Linux
```bash
python sf10_web_app.py
# Open http://localhost:8080
```

## License

Created for educational purposes for DepED schools.

## Author

**Kelvin A. Malabanan** - Software Engineer
GitHub: [Kelbeans](https://github.com/Kelbeans)

## Acknowledgments

- Uses DepED official SF10 format
- Kagawaran ng Edukasyon and DepED logos remain property of the Department of Education

## Changelog

### v2.1 (Current - February 2026)
- 👤 **Learners Profile Feature** - Optional upload to auto-fill LRN, Birthday, and Sex fields
- 🔍 **Smart Name Matching** - Handles comma spacing variations in student names
- 🚀 **AWS Production Deployment** - Live at http://54.206.157.216
- 🏗️ **Terraform Infrastructure** - One-command AWS deployment
- 🪟 **Windows Support** - Double-click startup scripts (.bat and .ps1)
- 📖 **Windows Setup Guide** - Non-technical user documentation
- 🌏 **Sydney Region** - Deployed to ap-southeast-2 for optimal performance
- ⚙️ **Production Stack** - Nginx + Gunicorn + systemd with auto-restart

### v2.0
- Web interface with drag-and-drop
- Multi-quarter support
- Smart SF10 file detection
- Logo embedding with exact positioning
- Professional UI with Poppins font
- Proper MVC project structure

### v1.0
- Initial command-line version
- Single quarter processing
- Basic SF10 generation
