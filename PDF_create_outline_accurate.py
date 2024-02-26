# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 11:21:14 2024

@author: anter
"""
import argparse
import sys
import fitz  # PyMuPDF
import os


def parse_bookmarks(text_file_path, adjust_page):
    """
    Parses a text file containing bookmarks, their page numbers, and indent levels based on leading spaces or tabs.
    
    Parameters:
    - text_file_path: Path to the text file.
    
    Returns:
    - A list of tuples, where each tuple contains the bookmark name, page number, and level of indentation.
    """
    bookmarks = []
    tab_size = 4  # Assuming 1 tab = 4 spaces; adjust as needed
    with open(text_file_path, 'r') as file:
        for line in file:
            # Normalize tabs to spaces
            normalized_line = line.replace('\t', ' ' * tab_size)
            
            # Count leading spaces to determine the level
            leading_spaces = len(normalized_line) - len(normalized_line.lstrip(' '))
            level = leading_spaces // 4  # Assuming 2 spaces per level; adjust as needed
            
            # Split each line by semicolon
            parts = normalized_line.strip().split(';')
            if len(parts) == 2:
                bookmark_name, page_str = parts
                try:
                    page = int(page_str.strip()) + adjust_page  # Adjust page number to correct page
                    bookmarks.append((level, bookmark_name, page))
                except ValueError:
                    print("\n"+f"Warning: Invalid page number '{page_str}' for bookmark '{bookmark_name}'. Skipping.")
            else:
                print("\n"+f"Warning: Invalid format in line '{normalized_line.strip()}'. Skipping.")
    return bookmarks


def add_bookmarks_to_pdf(pdf_file_path, bookmarks, output_pdf_path):
    """
    Adds hierarchical bookmarks to a PDF file based on levels indicated by leading spaces in the bookmark name,
    and saves the result to a new file using PyMuPDF.
    
    Parameters:
    - pdf_file_path: Path to the source PDF file.
    - bookmarks: A list of tuples, where each tuple contains the level of indentation, bookmark name, and page number.
    - output_pdf_path: Path to save the modified PDF file.
    """
    # Open the PDF
    doc = fitz.open(pdf_file_path)
    toc = doc.get_toc(simple=False)  # Get current TOC (if exists), simple=False for the detailed TOC
    toc = []
    
    # Add bookmarks with hierarchy
    for level, bookmark_name, page in bookmarks:
        if page < doc.page_count:
            toc.append([level + 1, bookmark_name, page])  # `level + 1` because PyMuPDF levels start at 1
        else:
            print("\n"+f"Warning: Page number {page+1} for bookmark '{bookmark_name}' is out of range. Skipping.")
    
    doc.set_toc(toc)  # Update the document's TOC
    
    # Save the modified PDF
    doc.save(output_pdf_path, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()
    print("\n"+f"Modified PDF saved to '{output_pdf_path}'.")



def replace_original_with_new(original_path, new_path):
    """
    Deletes the original file and renames the new file to the original file's name.

    :param original_path: Path to the original PDF file.
    :param new_path: Path to the new PDF file.
    """
    try:
        os.remove(original_path)  # Delete the original file
        os.rename(new_path, original_path)  # Rename the new file
        print("\n"+f"Replaced {original_path} and renamed {new_path} to {original_path}")
    except Exception as e:
        print("\n"+f"Error replacing file: {e}")


def main(text_file_path, pdf_file_path, output_pdf_path, replace, adjust_page):
    
    # Step 1: Parse the bookmarks from the text file
    bookmarks = parse_bookmarks(text_file_path, adjust_page)
    
    # Step 2: Add bookmarks to the PDF
    add_bookmarks_to_pdf(
        pdf_file_path, bookmarks, output_pdf_path)
    
    # Conditionally replace the original file
    if replace:
        replace_original_with_new(pdf_file_path, output_pdf_path)


if __name__ == "__main__":    
    
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Add bookmarks to a PDF file based on a text file.")
    
    # Add arguments
    parser.add_argument(
        "text_file_path", 
        help="Path to the text file containing bookmarks and page numbers.")
    parser.add_argument(
        "pdf_file_path", 
        help="Path to the PDF file to which bookmarks will be added.")
    parser.add_argument(
        "output_pdf_path", 
        help="Path to save the modified PDF file with bookmarks.")
    parser.add_argument(
        '-r', '--replace', action='store_true', 
        help='Replace the original file and rename the new file to the original name')
    parser.add_argument(
        "-ap", "--adjust_page", type=int, default=1,
        help='Adjust the placing of the outline based on pdf paging.')
    
    # Set False for CLI usage and True for debugging
    DEBUG = False
    if DEBUG:
        # Use predefined arguments
        args = parser.parse_args(
            [r'C:\Users\anter\Documents\42\harrasteet\DnD\Supplements\tashas_cualdron_of_everything_content.txt',
             r'C:\Users\anter\Documents\42\harrasteet\DnD\Supplements\DnD5e_WotC_Tashas_Cauldron_of_Everything.pdf',
             r'C:\Users\anter\Documents\42\harrasteet\DnD\Supplements\DnD5e_WotC_Tashas_Cauldron_of_Everything_outlined.pdf'
              ]) #,'--replace' # Use this as fourth argument as needed in debugging
    else:
        # Parse arguments from the command line
        args = parser.parse_args()

    main(
        args.text_file_path, 
        args.pdf_file_path, 
        args.output_pdf_path, 
        args.replace, args.adjust_page)

