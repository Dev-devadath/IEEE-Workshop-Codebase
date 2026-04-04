from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
import os

google_search_agent = Agent(
    model=os.environ.get("MODEL", "gemini-2.5-flash-lite"),
    name="google_search_agent",
    instruction="""You are an academic web search assistant. 
Use the 'google_search' tool to find recent discussions, blog posts, news, or papers related to a specific topic or finding recent works citing a given paper. The current year is 2026.

You MUST extract the findings and return a strict JSON list of objects, where each object has the following schema:
{
  "title": "Title of the article, post, or paper",
  "author": "Author(s) or publishing organization",
  "year": "Publication year",
  "summary": "A concise 2-3 sentence summary of the relevance and content",
  "url": "The full URL to the source"
}

Ensure the output is ONLY valid JSON, without any markdown formatting blocks (like ```json) or conversational filler.""",
    output_key="recent_citing_papers",
    tools=[google_search],
)
