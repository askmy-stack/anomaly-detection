# Security Policy

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

- Preferred: use GitHub's private vulnerability reporting for this repository
  (Security tab → **Report a vulnerability**).
- Alternative: email **kamineniabhinaysai@gmail.com** with a description of
  the issue, steps to reproduce, and its potential impact.

We aim to acknowledge reports within 7 days and to keep you updated as we
investigate and fix confirmed issues.

## Supported Versions

Py-Outlier does not yet have tagged releases; security fixes are applied to
the `main` branch. Run the latest `main` to get fixes as soon as they land.

## API Authentication

The FastAPI service (`src/anomaly_detection/api/`) supports optional
`X-API-Key` authentication via `ApiKeyMiddleware`. Set `ANOMALY_API_KEY` to
require a matching key on every route except `/health`, `/docs`, `/redoc`,
and `/openapi.json`. **Leaving `ANOMALY_API_KEY` unset runs the service in
open mode with no auth** — fine for local/dev use, but set it before
exposing the service on a network. CORS is also wide open
(`allow_origins=["*"]`) by default.

`/detect` and `/detect/batch` cap accepted rows via `MAX_DETECT_ROWS`
(default 100,000) to bound memory/CPU usage from a single request.

## LLM Usage and PII Handling

The optional LLM explainer (`llm.enabled` in config, disabled by default)
sends anomaly context — sample indices, scores, predictions, and
feature names/values — to **Anthropic** via `ANTHROPIC_API_KEY` when enabled.

Before that data is sent, and again on the model's response,
`src/anomaly_detection/llm/redaction.py` applies regex-based redaction for:

- Email addresses → `[REDACTED_EMAIL]`
- US-format phone numbers → `[REDACTED_PHONE]`
- SSN-shaped values → `[REDACTED_SSN]`

**Limitations:** this redaction is pattern-based only. It does not catch
names, addresses, credit card numbers, or other free-text PII, and it is
not applied to `/detect` or `/detect/batch` inputs (which are processed
locally and never sent to an LLM by those endpoints themselves). Do not
enable the LLM explainer on datasets containing PII types beyond emails,
phone numbers, and SSNs unless you've reviewed and extended the redaction
patterns for your data.

## Data Handled

The service processes user-supplied tabular numeric data (JSON or CSV
upload) and, if the `[vision]` extra is installed, images/video for
classification. There is no persistent user database; data is processed
in-memory unless you configure output paths yourself.
