import requests
from google.adk.agents.llm_agent import Agent
import os
def fetch_citations(paper_id: str) -> dict:
    """Fetch citations (forward citations) using Semantic Scholar Graph API"""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields=title,authors,year"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def fetch_references(paper_id: str) -> dict:
    """Fetch references (backward citations) using Semantic Scholar Graph API"""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?fields=title,authors,year"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

citation_graph_agent = Agent(
    model=os.environ.get("MODEL", "gemini-2.5-flash-lite"),
    name="citation_graph_agent",
    instruction="""You are a citation analysis assistant. Use the 'fetch_citations' and 'fetch_references' tools to retrieve forward citations and backward references for a given paper. For ArXiv papers, use the format 'ARXIV:<arxiv_id>' as the paper_id.

You MUST process the results and return a strict JSON object mapping the citation history.
Expected JSON format:
{
  "target_paper_id": "The ID of the paper being analyzed",
  "forward_citations": [
    {
      "title": "Title of the citing paper",
      "authors": ["Author 1", "Author 2"],
      "year": "Publication year"
    }
  ],
  "backward_references": [
    {
      "title": "Title of the referenced paper",
      "authors": ["Author 1", "Author 2"],
      "year": "Publication year"
    }
  ],
  "summary": "A brief 2-3 sentence summary of the prominent works cited by and citing this paper."
}

Ensure the output is ONLY valid JSON, with no markdown formatting blocks (like ```json) or conversational text.""",
    output_key="citation_graph",
    tools=[fetch_citations, fetch_references],
)
