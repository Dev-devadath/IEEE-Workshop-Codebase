# ADK Research Agent

A research orchestration app built with Google ADK. A single `root_agent` coordinates three specialist sub-agents: ArXiv search, PDF parsing, and Google Search (built-in ADK tool).

## Layout

```
subagents/
├── __init__.py          # exports root_agent
├── agent.py             # root orchestrator
├── tools/               # plain tool functions only
│   ├── arxiv_search.py  # arxiv_search()
│   └── pdf_parser.py    # pdf_extract()
└── agents/              # LLM sub-agents wired to tools
    ├── arxiv_agent.py
    ├── pdf_agent.py
    └── google_agent.py
```

## Workflow

1. **ArXiv** — Search for highly relevant papers (prefer 2025/2026), filter by abstract, return up to three with PDF links and ArXiv IDs.
2. **PDF** — Parse each selected PDF and extract methodology and key takeaways.
3. **Google Search** — Find recent blog posts, discussions, or news; search author names as needed.
4. **NeurIPS 2026** — Look up Call for Papers details (page limits, blind submission, formatting) via web search.

The root agent then synthesizes a report and suggests what to think about and what to write.

## How to Run

### Terminal

```bash
adk run subagents
```

### Web UI

```bash
adk web subagents
```

Set `MODEL`, `GOOGLE_API_KEY`, and (for Vertex if used) related env vars in `.env` as required by your ADK setup.

## Dependencies

See [requirements.txt](requirements.txt): `google-adk`, `requests`, `pymupdf`, `arxiv`.
