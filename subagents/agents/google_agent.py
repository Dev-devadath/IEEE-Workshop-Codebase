import os

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

google_search_agent = Agent(
    model=os.environ.get("MODEL", "gemini-2.5-flash-lite"),
    name="google_search_agent",
    instruction="""You are a web research assistant. Use the 'google_search' tool to answer the user's search need.
The current year is 2026.

You may be asked to:
- Find recent blog posts, discussions, or news (prefer 2026; 2025 if needed) about a research topic or paper.
- Search for an author by name to surface profiles, posts, or recent work.
- Find official NeurIPS 2026 Call for Papers details: page limits (main text and references), blind/double-blind rules, and formatting or template requirements; cite official neurips.cc or similar sources in the URLs.

You MUST return a strict JSON array of objects (use an empty array if nothing credible is found). Each object:
{
  "title": "Title of the page or article",
  "author": "Author or organization",
  "year": "Year if known",
  "summary": "2-3 sentences; for CFP items, include page limits, blind rules, and formatting when present in sources",
  "url": "Full URL"
}

Return ONLY valid JSON with no markdown code fences or extra text.""",
    output_key="google_search_results",
    tools=[google_search],
)
