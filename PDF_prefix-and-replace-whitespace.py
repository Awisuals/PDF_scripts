# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:52:38 2024

@author: anter
"""
import os
import argparse

def rename_pdfs_in_folder(folder_path, prefix):
    """
    Renames all PDF files in the specified folder by adding a prefix and replacing whitespaces with underscores.
    
    Args:
    - folder_path: Path to the folder containing PDF files.
    - prefix: Prefix to add to the file names.
    """
    try:
        # List all files in the given folder
        files = os.listdir(folder_path)
        
        for file in files:
            # Check if the file is a PDF
            if file.lower().endswith('.pdf'):
                # Construct the new file name
                new_file_name = prefix + file.replace(" ", "_")
                
                # Construct the full old and new file paths
                old_file_path = os.path.join(folder_path, file)
                new_file_path = os.path.join(folder_path, new_file_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed '{file}' to '{new_file_name}'")
                
        print("All PDF files have been renamed.")
    except Exception as e:
        print(f"Error: {e}")

def main(folder_path, prefix):
    
    rename_pdfs_in_folder(folder_path, prefix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename all PDFs in a folder with a specified prefix and replace spaces with underscores.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing the PDF files.")
    parser.add_argument("prefix", type=str, help="Prefix to add to the PDF files. Should be of the form ''myPrefix_''.")
    
    args = parser.parse_args()
    
    main(args.folder_path, args.prefix)
