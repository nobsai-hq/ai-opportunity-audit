"""Optional LLM deep-dive: industry-specific plays and ROI narrative.

Skipped entirely without OPENAI_API_KEY — the heuristic audit stands alone.
"""
from __future__ import annotations

import os

from analyzer import Finding


def deep_dive(url: str, findings: list[Finding]) -> str:
    if not os.environ.get("OPENAI_API_KEY"):
        return ""
    from openai import OpenAI  # type: ignore

    client = OpenAI()
    summary = "\n".join(f"- {f.title}: {f.opportunity}" for f in findings)
    resp = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a pragmatic AI consultant writing for a non-technical "
                    "small business owner. Be concrete, avoid jargon, quantify ROI "
                    "where possible. Keep it under 300 words."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Website: {url}\nAudit findings:\n{summary}\n\n"
                    "Write: 1) the one automation that pays for itself fastest and why, "
                    "2) what 'good' looks like 90 days after implementation."
                ),
            },
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""
