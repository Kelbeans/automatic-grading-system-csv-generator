"""
Test SF10 file detection with various filenames
"""

import unittest
import os
import tempfile
import shutil
from openpyxl import load_workbook
from sf10_web_app import is_sf10_file
from generate_sf10 import SF10Generator


class TestSF10Detection(unittest.TestCase):
    """Test SF10 file detection by content, not filename"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.grading_sheet = 'assets/docs/1st QTR GRADE 1 DAISY GRADING SHEET.xlsx'
        self.sf10_template = 'assets/docs/SF10.xlsx'

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_detect_sf10_with_standard_name(self):
        """Test detection of SF10 with standard name"""
        generator = SF10Generator(
            grading_sheet_path=self.grading_sheet,
            sf10_template_path=self.sf10_template,
            output_dir=self.test_dir
        )

        # Generate a standard SF10 file
        output_path = generator.generate_single_workbook_all_students(
            quarter=1,
            output_filename='SF10_All_Students.xlsx'
        )

        # Should be detected as SF10
        self.assertTrue(is_sf10_file(output_path))

    def test_detect_sf10_with_custom_name(self):
        """Test detection of SF10 with custom/unusual name"""
        generator = SF10Generator(
            grading_sheet_path=self.grading_sheet,
            sf10_template_path=self.sf10_template,
            output_dir=self.test_dir
        )

        # Generate SF10 with various non-standard names
        test_names = [
            'MyGrades.xlsx',
            'Student_Records_2024.xlsx',
            'Q1_Complete.xlsx',
            'Grade1_DAISY.xlsx',
            'Random_Name_123.xlsx'
        ]

        for filename in test_names:
            output_path = generator.generate_single_workbook_all_students(
                quarter=1,
                output_filename=filename
            )

            # Should still be detected as SF10 regardless of name
            result = is_sf10_file(output_path)
            self.assertTrue(
                result,
                f"Failed to detect SF10 with filename: {filename}"
            )

    def test_not_detect_grading_sheet_as_sf10(self):
        """Test that grading sheets are NOT detected as SF10"""
        # The grading sheet should not be detected as SF10
        self.assertFalse(is_sf10_file(self.grading_sheet))

    def test_not_detect_template_as_sf10(self):
        """Test that the template is NOT detected as SF10 (only has 1 sheet)"""
        # The template only has 1 sheet, so should not be detected as SF10
        self.assertFalse(is_sf10_file(self.sf10_template))

    def test_detect_sf10_by_structure(self):
        """Test that detection works by checking structure, not name"""
        generator = SF10Generator(
            grading_sheet_path=self.grading_sheet,
            sf10_template_path=self.sf10_template,
            output_dir=self.test_dir
        )

        # Generate with a name that doesn't include "SF10" at all
        output_path = generator.generate_single_workbook_all_students(
            quarter=1,
            output_filename='records.xlsx'  # No "SF10" in name
        )

        # Load and verify it has the right structure
        wb = load_workbook(output_path)

        # Should have multiple sheets
        self.assertGreater(len(wb.sheetnames), 5)

        # Should have names in row 9
        first_sheet = wb[wb.sheetnames[0]]
        self.assertIsNotNone(first_sheet.cell(row=9, column=5).value)

        # Should be detected as SF10
        self.assertTrue(is_sf10_file(output_path))


if __name__ == '__main__':
    unittest.main()
