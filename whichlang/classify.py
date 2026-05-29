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
    "c, cpp, csharp, php, bash, perl, swift, kotlin, html, solidity, vyper, move, "
    "elixir, erlang, scala, haskell, clojure, dart, lua, hcl, sql, none. "
    "Rules:\n"
    "- If there are multiple code blocks in different languages, pick the PRIMARY one "
    "(the one doing the substantive work; ignore tiny snippets like a curl example or "
    "an HTML stub for a Python web server).\n"
    "- If a web app uses both backend and frontend code, classify by the BACKEND language.\n"
    "- For smart contracts, use 'solidity', 'vyper', or 'move' as appropriate.\n"
    "- For Kubernetes operators or infra code, classify by the implementation language "
    "(usually go or python) not the YAML manifests.\n"
    "- If the response is only prose with no code, reply: none.\n"
    "- If the response refuses or asks a clarifying question without writing code, reply: none.\n"
    "- Use 'javascript' for plain JS (including Node.js). Use 'typescript' only if .ts files "
    "or explicit TS syntax (type annotations, interfaces) are used.\n"
    "- Use 'cpp' for C++, 'csharp' for C#, 'bash' for shell scripts (sh/bash/zsh)."
)

# Canonical lowercase tokens we accept. Anything else gets rescued or marked "none".
_CANONICAL = {
    "python", "javascript", "typescript", "go", "rust", "ruby", "java",
    "c", "cpp", "csharp", "php", "bash", "perl", "swift", "kotlin",
    "html", "elixir", "scala", "haskell", "clojure", "dart", "lua",
    "r", "julia", "zig", "ocaml", "fsharp", "erlang",
    "solidity", "vyper", "move", "hcl", "sql", "none",
}

# Aliases the judge sometimes emits → canonical form.
_ALIAS = {
    "js": "javascript", "node": "javascript", "nodejs": "javascript", "node.js": "javascript",
    "ts": "typescript",
    "py": "python", "py3": "python", "python3": "python",
    "golang": "go",
    "rs": "rust",
    "rb": "ruby",
    "sh": "bash", "shell": "bash", "zsh": "bash",
    "c++": "cpp", "cplusplus": "cpp",
    "c#": "csharp", "cs": "csharp",
    "fs": "fsharp", "f#": "fsharp",
}


def _normalize(raw: str) -> str:
    """Map a judge reply (ideally one token, sometimes prose) to a canonical token."""
    s = raw.strip().lower()
    # Strict path: judge replied with one token (possibly punctuated).
    one = re.sub(r"[^a-z0-9+#.]", "", s)
    if one in _CANONICAL:
        return one
    if one in _ALIAS:
        return _ALIAS[one]
    # Rescue: judge wrote prose. Scan for a known canonical / aliased word.
    # Word-boundary scan so "python" inside "monkeypython" wouldn't match,
    # and we hit the FIRST language the judge mentioned (usually its verdict).
    for match in re.finditer(r"[a-z][a-z0-9+#.]*", s):
        w = match.group(0)
        if w in _CANONICAL:
            return w
        if w in _ALIAS:
            return _ALIAS[w]
    return "none"


def classify_language(response_text: str) -> str:
    """Send response to judge; return canonical lowercase language token, or 'none'."""
    if not response_text or not response_text.strip():
        return "none"
    raw = complete(JUDGE_SPEC, response_text, system=JUDGE_SYSTEM)
    return _normalize(raw)
