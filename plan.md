# whichlang — plan

## Goal

A harness that asks LLMs to write code for common, language-agnostic tasks and records which programming language each model defaults to. Output is a table (model × task → language distribution) that's useful to developers as a signal of what an LLM will reach for unprompted.

## Design decisions (from user)

- **Sampling**: N runs per (model, task), report full distribution (e.g. `python 7/10, go 3/10`).
- **Language detection**: judge LLM classifies each response (handles weird formatting, multi-language responses, "I'd recommend X" prose).
- **Task categories**: scripting/glue, backend service/API, CLI tool, web app.
- **Output**: markdown table for humans + JSONL of raw runs so others can re-aggregate.

## Architecture

```
whichlang/
├── tasks.yaml              # ~3-5 prompts per category, language-neutral
├── models.yaml             # list of (provider, model_id, display_name)
├── whichlang/
│   ├── providers.py        # unified .complete(model, prompt) → str across Anthropic, OpenAI, Google, OpenAI-compatible
│   ├── classify.py         # judge LLM: response → language name (lowercase) or "none"
│   ├── run.py              # main loop; resumable; appends to results/runs.jsonl
│   └── report.py           # JSONL → REPORT.md (markdown table) + summary stats
├── results/runs.jsonl      # one line per (model, task, sample) with raw response + classified language
└── REPORT.md               # generated
```

### Provider abstraction

One function: `complete(model_spec, prompt) -> str`. `model_spec` carries provider + model_id + optional base_url. This makes adding open models (DeepSeek, Llama, Qwen via Together/Fireworks/OpenRouter) a config-file change, not a code change — any OpenAI-compatible endpoint plugs in.

### Resumability

Runs.jsonl is append-only. Each line carries `(model_id, task_id, sample_idx)`. On startup, `run.py` reads existing lines and skips combinations already done. Safe to ctrl-C and resume.

### Prompt design

Prompts must NOT mention a language or ask the model to choose. They should read like a normal developer request: "I need a tool that takes a CSV and emits JSON. Write it." If we hint or ask "what language would you use," we measure something different.

System prompt: minimal — just nudge toward producing runnable code in one language, no clarifying questions. Goal is to capture the model's default, not its question-asking behavior.

### Judge

Cheap small model (e.g. claude-haiku or gpt-5-mini). Input: the raw response. Output: a single lowercase language token. Bias check: judge sees only the code, not which model produced it.

## Initial model set

Adjustable in models.yaml. Starting with:
- Anthropic: claude-opus-4-7, claude-sonnet-4-6, claude-haiku-4-5
- OpenAI: gpt-5, gpt-5-mini (or current equivalents)
- Google: gemini-2.5-pro, gemini-2.5-flash

## Steps

1. [x] Confirm design with user
2. [x] Write providers.py
3. [x] Write tasks.yaml (16 tasks across 4 categories)
4. [x] Write models.yaml (3 Anthropic + 2 OpenAI + 2 Google = 7 models)
5. [x] Write run.py (resumable loop, JSONL output)
6. [x] Write classify.py (judge LLM = claude-haiku-4-5)
7. [x] Write report.py (markdown table generator)
8. [x] Smoke test: 1 sample on Anthropic + OpenAI + Google paths — all three work end-to-end
9. [x] README
10. [x] Initial git commit
11. [ ] Ask user before running the full benchmark (API spend ~7×16×5 = 560 generation calls + 560 judge calls)

## Notes from smoke test

- Resume logic initially counted errored runs as "done", so a transient Google 503 would
  never get retried. Fixed: errors stay in the JSONL for the record but `_load_done`
  ignores them so they get re-attempted on the next run.
- All three providers wire up cleanly. The classifier returned "python" on the same task
  for all three smoke-tested models (csv_to_json), which is the expected boring baseline.

## Open questions to revisit

- How many samples per (model, task)? Starting plan: 5. Trades cost vs. distribution confidence.
- Do we also capture *reasoning* (does the model justify the choice)? Could be a follow-up column.
- Should the prompt forbid clarifying questions or let "I'd need to know X first" responses count as a no-op? Currently treating no-code responses as `none` in the distribution.
