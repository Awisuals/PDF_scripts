# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 12:09:43 2024

@author: anter
"""
from textblob import TextBlob
from pdfminer.high_level import extract_text
import re

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def manipulate_text(text):
    # Add a line break after occurrences of (\.\.+ \d+)
    text = re.sub(r'(\.\.+ \d+)', r'\1\n', text)
    
    # Replace occurrences of \s+\.{2,}\s+ with a semicolon ;
    text = re.sub(r'\s+\.{2,}\s+', ';', text)
    
    # Delete all leading whitespaces
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)
    
    return text

def output_to_txt_file(text, output_path):
    with open(output_path, 'w') as file:
        file.write(text)


def organize_and_output_final_text(input_path, final_output_path):
    with open(input_path, 'r') as file:
        lines = file.readlines()
    
    # Filter lines to include only those with numbers after the semicolon
    filtered_lines = [line for line in lines if re.search(r';\s*\d+', line)]

    # Organize lines based on numbers occurring after semicolon
    lines_sorted = sorted(filtered_lines, key=lambda x: int(re.search(r';\s*(\d+)', x).group(1)))

    # Output the organized text to the final .txt file
    with open(final_output_path, 'w') as file:
        file.writelines(lines_sorted)


def add_tab_after_keywords(input_path, output_path, keywords):
    with open(input_path, 'r') as file:
        lines = file.readlines()
    
    # Convert keywords to lowercase for case-insensitive matching
    keywords_lower = [keyword.lower() for keyword in keywords]
    
    modified_lines = []
    for line in lines:
        # Check if the current line contains any of the keywords
        if any(keyword in line.lower() for keyword in keywords_lower):
            # add_tab = not add_tab  # Toggle the flag upon finding a keyword
            modified_lines.append(line)  # Add the current keyword line without a tab
            continue
        else:
            line = '\t' + line
        
        modified_lines.append(line)
    
    # Write the modified lines to the output file
    with open(output_path, 'w') as file:
        file.writelines(modified_lines)


def autocorrect_text_before_semicolons(text):
    # Split the text into lines
    lines = text.split('\n')

    corrected_lines = []
    for line in lines:
        # Find the index of the semicolon if it exists
        semicolon_index = line.find(';')
        if semicolon_index != -1:
            # Split the line into before and after the semicolon
            before_semicolon = line[:semicolon_index]
            after_semicolon = line[semicolon_index:]
            
            # Apply autocorrection to the text before the semicolon
            corrected_before_semicolon = str(TextBlob(before_semicolon).correct())
            
            # Reconstruct the line with the corrected text
            corrected_line = corrected_before_semicolon + after_semicolon
            corrected_lines.append(corrected_line)
        else:
            # If no semicolon, just append the line as it is
            corrected_lines.append(line)

    # Join the corrected lines back into a single text
    corrected_text = '\n'.join(corrected_lines)
    return corrected_text


def process_pdf_to_txt(pdf_path, output_path):
    text = extract_text_from_pdf(pdf_path)
    manipulated_text = manipulate_text(text)
    # corrected_text = autocorrect_text_before_semicolons(manipulated_text)
    # output_to_txt_file(corrected_text, output_path)
    output_to_txt_file(manipulated_text, output_path)

# process_pdf_to_txt_with_autocorrect('input.pdf', 'output_with_autocorrect.txt')

input_pdf = r"C:\Users\User\pdf.pdf"
output_txt1 = r"C:\Users\User\pdf.txt"
output_txt2 = output_txt1
output_txt3 = output_txt2
keywords = ["keyword1", "keyword2", "keyword3"]

print(extract_text(input_pdf))

# # Example usage
# process_pdf_to_txt(input_pdf, output_txt1)

# # Example usage
# organize_and_output_final_text(output_txt1, output_txt2)

# add_tab_after_keywords(output_txt2, output_txt3, keywords)
