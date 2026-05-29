"""Judge LLM that maps a raw model response to a single lowercase language token.

We use a cheap small model. The judge never sees which model produced the response,
so it can't bias toward expected defaults.

Returned tokens are normalized to a small canonical set so the report aggregates cleanly
(e.g. "js" → "javascript", "golang" → "go", "py" → "python").
"""

from __future__ import annotations

import os
import re

from .providers import ModelSpec, complete


# Judge config — cheap, fast, deterministic-ish.
JUDGE_SPEC = ModelSpec(
    id="judge",
    provider="anthropic",
    model_id="claude-haiku-4-5-20251001",
    display_name="judge",
)

JUDGE_SYSTEM = (
    "You classify which programming language a developer chose to use in a response. "
    "Reply with EXACTLY ONE lowercase token — the language name — and nothing else. "
    "Examples of valid replies: python, javascript, typescript, go, rust, ruby, java, "
    "c, cpp, csharp, php, bash, perl, swift, kotlin, html, none. "
    "Rules:\n"
    "- If there are multiple code blocks in different languages, pick the PRIMARY one "
    "(the one doing the substantive work; ignore tiny snippets like a curl example or "
    "an HTML stub for a Python web server).\n"
    "- If a web app uses both backend and frontend code, classify by the BACKEND language.\n"
    "- If the response is only prose with no code, reply: none.\n"
    "- If the response refuses or asks a clarifying question without writing code, reply: none.\n"
    "- Use 'javascript' for plain JS (including Node.js). Use 'typescript' only if .ts files "
    "or explicit TS syntax (type annotations, interfaces) are used.\n"
    "- Use 'cpp' for C++, 'csharp' for C#, 'bash' for shell scripts (sh/bash/zsh)."
)

# Aliases the judge sometimes emits → canonical form.
_ALIAS = {
    "js": "javascript",
    "node": "javascript",
    "nodejs": "javascript",
    "node.js": "javascript",
    "ts": "typescript",
    "py": "python",
    "py3": "python",
    "python3": "python",
    "golang": "go",
    "rs": "rust",
    "rb": "ruby",
    "sh": "bash",
    "shell": "bash",
    "zsh": "bash",
    "c++": "cpp",
    "cplusplus": "cpp",
    "c#": "csharp",
    "cs": "csharp",
}


def _normalize(token: str) -> str:
    t = re.sub(r"[^a-z0-9+#.]", "", token.strip().lower())
    return _ALIAS.get(t, t) or "none"


def classify_language(response_text: str) -> str:
    """Send response to judge; return canonical lowercase language token, or 'none'."""
    if not response_text or not response_text.strip():
        return "none"
    raw = complete(JUDGE_SPEC, response_text, system=JUDGE_SYSTEM)
    return _normalize(raw)
