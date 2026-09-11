"""CLI: fetch a business website -> heuristic analysis -> markdown audit report."""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request

from analyzer import analyze
from llm import deep_dive
from report import build_report


def fetch(url: str, timeout: int = 20) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    req = urllib.request.Request(url, headers={"User-Agent": "ai-opportunity-audit/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
    return raw


def visible_text(html: str) -> str:
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an AI Opportunity Audit for a business website.")
    parser.add_argument("--url", required=True, help="Business website URL")
    parser.add_argument("--out", default="audit-report.md", help="Output markdown file")
    parser.add_argument("--html-file", help="Analyze a saved HTML file instead of fetching")
    args = parser.parse_args()

    try:
        if args.html_file:
            with open(args.html_file, encoding="utf-8", errors="ignore") as f:
                html = f.read()
        else:
            print(f"Fetching {args.url} ...")
            html = fetch(args.url)
    except Exception as e:  # noqa: BLE001 — CLI: report and exit
        print(f"Fetch failed: {e}", file=sys.stderr)
        sys.exit(1)

    findings = analyze(args.url, html, visible_text(html))
    print(f"Found {len(findings)} opportunities.")
    llm_section = deep_dive(args.url, findings)
    report = build_report(args.url, findings, llm_section)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report written to {args.out}")


if __name__ == "__main__":
    main()
