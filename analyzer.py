"""Heuristic detectors: offline, deterministic signals from a website fetch.

Each detector returns a Finding with impact/effort scores. Deterministic
matters here: the audit must be explainable to a non-technical owner, and
every claim must trace to something observed on their site.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Finding:
    id: str
    title: str
    observed: str
    opportunity: str
    impact: int  # 1-5
    effort: int  # 1-5 (1 = easy)
    play: str = ""  # which Get247.ai-style play this maps to


def _has(html: str, *patterns: str) -> bool:
    return any(re.search(p, html, re.I) for p in patterns)


def analyze(url: str, html: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    low = html.lower()

    # 1. Booking / quoting
    if not _has(html, r"book\s*(now|online|appointment)", r"schedule", r"get\s*(a\s*)?quote", r"calendly", r"acuity"):
        findings.append(Finding(
            id="booking",
            title="No online booking or instant quote path",
            observed="No booking widget, scheduler, or quote flow detected on the site.",
            opportunity="Visitors who want to book after hours bounce. An AI booking agent captures them 24/7.",
            impact=5, effort=2, play="AI receptionist + booking agent",
        ))

    # 2. Chat
    if not _has(html, r"intercom|drift|tidio|crisp|hubspot.*chat|chat-widget|tawk\.to"):
        findings.append(Finding(
            id="chat",
            title="No website chat",
            observed="No chat widget detected.",
            opportunity="A chat agent trained on their services answers FAQs instantly and captures the lead.",
            impact=4, effort=2, play="Website chat agent",
        ))

    # 3. Phone without after-hours coverage
    phones = re.findall(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    if phones and not _has(html, r"24\s?/\s?7|after.?hours|ai\s*receptionist|virtual\s*receptionist"):
        findings.append(Finding(
            id="after-hours",
            title="Phone listed, no after-hours coverage",
            observed=f"Phone number(s) found ({phones[0]}), no mention of 24/7 or after-hours handling.",
            opportunity="Missed-call text-back + AI receptionist answers every call, even at 2 AM.",
            impact=5, effort=2, play="Missed-call text-back + AI receptionist",
        ))

    # 4. Reviews
    if not _has(html, r"google.*review|leave\s*(us\s*)?(a\s*)?review|review\s*us"):
        findings.append(Finding(
            id="reviews",
            title="No review funnel",
            observed="No review request links or Google review prompts detected.",
            opportunity="Automated post-service review requests + AI-drafted responses grow 5-star velocity.",
            impact=4, effort=1, play="Review automation",
        ))

    # 5. FAQ / thin content
    faq_hits = len(re.findall(r"faq|frequently asked", low))
    word_count = len(text.split())
    if faq_hits == 0 or word_count < 400:
        findings.append(Finding(
            id="faq",
            title="Thin self-service content",
            observed=f"No FAQ section found; ~{word_count} words of indexable text.",
            opportunity="A Q&A agent trained on their services deflects repetitive calls and qualifies buyers.",
            impact=3, effort=2, play="RAG Q&A agent",
        ))

    # 6. Lead follow-up
    if _has(html, r"<form") and not _has(html, r"hubspot|gohighlevel|salesforce|pipedrive|zoho|activecampaign|mailchimp"):
        findings.append(Finding(
            id="crm",
            title="Contact form with no visible CRM",
            observed="A contact form exists but no marketing automation / CRM markers detected.",
            opportunity="Form → CRM + instant SMS/email follow-up. Speed-to-lead is the whole game.",
            impact=5, effort=2, play="Lead capture + instant follow-up automation",
        ))

    # 7. Social proof
    if not _has(html, r"testimonial|success\s*stor|case\s*stud|our\s*clients"):
        findings.append(Finding(
            id="social-proof",
            title="Little visible social proof",
            observed="No testimonials, case studies, or client logos detected.",
            opportunity="Systematic testimonial collection feeds the site and the review funnel.",
            impact=3, effort=1, play="Social proof pipeline",
        ))

    return sorted(findings, key=lambda f: (f.impact / f.effort), reverse=True)
