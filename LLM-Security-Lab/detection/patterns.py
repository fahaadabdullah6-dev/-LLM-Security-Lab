# =============================================================================
# detection/patterns.py — Attack Pattern Library
# =============================================================================
# All known attack patterns stored here.
# The detector imports these to scan prompts and responses.
# =============================================================================

import re

# ── PROMPT INJECTION PATTERNS ─────────────────────────────────────────────────
# These phrases are classic injection attempts
INJECTION_PATTERNS = [
    r"ignore (previous|all|prior) instructions",
    r"disregard (your|the|all) (instructions|rules|guidelines)",
    r"forget (everything|what|your) (you were|you've been|above)",
    r"you are now (a|an|DAN|evil|unrestricted)",
    r"act as (a|an|if) (you have no|unrestricted|evil)",
    r"new (instructions|task|objective|goal):",
    r"system prompt:",
    r"override (safety|guidelines|rules|filters)",
    r"pretend (you are|to be|there are no) (rules|restrictions|guidelines)",
    r"from now on (you|ignore|forget)",
    r"do anything now",
    r"DAN mode",
    r"developer mode",
    r"jailbreak",
]

# ── JAILBREAK PATTERNS ────────────────────────────────────────────────────────
JAILBREAK_PATTERNS = [
    r"roleplay as",
    r"in this fictional (world|story|scenario)",
    r"hypothetically speaking",
    r"for a (story|novel|movie|book|game)",
    r"imagine you (have no|are without|lack) restrictions",
    r"in (an alternate|a parallel|a fictional) (universe|world|reality)",
    r"your (true|real|inner) self",
    r"without (any|your) (filters|restrictions|guidelines|safety)",
    r"base model",
    r"raw model",
    r"you (must|should|will) comply",
    r"no (ethical|moral) (constraints|guidelines|boundaries)",
]

# ── PRIVACY EXTRACTION PATTERNS ──────────────────────────────────────────────
PRIVACY_PATTERNS = [
    r"(tell me|reveal|show|give me|what is) (your|the|a) (password|secret|private key)",
    r"(repeat|reproduce|recite|tell me) (what|the|your) (training data|dataset)",
    r"(what|which) (email|phone|address|SSN|credit card) (did|do|was|were)",
    r"(extract|retrieve|get) (personal|private|sensitive|confidential) (data|information)",
    r"memorized (data|information|text|content)",
    r"training (data|examples|samples)",
    r"(user|customer|patient) (data|records|information)",
]

# ── PII PATTERNS (in responses) ───────────────────────────────────────────────
# Check if model response accidentally contains PII
PII_PATTERNS = {
    "email":        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "phone_uk":     r"\b(\+44|0)[0-9]{10,11}\b",
    "phone_us":     r"\b(\+1)?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b",
    "ssn":          r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card":  r"\b(?:\d{4}[\s-]?){3}\d{4}\b",
    "ip_address":   r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "password":     r"(password|passwd|pwd)\s*[:=]\s*\S+",
    "api_key":      r"(api[_-]?key|token|secret)\s*[:=]\s*[A-Za-z0-9_\-]{20,}",
}


def check_injection(text):
    """Check if text contains prompt injection patterns. Returns list of matches."""
    text_lower = text.lower()
    matches = []
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            matches.append(pattern)
    return matches


def check_jailbreak(text):
    """Check if text contains jailbreak patterns. Returns list of matches."""
    text_lower = text.lower()
    matches = []
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, text_lower):
            matches.append(pattern)
    return matches


def check_privacy_extraction(text):
    """Check if text is trying to extract private data."""
    text_lower = text.lower()
    matches = []
    for pattern in PRIVACY_PATTERNS:
        if re.search(pattern, text_lower):
            matches.append(pattern)
    return matches


def check_pii_in_response(text):
    """Check if model response contains leaked PII."""
    found = {}
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found[pii_type] = matches
    return found
