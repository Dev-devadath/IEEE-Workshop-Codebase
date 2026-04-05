import os
import tempfile

import fitz  # PyMuPDF
import requests


def pdf_extract(url: str) -> str:
    """
    Downloads and extracts text from a given PDF URL or local file path.

    Args:
        url (str): The URL or local path of the PDF document.

    Returns:
        str: Extracted text from the PDF.
    """
    print(f"[Tool: pdf_extract] Fetching PDF from: '{url}'...")
    try:
        if os.path.exists(url):
            temp_path = url
            to_delete = False
        else:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(response.content)
                temp_path = temp_pdf.name
            to_delete = True

        text_content = []
        with fitz.open(temp_path) as doc:
            for page in doc:
                text_content.append(page.get_text())

        if to_delete:
            os.remove(temp_path)
        return "\n".join(text_content)[:15000]
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"
