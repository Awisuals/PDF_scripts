# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 12:50:40 2024

@author: anter
"""

import fitz  # Import PyMuPDF

def extract_and_format_text(pdf_path):
    formatted_text = []  # List to hold the formatted lines of text

    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text = page.get_text("text")
            lines = text.split('\n')  # Split text into lines

            for line in lines:
                # Custom logic to identify and format lines with titles and page numbers
                if "..." in line:
                    # Remove dots and any excess spaces
                    line = line.replace('.', '').strip()
                    # Split line based on the last space (assuming it separates title from page number)
                    parts = line.rsplit(' ', 1)
                    if len(parts) == 2:  # Ensure line split into two parts: title and page number
                        title, page_number = parts
                        # Reformat line as per the desired output
                        formatted_line = f"{title};{page_number} \n"
                        formatted_text.append(formatted_line)
            
    # Join all formatted lines into a single string
    return ''.join(formatted_text)

# Example usage
pdf_path = r"C:\Users\user\PDF.pdf"  # Path to your PDF file
formatted_text = extract_and_format_text(pdf_path)
print(formatted_text)
