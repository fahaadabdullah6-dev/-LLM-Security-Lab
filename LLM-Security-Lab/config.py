# =============================================================================
# config.py — Central Configuration
# =============================================================================

# ── FREE MODEL SETTINGS (HuggingFace — no API key needed) ────────────────────
# We use small, fast models that run locally on CPU
# Options:
#   "gpt2"                    — Fast, lightweight (best for testing)
#   "google/flan-t5-small"    — Better instruction following
#   "facebook/opt-125m"       — Facebook's open model

MODEL_NAME       = "gpt2"           # Change this to try different models
MAX_NEW_TOKENS   = 150              # Max tokens in model response
TEMPERATURE      = 0.7              # Creativity level (0=robotic, 1=creative)

# ── DETECTION SETTINGS ───────────────────────────────────────────────────────
# Severity levels
SEVERITY_LOW      = "LOW"
SEVERITY_MEDIUM   = "MEDIUM"
SEVERITY_HIGH     = "HIGH"
SEVERITY_CRITICAL = "CRITICAL"

# ── LOGGING ──────────────────────────────────────────────────────────────────
LOG_FILE_PATH = "logs/alerts.log"

# ── DASHBOARD ────────────────────────────────────────────────────────────────
DASHBOARD_REFRESH = 1.0
MAX_ALERTS_SHOWN  = 20
