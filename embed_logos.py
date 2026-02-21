"""
Embed logos into SF10 template in a format that can be properly copied
"""
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import shutil

print("="*70)
print("Embedding Logos into SF10 Template")
print("="*70)

# Backup the original template
print("\n1. Creating backup of SF10.xlsx...")
shutil.copy('SF10.xlsx', 'SF10_backup.xlsx')
print("   ✓ Backup saved as: SF10_backup.xlsx")

# Load the template
print("\n2. Loading SF10 template...")
wb = load_workbook('SF10.xlsx')
ws = wb.active

# Remove existing images (they're in VML format and cause issues)
print("\n3. Clearing old images...")
ws._images = []

# Add the DepED seal (left side)
print("\n4. Adding Kagawaran ng Edukasyon seal (left)...")
deped_seal = Image('c128a1b0-b3b3-492b-84f3-6624923eb8b4-removebg-preview.png')
# Resize to fit nicely (about 1 inch = 96 pixels)
deped_seal.width = 80
deped_seal.height = 80
# Position at cell A1 (top-left)
deped_seal.anchor = 'A1'
ws.add_image(deped_seal)
print("   ✓ Kagawaran seal added at cell A1 (transparent background)")

# Add the DepED logo (right side)
print("\n5. Adding DepED Department of Education logo (right)...")
deped_logo = Image('95c51f57-dfdc-418a-bf4c-54acb45308be-removebg-preview.png')
# Resize to fit nicely
deped_logo.width = 120
deped_logo.height = 60
# Position at cell T1 (top-right area)
deped_logo.anchor = 'T1'
ws.add_image(deped_logo)
print("   ✓ DepED logo added at cell T1 (transparent background)")

# Save the template
print("\n6. Saving updated template...")
wb.save('SF10.xlsx')
print("   ✓ Template saved successfully!")

print("\n" + "="*70)
print("✅ DONE! Logos embedded in SF10.xlsx")
print("="*70)
print("\nThe logos are now properly embedded and will be copied")
print("to all generated SF10 files automatically!")
print("\nYou can restore the original with: SF10_backup.xlsx")
