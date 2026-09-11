"""Markdown report builder: scored findings -> phased, priced roadmap."""
from __future__ import annotations

from analyzer import Finding

PHASE_PRICING = {
    "quick-wins": ("Phase 1 — Quick wins (weeks 1–2)", "$1,500–$3,000"),
    "systems": ("Phase 2 — Systems (weeks 3–6)", "$3,000–$8,000"),
    "scale": ("Phase 3 — Scale (month 3+)", "$1,000–$2,500/mo care plan"),
}


def _stars(n: int) -> str:
    return "★" * n + "☆" * (5 - n)


def build_report(url: str, findings: list[Finding], llm_section: str = "") -> str:
    lines = [
        "# AI Opportunity Audit",
        "",
        f"**Site:** {url}",
        f"**Findings:** {len(findings)} opportunities scored below.",
        "",
        "## Scored findings",
        "",
        "| # | Opportunity | Impact | Effort | ROI signal |",
        "|---|-------------|--------|--------|------------|",
    ]
    for i, f in enumerate(findings, 1):
        lines.append(
            f"| {i} | {f.title} | {_stars(f.impact)} | {_stars(6 - f.effort)} | {f.play} |"
        )
    lines += ["", "## What we observed", ""]
    for i, f in enumerate(findings, 1):
        lines += [
            f"### {i}. {f.title}",
            "",
            f"- **Observed:** {f.observed}",
            f"- **Opportunity:** {f.opportunity}",
            f"- **Play:** {f.play}",
            "",
        ]

    lines += ["## Recommended roadmap", ""]
    quick = [f for f in findings if f.effort <= 2 and f.impact >= 4]
    systems = [f for f in findings if f not in quick and f.effort <= 3]
    scale = [f for f in findings if f not in quick and f not in systems]
    for key, items in (("quick-wins", quick), ("systems", systems), ("scale", scale)):
        title, price = PHASE_PRICING[key]
        lines.append(f"### {title} — {price}")
        lines.append("")
        for f in items:
            lines.append(f"- {f.title} → *{f.play}*")
        if not items:
            lines.append("- _(nothing in this phase)_")
        lines.append("")

    if llm_section:
        lines += ["## Industry deep-dive (AI-assisted)", "", llm_section, ""]

    lines += [
        "---",
        "",
        "*This audit is credited in full toward your build. — Get247.ai, bobby@nobsai.com*",
    ]
    return "\n".join(lines)
