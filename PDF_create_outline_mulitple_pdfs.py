import os
from PDF_create_outline_accurate import main as add_bookmarks_to_pdf
import argparse

def find_matching_files(directory):
    files = os.listdir(directory)
    matched_files = {}
    for file in files:
        name, extension = os.path.splitext(file)
        if name not in matched_files:
            matched_files[name] = {}
        matched_files[name][extension] = file

    return [(os.path.join(directory, v['.txt']), os.path.join(directory, v['.pdf']))
            for k, v in matched_files.items() if '.txt' in v and '.pdf' in v]

def create_outlines_for_pdfs(directory, replace, adjust_page):
    matches = find_matching_files(directory)
    
    print("Files found:" + "\n")
    for txt_path, pdf_path in matches:
        print(txt_path)
    
    for txt_path, pdf_path in matches:
        output_pdf_path = pdf_path.replace('.pdf', '_outlined.pdf')
        add_bookmarks_to_pdf(text_file_path=txt_path, pdf_file_path=pdf_path, output_pdf_path=output_pdf_path, replace=replace, adjust_page=adjust_page)
        print(f'Outline added to {output_pdf_path} based on {txt_path}')

def main(dir, replace, adjust_page):
    create_outlines_for_pdfs(dir, replace, adjust_page)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Automatically add outlines to PDFs based on matching TXT files.')
    
    parser.add_argument(
        'directory', 
        help='Directory containing the PDF and TXT files')
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
            [r"C:\Users\anter\Documents\42\Harrasteet\dnd – kopio"
              ,r'-r']) #,'--replace' # Use this as fourth argument as needed in debugging
    else:
        # Parse arguments from the command line
        args = parser.parse_args()
    
    main(args.directory, 
         args.replace, 
         args.adjust_page)

