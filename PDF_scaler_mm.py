# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:01:15 2024

@author: anter
"""
import fitz  # PyMuPDF
import argparse
import sys
import os
import glob

def mm_to_points(mm):
    """Convert millimeters to points"""
    return mm * (72 / 25.4)


def replace_original_with_new(original_path, new_path):
    """Deletes the original file and renames
    the new file to the original's name."""
    try:
        os.remove(original_path)  # Delete the original file
        os.rename(new_path, original_path)  # Rename the new file
        print("\n"+f"Replaced '{original_path}' with the new file.")
    except Exception as e:
        print("\n"+f"Error replacing file: {e}")


def scale_pdf_content(
        source_pdf_path, target_width_mm, target_height_mm, output_pdf_path):
    # Convert target size from millimeters to points
    target_width_pt = mm_to_points(target_width_mm)
    target_height_pt = mm_to_points(target_height_mm)
    
    # Open the source PDF
    doc = fitz.open(source_pdf_path)
    new_doc = fitz.open()  # Create a new PDF to save the scaled content
    
    for page_number in range(len(doc)):
        # Create a new page in the new document with the target dimensions
        new_page = new_doc.new_page(
            width=target_width_pt, height=target_height_pt)
        
        # Scale and insert the page content into the new page
        # directly, without keeping the proportions
        new_page.show_pdf_page(
            new_page.rect, doc, page_number, clip=None, keep_proportion=False)
        
        # Print status of scaling pdf
        # Update progress status in place
        sys.stdout.write(f"\rProcessed page {page_number + 1}/{len(doc)}")
        # Ensures that the output is immediately written to the terminal
        sys.stdout.flush()

    # After the loop completes, print a newline character to
    # ensure the next console output starts on a new line
    sys.stdout.write("\n")
    
    # Save the new PDF with scaled content
    new_doc.save(output_pdf_path)
    new_doc.close()
    doc.close()
    print("\n"+"PDF scaling complete. Output saved to:", output_pdf_path)


def process_file(file_path, width, height, replace):
    # Existing logic to scale a PDF file
    output_pdf_path = file_path.replace('.pdf', '_scaled.pdf')
    
    try:
        scale_pdf_content(file_path, width, height, output_pdf_path)
        print("\n"+"PDF scaled and saved successfully.")
    except FileNotFoundError:
        print("\n"+"Error: The specified file was not found.")
    except Exception as e:
        print("\n"+f"An unexpected error occurred: {e}")
    
    # Conditionally replace the original file
    if replace:
        replace_original_with_new(file_path, output_pdf_path)
    
    

def main():
    # parser = argparse.ArgumentParser(
    #     description="Scale PDF content to a new size.")
    # parser.add_argument(
    #     "source_pdf_path", help="Path to the source PDF file")
    # parser.add_argument(
    #     "target_width_mm", type=float, help="Target width in millimeters")
    # parser.add_argument(
    #     "target_height_mm", type=float, help="Target height in millimeters")
    # parser.add_argument(
    #     "output_pdf_path", help="Path to save the output PDF file")
    # parser.add_argument(
    #     '--replace', action='store_true', help='Delete the original PDF and replace it with the new file.')

    # args = parser.parse_args()
    
    parser = argparse.ArgumentParser(description="Scale PDF content to a new size.")

    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--file", help="Path to a single PDF file to be processed.")
    group.add_argument(
        "-d", "--directory", help="Path to a directory to process all PDF files within.")
    
    parser.add_argument(
        'width', type=int, help='Target width in millimeters.')
    parser.add_argument(
        'height', type=int, help='Target height in millimeters.')
    parser.add_argument(
        '--replace', action='store_true', help='Delete the original PDF and replace it with the new file.')
    
    args = parser.parse_args()
    
    # Process based on the argument provided
    if args.file:
        # Process a single file
        process_file(args.file, args.width, args.height, args.replace)
    elif args.directory:
        # Process all PDFs in the specified directory
        for pdf_file in glob.glob(os.path.join(args.directory, '*.pdf')):
            process_file(pdf_file, args.width, args.height, args.replace)
        
    
    # # Conditionally replace the original file
    # if args.replace:
    #     replace_original_with_new(args.source_pdf_path, args.output_pdf_path)


if __name__ == "__main__":
    main()
    
    