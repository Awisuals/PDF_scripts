
# PDF and TXT Processing Scripts

This collection of scripts provides various utilities for processing PDF and TXT files, including creating outlines, extracting text, finding page sizes, organizing content, and more.

## Scripts Description

### PDF_create_outline_accurate.py
- **Description:** Creates a detailed outline in a PDF based on specific keywords.
- **Usage:** Requires specifying the PDF path and keywords for which the outline will be created.

### PDF_create_outline_rough.py
- **Description:** Designed for a rougher, quicker outline creation based on keywords.
- **Usage:** Input includes the PDF path and the keywords list.

### PDF_extract_text_careful-formatting.py
- **Description:** Extracts text from a PDF with careful attention to maintaining the original formatting.
- **Usage:** Requires the path to the PDF file from which text is to be extracted.

### PDF_extract_txt.py
- **Description:** Extracts text content from a PDF file, focusing on text content without prioritizing formatting.
- **Usage:** Specify the PDF file path to extract the text.

### PDF_find_smallest_page.py
- **Description:** Finds and reports the smallest page by dimension in a PDF.
- **Usage:** Input the PDF file path to examine.

### PDF_prefix-and-replace-whitespace.py
- **Description:** Modifies PDF file names by adding a prefix and replacing whitespace with underscores.
- **Usage:** Directory path and prefix need to be specified.

### PDF_scaler_mm.py
- **Description:** Rescales PDF pages to specified dimensions in millimeters.
- **Usage:** Include the PDF path, target width, and height in millimeters.

### TXT_organize.py
- **Description:** Organizes lines in a TXT file based on numeric values found after a semicolon.
- **Usage:** Requires paths for the input TXT file and the final output file.

## General Usage
Run the scripts with Python, providing the necessary arguments as detailed in their respective usage sections. Review each script's specific documentation for additional requirements or configurations.
