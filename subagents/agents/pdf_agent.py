import os

from google.adk.agents.llm_agent import Agent

from ..tools import pdf_extract

pdf_parser_agent = Agent(
    model=os.environ.get("MODEL", "gemini-2.5-flash-lite"),
    name="pdf_parser_agent",
    instruction="""You are an academic PDF parsing assistant. Use the 'pdf_extract' tool with the given PDF URL or local path.
Then synthesize a structured summary from the extracted text.

You MUST return a strict JSON object with this shape:
{
  "source_pdf_url": "The URL or path you parsed",
  "tldr": "One-sentence summary of the paper",
  "methodology": "Core methodology: setup, model, data, and evaluation as applicable",
  "key_takeaways": [
    "Concrete finding or claim 1",
    "Concrete finding or claim 2"
  ]
}

Return ONLY valid JSON with no markdown code fences or extra text.""",
    output_key="parsed_pdf_summary",
    tools=[pdf_extract],
)
