# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 14:29:51 2024

@author: anter
"""
import PyPDF2

def find_smallest_page_size(pdf_path):
    points_to_mm = 25.4 / 72  # Conversion factor from points to millimeters
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        smallest_size_mm = None
        for page in reader.pages:
            page_size = page.mediabox.upper_right
            # Convert page dimensions from points to millimeters
            page_size_mm = (float(page_size[0]) * points_to_mm, float(page_size[1]) * points_to_mm)
            page_area_mm = page_size_mm[0] * page_size_mm[1]
            if smallest_size_mm is None or page_area_mm < smallest_size_mm[1]:
                smallest_size_mm = (page_size_mm, page_area_mm)
        return smallest_size_mm[0]

# Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_path = r'C:\Users\User\pdf.pdf'
smallest_page_size = find_smallest_page_size(pdf_path)
print(f"The smallest page size is in millimeters: {smallest_page_size}")
