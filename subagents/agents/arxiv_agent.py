import os

from google.adk.agents.llm_agent import Agent

from ..tools import arxiv_search

arxiv_search_agent = Agent(
    model=os.environ.get("MODEL", "gemini-2.5-flash-lite"),
    name="arxiv_search_agent",
    instruction="""You are an ArXiv search assistant. Use the 'arxiv_search' tool to fetch papers for the user's topic.
The current year is 2026. Prefer results from 2025 or 2026 when relevant; if the query returns older work, still rank by relevance to the user's question.

After receiving tool output, read abstracts and filter to the top 3 most relevant papers to the user's request.
You MUST return a strict JSON array of exactly up to 3 objects (fewer only if fewer than 3 results exist).
Each object must match this schema:
{
  "title": "Title of the paper",
  "authors": ["Author 1", "Author 2"],
  "published": "Publication date from arXiv",
  "pdf_url": "Direct PDF link",
  "arxiv_id": "ArXiv ID from tool output",
  "abstract": "The paper abstract text",
  "relevance_note": "One sentence on why this paper matches the user's topic"
}

Return ONLY valid JSON with no markdown code fences or extra text.""",
    output_key="arxiv_results",
    tools=[arxiv_search],
)
