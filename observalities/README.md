# DeepAgents + LangSmith Observability

This folder is the **only part added/updated for observability**. Existing
application files are not modified.

## Architecture

```text
AI Startup Idea Validator
          |
          v
      DeepAgents
          |
          v
  Existing Gemini API Key Router
          |
          v
     Gemini LLM
          |
          v
      LangSmith
          |
  +-------+----------------+
  |                        |
  v                        v
TIER 1                  TIER 2
Model Metrics           System & Quality
- Tokens                - Quality
- Latency               - Cost
- Temperature           - Errors
- Model Usage           - Tracing
                        - Performance
                        - Safety
```

### API routing

`router.py` reuses the project's existing Gemini API-key router in
`app.config.llm`. That router already switches across `GEMINI_API_KEY_1` through
`GEMINI_API_KEY_5` on quota/rate-limit failures. The observability folder does
not modify that existing implementation. This does **not** increase Google's
quota; it prevents one key from being a single point of failure.

### LangSmith

LangSmith tracing is enabled through environment variables. The LangSmith key
is never hard-coded or written into reports.

Set these in the existing `.env` file (do not commit it):

```env
GEMINI_API_KEY_1=...
GEMINI_API_KEY_2=...
GEMINI_API_KEY_3=...
GEMINI_API_KEY_4=...
GEMINI_API_KEY_5=...

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=AI-Startup-Idea-Validator-Observability
```

Only the first Gemini key is required. Additional keys are optional fallback
keys.

## Dependencies

The existing project requirements are not changed. Install the additional
packages required by this isolated observability layer in the project's
virtual environment:

```bash
pip install deepagents langchain-google-genai langsmith
```

## Files

```text
observalities/
├── __init__.py
├── agent.py          # DeepAgent + workflow
├── tools.py          # Tier 1 and Tier 2 tools
├── router.py         # adapter to existing Gemini API-key router
├── tracing.py        # LangSmith tracing configuration
├── config.py         # observability-only configuration
├── schemas.py
├── README.md
└── data/
```

The dashboard is intentionally excluded because the frontend developer owns
that layer.
