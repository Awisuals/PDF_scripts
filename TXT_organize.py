# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 17:54:55 2024

@author: anter
"""
import re

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
        
input_path = r"C:\Users\anter\Documents\42\Harrasteet\dnd\5e_AiME_players_guide.txt"
output_path = input_path
organize_and_output_final_text(input_path, output_path)
