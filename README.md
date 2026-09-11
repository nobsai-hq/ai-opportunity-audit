# ai-opportunity-audit

The tooling behind my **$497 AI Opportunity Audit** for local businesses: point it at a company's website and get a scored, priced automation roadmap — the same deliverable I sell, generated in minutes instead of days.

## Quickstart

```bash
pip install -r requirements.txt
python audit.py --url https://example-bakery.com --out report.md
```

No API key needed: heuristic analysis runs offline. Set `OPENAI_API_KEY` for the LLM deep-dive section (industry-specific plays, ROI narrative).

## What it checks

| Signal | Opportunity it unlocks |
|---|---|
| No online booking / quote form | AI booking agent, missed-call text-back |
| Phone number but no after-hours handling | 24/7 AI receptionist |
| No chat widget | Website chat agent trained on their services |
| Reviews unanswered / no review funnel | Automated review request + response drafting |
| No FAQ / thin service pages | RAG Q&A agent to cut repetitive calls |
| Contact form only, no CRM mention | Lead capture → CRM + instant follow-up |

Each finding is scored 1–5 on **impact** and **effort**, then priced into a phased roadmap (quick wins → systems → scale).

## Layout

```
audit.py      # CLI: fetch -> analyze -> report
analyzer.py   # heuristic detectors (offline, deterministic)
llm.py        # optional LLM deep-dive (needs OPENAI_API_KEY)
report.py     # markdown report builder with scored roadmap
```

## Sample output

`sample-report.md` shows a real run against a fictional bakery — what a client receives.

## Why this exists

Audits are how I open client relationships: fixed price, credited toward the build, delivered fast. This repo is the engine. If you're a business owner reading this, the audit is $497 and the credit makes it free if we build together — bobby@nobsai.com.
