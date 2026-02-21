# SF10 Grade Automation System

An automated Python system for generating individual SF10 (Learner Permanent Academic Record) files from quarterly grading sheets.

## Overview

This system reads student grades from a quarterly grading sheet (SUMMARY OF QUARTERLY GRADES tab) and automatically generates individual SF10 files for each student with their grades populated in the appropriate quarter column.

## Features

- **Single Workbook Output**: Generates ONE Excel file with all students as tabs (much easier to manage!)
- **Automated SF10 Generation**: Creates SF10 records for all students automatically
- **Complete Name Filling**: Fills Last Name, First Name, and Middle Name in separate fields
- **Quarterly Grade Population**: Fills grades in the correct quarter column (1st, 2nd, 3rd, or 4th)
- **Quarter Isolation**: Only fills the specified quarter, clears others
- **Subject Mapping**: Maps subjects from grading sheet to SF10 format:
  - Language
  - Reading and Literacy
  - Mathematics
  - GMRC (Good Manners and Right Conduct)
  - Makabansa
- **Flexible Output**: Choose between single workbook or separate files
- **Robust Error Handling**: Handles missing data gracefully
- **Comprehensive Testing**: 18 unit tests with full coverage

## Requirements

- Python 3.7+
- pandas
- openpyxl

## Installation

Install required dependencies:

```bash
pip install pandas openpyxl
```

## Usage

### Basic Usage (Single Workbook - Recommended)

Run the script from the command line:

```bash
python generate_sf10.py
```

This will:
1. Read student data from `1st QTR GRADE 1 DAISY GRADING SHEET.xlsx`
2. Use `SF10.xlsx` as the template
3. Generate **ONE Excel file** with 40 tabs (one per student) in the `SF10_Generated/` directory

**Output:** `SF10_All_Students_Q1.xlsx` with 40 student tabs

### Alternative: Generate Separate Files

If you prefer individual files instead of tabs, modify the `main()` function:

```python
# Create generator instance
generator = SF10Generator(
    grading_sheet_path=grading_sheet,
    sf10_template_path=sf10_template,
    output_dir='SF10_Generated'
)

# Generate separate files (old approach)
generator.generate_all_sf10s(quarter=1)
```

### Customization

For different quarters or custom output:

```python
# Single workbook approach
generator.generate_single_workbook_all_students(
    quarter=2,  # For 2nd quarter
    output_filename='SF10_All_Students_Q2.xlsx'
)

# Or separate files approach
generator.generate_all_sf10s(quarter=2)
```

## File Structure

```
.
├── generate_sf10.py              # Main automation script
├── test_generate_sf10.py         # Unit tests
├── 1st QTR GRADE 1 DAISY GRADING SHEET.xlsx  # Input grading sheet
├── SF10.xlsx                     # SF10 template
├── SF10_Generated/               # Output directory with generated files
│   ├── SF10_AGOT_KHIAN_CLOUD.xlsx
│   ├── SF10_ANDEO_JHON_PAUL.xlsx
│   └── ...
└── README.md                     # This file
```

## How It Works

### 1. Data Extraction

The system reads the `SUMMARY OF QUARTERLY GRADES` sheet from the grading file:
- Student names from column B (index 1)
- Grades from columns F-J (indices 5-9):
  - Column F: Language
  - Column G: Reading and Literacy
  - Column H: Mathematics
  - Column I: GMRC
  - Column J: Makabansa

### 2. SF10 Generation

For each student:
1. Loads the SF10 template
2. Fills the last name in row 9, column E
3. Populates grades in the quarterly rating columns:
   - 1st Quarter: Column K (index 10)
   - 2nd Quarter: Column L (index 11)
   - 3rd Quarter: Column M (index 12)
   - 4th Quarter: Column N (index 13)

### 3. File Naming

Output files are named using the format:
```
SF10_<LASTNAME>_<FIRSTNAME>.xlsx
```

Example: `SF10_AGOT_KHIAN_CLOUD.xlsx`

## Testing

Run the unit tests to verify the system:

```bash
python -m unittest test_generate_sf10 -v
```

All tests should pass with OK status.

## Output

The script generates:
- Individual SF10 file for each student
- Console output showing progress:

```
Reading student data from: 1st QTR GRADE 1 DAISY GRADING SHEET.xlsx

Found 40 students
Generating SF10 files for Quarter 1...

1. Generated: SF10_AGOT_KHIAN_CLOUD.xlsx - AGOT,KHIAN CLOUD, DABLO
2. Generated: SF10_ANDEO_JHON_PAUL.xlsx - ANDEO,JHON PAUL, ANITADO
...
40. Generated: SF10_TURALDE_SHERLYN_JHANE.xlsx - TURALDE,SHERLYN JHANE, SALAS

✅ Successfully generated 40 SF10 files in "SF10_Generated" directory
```

## Class Reference

### SF10Generator

Main class for generating SF10 files.

#### Methods

- `__init__(grading_sheet_path, sf10_template_path, output_dir='output')`: Initialize the generator
- `read_student_grades()`: Read student data from grading sheet
- `generate_sf10_for_student(student, quarter=1)`: Generate SF10 for a single student
- `generate_all_sf10s(quarter=1)`: Generate SF10 files for all students

#### Attributes

- `subject_mapping`: Dictionary mapping grading sheet subjects to SF10 subjects
- `sf10_subject_rows`: Dictionary mapping SF10 subjects to row positions
- `sf10_quarter_columns`: Dictionary mapping quarter numbers to column positions

## Troubleshooting

### Common Issues

1. **Missing openpyxl module**: Install with `pip install openpyxl`
2. **File not found**: Ensure grading sheet and SF10 template are in the same directory as the script
3. **Permission denied**: Check that you have write permissions in the output directory

## Future Enhancements

- Support for multiple quarters in a single run
- GUI interface for easier use
- Automatic final rating calculation
- Batch processing for multiple grading sheets
- Excel validation and error reporting

## License

This project is created for educational purposes.

## Author

Created for Amparo Elementary School grading automation.
