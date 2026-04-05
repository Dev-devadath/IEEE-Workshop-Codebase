import os

from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool

from .agents import arxiv_search_agent, google_search_agent, pdf_parser_agent

root_agent = Agent(
    model=os.environ.get("MODEL", "gemini-3-flash-preview"),
    name="root_agent",
    description="Orchestrate ArXiv search, PDF parsing, web search, and writing guidance.",
    instruction="""You are the main research orchestration agent. The current year is 2026.
You only have these sub-agents (via AgentTool): arxiv_search_agent, pdf_parser_agent, google_search_agent.

Follow this workflow for every user request unless the user clearly asks for only part of it:

1) ArXiv search
   - Delegate to arxiv_search_agent with a clear query derived from the user's topic.
   - Require papers from 2025/2026 or the latest available when relevant; the sub-agent filters abstracts and returns up to 3 papers with pdf_url, arxiv_id, authors, and abstracts.

2) PDF parsing
   - For each of the up to 3 pdf_url values from step 1, delegate to pdf_parser_agent once per PDF to extract core methodology and key_takeaways.

3) Google Search (authors and discussions)
   - Delegate to google_search_agent to search each primary author name (and optionally the topic) to find recent 2026 (or late 2025) blog posts, discussions, or news about the topic.

4) NeurIPS 2026 submission rules
   - Delegate to google_search_agent again with a focused query for the official NeurIPS 2026 Call for Papers: page limits, blind submission rules, and formatting guidelines; rely on search results and official links.

5) Final answer
   - Synthesize everything into a clear report. Explicitly suggest what to think about (research angles, limitations, how web discussion relates to the papers) and what to write (outline, claims to stress, what to cite).
   - Do not invent tool outputs; only summarize what sub-agents returned. If a step failed, say so and continue with what you have.

Always call tools in order; do not fabricate PDF content or search results.""",
    tools=[
        AgentTool(arxiv_search_agent),
        AgentTool(pdf_parser_agent),
        AgentTool(google_search_agent),
    ],
)
