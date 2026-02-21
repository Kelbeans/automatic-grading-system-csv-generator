"""
SF10 Grade Automation System
Generates individual SF10 files for each student with their 1st quarter grades
"""

import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import os
from pathlib import Path


class SF10Generator:
    """Handles the generation of SF10 files for students"""

    def __init__(self, grading_sheet_path, sf10_template_path, output_dir='output'):
        """
        Initialize the SF10 Generator

        Args:
            grading_sheet_path: Path to the grading sheet Excel file
            sf10_template_path: Path to the SF10 template Excel file
            output_dir: Directory where generated SF10 files will be saved
        """
        self.grading_sheet_path = grading_sheet_path
        self.sf10_template_path = sf10_template_path
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        Path(self.output_dir).mkdir(exist_ok=True)

        # Define subject mapping between SUMMARY sheet and SF10
        self.subject_mapping = {
            'LANGUAGE': 'Language',
            'READING AND LITERACY': 'Reading and Literacy',
            'MATH': 'Mathematics',
            'GMRC': 'GMRC (Good Manners and Right Conduct)',
            'MAKABANSA': 'Makabansa'
        }

        # SF10 row positions for each subject (0-indexed)
        self.sf10_subject_rows = {
            'Language': 29,
            'Reading and Literacy': 30,
            'Mathematics': 31,
            'GMRC (Good Manners and Right Conduct)': 32,
            'Makabansa': 33
        }

        # Column positions in SF10 (0-indexed)
        self.sf10_quarter_columns = {
            1: 10,  # 1st quarter in column K (index 10)
            2: 11,  # 2nd quarter in column L (index 11)
            3: 12,  # 3rd quarter in column M (index 12)
            4: 13   # 4th quarter in column N (index 13)
        }

    def read_student_grades(self):
        """
        Read student data and grades from the SUMMARY sheet

        Returns:
            List of dictionaries containing student information and grades
        """
        # Read the SUMMARY sheet
        df = pd.read_excel(
            self.grading_sheet_path,
            sheet_name='SUMMARY OF QUARTERLY GRADES ',
            header=None
        )

        students = []

        # Start reading from row 10 (0-indexed: row 10 is the first student)
        # Row 7 has headers, row 9 has "MALE", row 10 starts student data
        start_row = 10

        for idx in range(start_row, len(df)):
            row = df.iloc[idx]

            # Check if we have valid student data
            if pd.isna(row[1]) or row[1] == '':
                continue

            # Extract student name (column 1)
            student_name = str(row[1]).strip()

            # Skip if this is a header row or empty
            if student_name in ['MALE', 'FEMALE', "LEARNERS' NAMES", '']:
                continue

            # Extract grades from columns 5-9 with safe access
            def safe_get_grade(row, col_idx):
                """Safely get grade value from row, handling missing columns"""
                try:
                    value = row[col_idx] if col_idx in row.index else 0
                    return value if not pd.isna(value) else 0
                except (KeyError, IndexError):
                    return 0

            grades = {
                'LANGUAGE': safe_get_grade(row, 5),
                'READING AND LITERACY': safe_get_grade(row, 6),
                'MATH': safe_get_grade(row, 7),
                'GMRC': safe_get_grade(row, 8),
                'MAKABANSA': safe_get_grade(row, 9)
            }

            students.append({
                'name': student_name,
                'grades': grades
            })

        return students

    def generate_sf10_for_student(self, student, quarter=1):
        """
        Generate an SF10 file for a single student

        Args:
            student: Dictionary containing student name and grades
            quarter: Quarter number (1-4, default is 1)
        """
        # Load the SF10 template
        wb = load_workbook(self.sf10_template_path)
        ws = wb.active

        # Parse student name (format: "LAST,FIRST, MIDDLE")
        student_name = student['name']
        name_parts = student_name.split(',')
        last_name = name_parts[0].strip() if len(name_parts) > 0 else ''
        first_name = name_parts[1].strip() if len(name_parts) > 1 else ''
        middle_name = name_parts[2].strip() if len(name_parts) > 2 else ''

        # Update the name fields in the SF10
        # In openpyxl, rows and columns are 1-indexed
        # Row 9, Column E (5): Last Name
        ws.cell(row=9, column=5, value=last_name)

        # Row 9, Column Q (17): First Name
        ws.cell(row=9, column=17, value=first_name)

        # Row 9, Column AP (42): Middle Name
        ws.cell(row=9, column=42, value=middle_name)

        # Fill in the grades for each subject in the appropriate quarter column
        quarter_col = self.sf10_quarter_columns[quarter]

        for summary_subject, sf10_subject in self.subject_mapping.items():
            grade = student['grades'].get(summary_subject, 0)
            row_idx = self.sf10_subject_rows[sf10_subject]

            # openpyxl uses 1-indexed rows/columns
            ws.cell(row=row_idx + 1, column=quarter_col + 1, value=grade)

            # Clear other quarter columns (only fill the specified quarter)
            for q in range(1, 5):
                if q != quarter:
                    other_col = self.sf10_quarter_columns[q]
                    # Use empty string to clear the cell (None doesn't work in openpyxl)
                    ws.cell(row=row_idx + 1, column=other_col + 1).value = ''

        # Generate output filename
        # Clean the name for filename (remove commas, spaces, special chars)
        safe_name = last_name.replace(',', '').replace(' ', '_')
        output_filename = f'SF10_{safe_name}_{first_name.replace(" ", "_")}.xlsx'
        output_path = os.path.join(self.output_dir, output_filename)

        # Save the workbook
        wb.save(output_path)

        return output_path

    def generate_all_sf10s(self, quarter=1):
        """
        Generate SF10 files for all students

        Args:
            quarter: Quarter number (1-4, default is 1)

        Returns:
            List of generated file paths
        """
        print(f'Reading student data from: {self.grading_sheet_path}')
        students = self.read_student_grades()

        print(f'\nFound {len(students)} students')
        print(f'Generating SF10 files for Quarter {quarter}...\n')

        generated_files = []

        for idx, student in enumerate(students, 1):
            try:
                output_path = self.generate_sf10_for_student(student, quarter)
                print(f'{idx}. Generated: {os.path.basename(output_path)} - {student["name"]}')
                generated_files.append(output_path)
            except Exception as e:
                print(f'{idx}. ERROR generating SF10 for {student["name"]}: {str(e)}')

        print(f'\n✅ Successfully generated {len(generated_files)} SF10 files in "{self.output_dir}" directory')

        return generated_files

    def generate_single_workbook_all_students(self, quarter=1, output_filename='SF10_All_Students.xlsx'):
        """
        Generate a single Excel workbook with one sheet per student
        Preserves images/logos from template by copying the entire workbook structure

        Args:
            quarter: Quarter number (1-4, default is 1)
            output_filename: Name of the output file

        Returns:
            Path to the generated workbook
        """
        import shutil
        from copy import copy

        print(f'Reading student data from: {self.grading_sheet_path}')
        students = self.read_student_grades()

        print(f'\nFound {len(students)} students')
        print(f'Generating single workbook with {len(students)} tabs for Quarter {quarter}...\n')

        # Create output path
        output_path = os.path.join(self.output_dir, output_filename)

        # Copy the template file to preserve all media/drawings
        shutil.copy(self.sf10_template_path, output_path)

        # Load the copied workbook
        output_wb = load_workbook(output_path)
        template_ws = output_wb.active  # This is the template sheet with images

        for idx, student in enumerate(students, 1):
            try:
                # Parse student name for sheet name
                student_name = student['name']
                name_parts = student_name.split(',')
                last_name = name_parts[0].strip() if len(name_parts) > 0 else ''
                first_name = name_parts[1].strip() if len(name_parts) > 1 else ''
                middle_name = name_parts[2].strip() if len(name_parts) > 2 else ''

                # Create a clean sheet name (max 31 chars, no special chars)
                sheet_name = f"{last_name[:15]} {first_name[:10]}".strip()
                # Remove invalid characters for sheet names
                for char in [':', '\\', '/', '?', '*', '[', ']']:
                    sheet_name = sheet_name.replace(char, '')

                # Copy the template sheet (this preserves images/drawings)
                new_ws = output_wb.copy_worksheet(template_ws)
                new_ws.title = sheet_name

                # Now fill in the student data
                # Update the name fields
                new_ws.cell(row=9, column=5, value=last_name)
                new_ws.cell(row=9, column=17, value=first_name)
                new_ws.cell(row=9, column=42, value=middle_name)

                # Fill in the grades for the specified quarter
                quarter_col = self.sf10_quarter_columns[quarter]

                for summary_subject, sf10_subject in self.subject_mapping.items():
                    grade = student['grades'].get(summary_subject, 0)
                    row_idx = self.sf10_subject_rows[sf10_subject]

                    # Fill the grade
                    new_ws.cell(row=row_idx + 1, column=quarter_col + 1, value=grade)

                    # Clear other quarter columns
                    for q in range(1, 5):
                        if q != quarter:
                            other_col = self.sf10_quarter_columns[q]
                            new_ws.cell(row=row_idx + 1, column=other_col + 1).value = ''

                print(f'{idx}. Added sheet: {sheet_name} - {student["name"]}')

            except Exception as e:
                print(f'{idx}. ERROR adding sheet for {student["name"]}: {str(e)}')

        # Remove the original template sheet (it was only used for copying)
        output_wb.remove(template_ws)

        # Save the workbook
        output_wb.save(output_path)

        # Manually copy media files and drawings from template to preserve logos
        try:
            from zipfile import ZipFile
            import tempfile as tmp

            # Create a temp file for the updated workbook
            temp_output = tmp.NamedTemporaryFile(delete=False, suffix='.xlsx')
            temp_output.close()

            # Copy the saved workbook to temp
            shutil.copy(output_path, temp_output.name)

            # Extract media and drawing files from template
            with ZipFile(self.sf10_template_path, 'r') as template_zip:
                media_files = [f for f in template_zip.namelist() if 'media/' in f or 'drawing' in f.lower()]

                # Add them to the output workbook
                with ZipFile(temp_output.name, 'r') as output_zip_read:
                    with ZipFile(output_path, 'w') as output_zip_write:
                        # Copy all existing files from output
                        for item in output_zip_read.namelist():
                            data = output_zip_read.read(item)
                            output_zip_write.writestr(item, data)

                        # Add media and drawing files from template
                        for media_file in media_files:
                            data = template_zip.read(media_file)
                            output_zip_write.writestr(media_file, data)

            # Clean up temp file
            os.unlink(temp_output.name)
            print('   ✓ Logos and images copied successfully')

        except Exception as e:
            print(f'   ⚠ Warning: Could not copy images: {e}')

        print(f'\n✅ Successfully generated single workbook with {len(output_wb.sheetnames)} sheets')
        print(f'   Saved to: {output_path}')

        return output_path


def main():
    """Main function to run the SF10 generation"""

    # Define file paths
    grading_sheet = '1st QTR GRADE 1 DAISY GRADING SHEET.xlsx'
    sf10_template = 'SF10.xlsx'

    # Create generator instance
    generator = SF10Generator(
        grading_sheet_path=grading_sheet,
        sf10_template_path=sf10_template,
        output_dir='SF10_Generated'
    )

    # Generate single workbook with all students for 1st quarter
    generator.generate_single_workbook_all_students(quarter=1, output_filename='SF10_All_Students_Q1.xlsx')


if __name__ == '__main__':
    main()
