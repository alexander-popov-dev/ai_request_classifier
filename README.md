# AI Request Classifier

A Python service that classifies internal team requests using the Gemini API.
For each request it extracts category, priority, target department, short summary,
action items, clarification flags, language, and duplicate hints.

## Features

- Classifies requests into 6 categories: automation, integration, analytics, bug/support, consultation, out-of-scope
- Assigns priority: `high` / `medium` / `low`
- Identifies target department and requested actions
- Flags vague requests that need clarification
- Detects self-reported duplicates
- Outputs structured JSON + an aggregated Markdown report
- Retry logic with exponential backoff on API failures
- Rate-limit-safe delay between requests (configurable)

## Architecture

```
src/
├── core/
│   ├── base/
│   │   ├── ai/          # Abstract AI client and parser
│   │   └── io/          # Abstract reader and writer
│   ├── schemas.py       # Pydantic domain models
│   ├── enums.py         # CategoryType, PriorityType
│   ├── exceptions.py    # Exception hierarchy
│   └── decorators.py    # Retry decorator
├── ai/gemini/           # Gemini API client and response parser
├── readers/             # CSV reader
├── writers/             # JSON and Markdown writers
├── service.py           # Classification orchestration
├── config.py            # Settings (pydantic-settings)
└── main.py              # Composition root
```

All dependencies are injected — the service is decoupled from the AI provider,
the input format, and the output format.

## Tech Stack

- Python 3.14
- [google-genai](https://pypi.org/project/google-genai/) 2.x (Gemini API SDK)
- [Pydantic](https://docs.pydantic.dev/) v2
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- Poetry

## Setup

**Prerequisites:** Python 3.14, Poetry

```bash
git clone <repo-url>
cd ai-request-classifier
poetry install
```

Copy the environment template and set your API key:

```bash
cp .env.example .env
```

## Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | yes | — | Gemini API key |
| `GEMINI_MODEL` | no | `gemini-3.1-flash-lite` | Model name |
| `INPUT_FILE` | no | `input/input_requests.csv` | Path to input CSV |
| `OUTPUT_FILE` | no | `output/output.json` | Path to JSON output |
| `REPORT_FILE` | no | `output/report.md` | Path to Markdown report |
| `REQUEST_DELAY` | no | `4.0` | Delay (seconds) between API calls |

## Running

From the project root:

```bash
python -m src.main
```

Results are written to `output/output.json` and `output/report.md`.

## Docker

```bash
make up      # build and run
make logs    # follow logs
make down    # stop and remove
```

## Input Format

CSV file with columns: `id`, `channel`, `timestamp`, `raw_text`.

```csv
id,channel,timestamp,raw_text
REQ-001,Slack,2026-06-08 09:14,"Привіт! Можна якось автоматизувати..."
```

## Output

**`output.json`** — array of classified requests:

```json
[
  {
    "source": { "id": "REQ-001", "channel": "Slack", "timestamp": "...", "raw_text": "..." },
    "category": "автоматизація",
    "priority": "medium",
    "target_department": "аналітика",
    "short_summary": "...",
    "requested_actions": ["...", "..."],
    "needs_clarification": false,
    "language": "uk",
    "is_duplicate_hint": null
  }
]
```

**`report.md`** — aggregated report: counts by category, priority, and department;
a list of requests needing clarification; and parse errors if any.

## Limitations

- **LLM non-determinism** — results may vary slightly between runs
- **Rate limits** — Gemini free tier allows 15 RPM. The default `REQUEST_DELAY=4.0` keeps within the limit; lower it for paid tiers
- **Duplicate detection** — `is_duplicate_hint` only triggers when the author explicitly references a prior request; the service processes one request at a time and cannot compare across requests
- **No ground truth** — classification quality is not automatically validated

## What's Next

- Async execution with concurrent API calls
- `response_schema` in the Gemini config for strict JSON validation
- Vector similarity for automatic cross-request duplicate detection
- Iterator/generator for streaming large input files
