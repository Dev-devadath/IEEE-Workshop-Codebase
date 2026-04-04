import requests
import fitz  # PyMuPDF
import tempfile
import os

def pdf_extract(url: str) -> str:
    """
    Downloads and extracts text from a given PDF URL or local file path.
    
    Args:
        url (str): The URL or local path of the PDF document.
        
    Returns:
        str: Extracted text from the PDF.
    """
    print(f"Ÿ“ [Tool: pdf_extract] Fetching PDF from: '{url}'...")
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
        return "\n".join(text_content)[:15000] # Limiting to 15000 chars to avoid overwhelming models
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

from google.adk.agents.llm_agent import Agent

pdf_parser_agent = Agent(
    model=os.environ.get("MODEL", "gemini-2.5-flash-lite"),
    name="pdf_parser_agent",
    instruction="""You are an academic PDF parsing assistant. Use the 'pdf_extract' tool to extract the entire text from a provided PDF URL or local file path.
Once extracted, synthesize a structured summary.
You MUST process the result and return a strict JSON object mapping the critical components of the document.
Expected JSON format:
{
  "tldr": "A high-level 1-sentence abstract of the paper",
  "methodology": "Detailed overview of the architecture, data, or experiments used",
  "key_takeaways": [
    "Important stat or finding 1",
    "Important stat or finding 2"
  ]
}

Ensure the output is ONLY valid JSON, with no markdown code blocks (like ```json) or conversational text.""",
    output_key="parsed_pdf_summary",
    tools=[pdf_extract],
)
