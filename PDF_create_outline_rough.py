# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 13:50:09 2024

@author: anter
"""
import fitz  # PyMuPDF
import argparse
import os
import sys


def search_keywords_in_pdf(pdf_path, keywords):
    """
    Search for keywords in the specified PDF and 
    return a list of pages where each keyword was found.
    
    :param pdf_path: Path to the PDF file.
    :param keywords: List of keywords or sentences to search for.
    :return: Dictionary with keywords as keys and a list of 
             page numbers as values.
    """
    doc = fitz.open(pdf_path)
    results = {keyword: [] for keyword in keywords}
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        for keyword in keywords:
            if keyword.lower() in text.lower():  # Case insensitive search
                results[keyword].append(page_num + 1)  # Page numbers are 1-based for human readability
    
    doc.close()
    return results


def add_outline_to_pdf(pdf_path, search_results, output_pdf_path):
    """
    Add an outline to the PDF for each keyword found on specific pages using the Table of Contents (TOC).
    
    :param pdf_path: Path to the original PDF file.
    :param search_results: Dictionary with keywords as keys and a list of page numbers as values.
    :param output_pdf_path: Path to save the modified PDF with outlines.
    """
    doc = fitz.open(pdf_path)
    toc = doc.get_toc(simple=False)  # Get current TOC (if exists), simple=False for the detailed TOC

    for keyword, pages in search_results.items():
        for page_num in pages:
            # Each TOC entry is a list: [level, title, page, ...]
            # Level 1 for top-level entries; adjust as needed for hierarchical outlines
            
            toc.append([1, f"{keyword} on page {page_num}", page_num])

    doc.set_toc(toc)  # Update the document's TOC
    doc.save(output_pdf_path, garbage=4, deflate=True, clean=True)
    doc.close()


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


def main():
    parser = argparse.ArgumentParser(
        description='Rough PDF Outline Creator based on Keywords')
    parser.add_argument(
        'pdf_path', type=str,
        help='Path to the input PDF file')
    parser.add_argument(
        'output_pdf_path', type=str,
        help='Path to the output PDF file with outlines')
    parser.add_argument(
        '-k', '--keywords', type=str, nargs='+',
        help='Keywords to search for in the PDF')
    parser.add_argument(
        '-r', '--replace', action='store_true', 
        help='Replace the original file and rename the new file to the original name')

    args = parser.parse_args()

    try:
        if args.keywords:
            search_results = search_keywords_in_pdf(args.pdf_path, args.keywords)
            add_outline_to_pdf(args.pdf_path, search_results, args.output_pdf_path)
            print("\n"+f"Processed {args.pdf_path} and saved outlines to {args.output_pdf_path}")
        else:
            print("\n"+"No keywords provided for searching.")
        print("\n"+"PDF outlined and saved successfully.")
    except FileNotFoundError:
        print("\n"+"Error: The specified file was not found.")
    except Exception as e:
        print("\n"+f"An unexpected error occurred: {e}")
        
    # Conditionally replace the original file
    if args.replace:
        replace_original_with_new(args.pdf_path, args.output_pdf_path)


if __name__ == "__main__":
    main()


# pdf_path = r'C:\Users\anter\Documents\42\harrasteet\DnD\edited\Core_Books\DnD5e_WotC_Dungeon_Masters_Guide – kopio.pdf'
# output_pdf_path = r'C:\Users\anter\Documents\42\harrasteet\DnD\edited\Core_Books\DnD5e_WotC_Dungeon_Masters_Guide – kopio_outlined.pdf'
# keywords = ["CONTENTS", 
#             "INTRODUCTION", 
#             "PART 1", 
#             "PART 2", 
#             "PART 3", 
#             "CHAPTER 1", 
#             "CHAPTER 2", 
#             "CHAPTER 3", 
#             "CHAPTER 4", 
#             "CHAPTER 5", 
#             "CHAPTER 6", 
#             "CHAPTER 7", 
#             "CHAPTER 8", 
#             "CHAPTER 9", 
#             "APPENDIX A", 
#             "APPENDIX B", 
#             "APPENDIX C", 
#             "APPENDIX D", 
#             "INDEX"]

# # Search for keywords in the PDF
# search_results = search_keywords_in_pdf(pdf_path, keywords)

# # Add outlines to the PDF based on search results
# add_outline_to_pdf(pdf_path, search_results, output_pdf_path)

# print("Modified PDF saved to:", output_pdf_path)

