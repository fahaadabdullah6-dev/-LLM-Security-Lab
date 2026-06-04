# =============================================================================
# detection/detector.py — Core Detection Engine
# =============================================================================
# Analyses every prompt sent to the LLM and every response received.
# Flags attacks, scores severity, and logs alerts.
# =============================================================================

import json
import time
import os
import sys
from datetime import datetime
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from detection.patterns import (
    check_injection, check_jailbreak,
    check_privacy_extraction, check_pii_in_response
)

# ── SHARED STATE (read by dashboard) ─────────────────────────────────────────
alert_queue  = deque(maxlen=500)
attack_stats = {
    "total_prompts":    0,
    "total_attacks":    0,
    "injection":        0,
    "jailbreak":        0,
    "privacy":          0,
    "pii_leaked":       0,
    "start_time":       time.time()
}

SEVERITY_ICONS = {
    config.SEVERITY_LOW:      "🔵",
    config.SEVERITY_MEDIUM:   "🟡",
    config.SEVERITY_HIGH:     "🔴",
    config.SEVERITY_CRITICAL: "💀",
}


def create_alert(attack_type, severity, prompt, response, details):
    """Creates a standardised alert dictionary."""
    return {
        "attack_type": attack_type,
        "severity":    severity,
        "prompt":      prompt[:200],        # Truncate for log
        "response":    response[:200],
        "details":     details,
        "timestamp":   time.time()
    }


def log_alert(alert):
    """Logs alert to file and console, adds to shared queue."""
    alert_queue.appendleft(alert)
    attack_stats["total_attacks"] += 1

    # Update per-type counters
    atype = alert["attack_type"].lower()
    if "injection"  in atype: attack_stats["injection"]   += 1
    if "jailbreak"  in atype: attack_stats["jailbreak"]   += 1
    if "privacy"    in atype: attack_stats["privacy"]     += 1
    if "pii"        in atype: attack_stats["pii_leaked"]  += 1

    # ── Console output ────────────────────────────────────────────────────
    ts   = datetime.fromtimestamp(alert["timestamp"]).strftime("%H:%M:%S")
    icon = SEVERITY_ICONS.get(alert["severity"], "⚪")
    print(f"\n{'='*65}")
    print(f"  🚨 ATTACK DETECTED [{ts}]")
    print(f"  {icon} [{alert['severity']}] {alert['attack_type']}")
    print(f"  Prompt  : {alert['prompt'][:80]}...")
    print(f"  Details : {alert['details']}")
    print(f"{'='*65}")

    # ── File logging ──────────────────────────────────────────────────────
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
    )
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "alerts.log")

    with open(log_file, "a", encoding="utf-8") as f:
        ts_full = datetime.fromtimestamp(alert["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ts_full}] {icon} [{alert['severity']}] "
                f"[{alert['attack_type']}] {alert['details']}\n")
        f.write("  JSON: " + json.dumps(alert) + "\n")


def analyse(prompt, response):
    """
    Main analysis function.
    Call this after every LLM interaction with the prompt and response.
    Returns list of triggered alerts.
    """
    attack_stats["total_prompts"] += 1
    alerts = []

    # ── 1. Prompt Injection Check ─────────────────────────────────────────
    injection_hits = check_injection(prompt)
    if injection_hits:
        severity = (config.SEVERITY_CRITICAL
                    if len(injection_hits) >= 3
                    else config.SEVERITY_HIGH)
        alert = create_alert(
            attack_type = "PROMPT_INJECTION",
            severity    = severity,
            prompt      = prompt,
            response    = response,
            details     = f"Injection patterns found: {len(injection_hits)} matches"
        )
        log_alert(alert)
        alerts.append(alert)

    # ── 2. Jailbreak Check ────────────────────────────────────────────────
    jailbreak_hits = check_jailbreak(prompt)
    if jailbreak_hits:
        severity = (config.SEVERITY_HIGH
                    if len(jailbreak_hits) >= 2
                    else config.SEVERITY_MEDIUM)
        alert = create_alert(
            attack_type = "JAILBREAK_ATTEMPT",
            severity    = severity,
            prompt      = prompt,
            response    = response,
            details     = f"Jailbreak patterns found: {len(jailbreak_hits)} matches"
        )
        log_alert(alert)
        alerts.append(alert)

    # ── 3. Privacy Extraction Check ───────────────────────────────────────
    privacy_hits = check_privacy_extraction(prompt)
    if privacy_hits:
        alert = create_alert(
            attack_type = "PRIVACY_EXTRACTION",
            severity    = config.SEVERITY_HIGH,
            prompt      = prompt,
            response    = response,
            details     = f"Privacy extraction attempt: {len(privacy_hits)} patterns"
        )
        log_alert(alert)
        alerts.append(alert)

    # ── 4. PII in Response Check ──────────────────────────────────────────
    pii_found = check_pii_in_response(response)
    if pii_found:
        pii_types = list(pii_found.keys())
        alert = create_alert(
            attack_type = "PII_LEAKED_IN_RESPONSE",
            severity    = config.SEVERITY_CRITICAL,
            prompt      = prompt,
            response    = response,
            details     = f"PII types detected in response: {pii_types}"
        )
        log_alert(alert)
        alerts.append(alert)

    return alerts
