"""Unified completion interface across Anthropic, OpenAI, Google, and OpenAI-compatible endpoints.

One function: complete(spec, prompt, system=None) -> str.

A ModelSpec describes provider + model_id (+ optional base_url for OpenAI-compatible hosts).
Adding open models — DeepSeek, Llama, Qwen via Together/Fireworks/OpenRouter — is a YAML
edit, not a code change: point provider=openai_compatible at the relevant base_url.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ModelSpec:
    id: str                  # stable key used in JSONL / report
    provider: str            # anthropic | openai | google | openai_compatible
    model_id: str            # provider-side model identifier
    display_name: str        # for the report
    base_url: Optional[str] = None
    api_key_env: Optional[str] = None  # override default env var name


def _anthropic_complete(spec: ModelSpec, prompt: str, system: Optional[str]) -> str:
    import anthropic
    key = os.environ[spec.api_key_env or "ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=key)
    kwargs = {
        "model": spec.model_id,
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    msg = client.messages.create(**kwargs)
    parts = [b.text for b in msg.content if getattr(b, "type", None) == "text"]
    return "".join(parts)


def _openai_complete(spec: ModelSpec, prompt: str, system: Optional[str]) -> str:
    from openai import OpenAI
    key = os.environ[spec.api_key_env or "OPENAI_API_KEY"]
    client = OpenAI(api_key=key, base_url=spec.base_url) if spec.base_url else OpenAI(api_key=key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=spec.model_id,
        messages=messages,
        max_completion_tokens=2048,
    )
    return resp.choices[0].message.content or ""


def _google_complete(spec: ModelSpec, prompt: str, system: Optional[str]) -> str:
    from google import genai
    from google.genai import types
    key = os.environ[spec.api_key_env or "GEMINI_API_KEY"]
    client = genai.Client(api_key=key)
    config = types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=2048,
    ) if system else types.GenerateContentConfig(max_output_tokens=2048)
    resp = client.models.generate_content(
        model=spec.model_id,
        contents=prompt,
        config=config,
    )
    return resp.text or ""


_DISPATCH = {
    "anthropic": _anthropic_complete,
    "openai": _openai_complete,
    "openai_compatible": _openai_complete,
    "google": _google_complete,
}


def complete(spec: ModelSpec, prompt: str, system: Optional[str] = None) -> str:
    fn = _DISPATCH.get(spec.provider)
    if fn is None:
        raise ValueError(f"unknown provider: {spec.provider}")
    return fn(spec, prompt, system)


def load_models(path: str) -> list[ModelSpec]:
    import yaml
    with open(path) as f:
        data = yaml.safe_load(f)
    return [ModelSpec(**entry) for entry in data["models"]]
