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

---

# Next: add open models

The harness already supports any OpenAI-compatible endpoint, so adding open models is a
YAML edit, not a code change. The interesting decision is which ones, and via what host.

## Recommended open models to add (in priority order)

1. **DeepSeek V3.1** (or V3.2 if released) — frontier-competitive, MIT/MIT-ish license,
   wide deployment. Has both a reasoning ("R1"-style) and non-reasoning variant.
2. **Qwen 3 Coder** (32B or 480B if hosted) — Alibaba's coding-tuned line is the open
   model most likely to behave *differently* from Western frontier models on language
   choice. If anything is going to default to Java or C++, it's a Chinese coder model.
3. **Llama 3.3 70B Instruct** (or Llama 4 Maverick if released and stable) — Meta's
   flagship instruct line, widely cited as the open baseline.

Stretch picks (round it out to 5 if budget allows):
- **Mistral Large 2** — European frontier-tier open weights.
- **Gemma 3 27B** — Google's open line, comparator for Gemini.
- **GLM 4** — increasingly cited.

## How to serve them

### Recommended: OpenRouter (hosted, single API key, all three above)

- One key (`OPENROUTER_API_KEY`), one base_url (`https://openrouter.ai/api/v1`), routes
  to DeepSeek / Qwen / Llama and dozens more.
- Full-precision weights (no quantization artifacts skewing defaults).
- Pay-as-you-go, no monthly minimum. Whole 3-model × 16-task × 5-sample run would be
  under $1 for these models (they're cheap on OpenRouter).
- Slots straight into our `openai_compatible` provider — already supported, no new code.

### Alternative: Together AI / Fireworks / DeepInfra

- Same OpenAI-compatible shape, separate API keys per host.
- Sometimes lower latency or better availability than OpenRouter for a specific model.
- Worth using as a fallback when OpenRouter is rate-limiting.

### Local: Ollama (for reproducibility, smaller models)

- User has Ollama installed (0.5.3 — current is 0.6.x+, **update first**:
  `curl https://ollama.com/install.sh | sh` or download from ollama.com).
- Daemon needs to be running (`ollama serve` or launch the Mac app).
- Exposes an OpenAI-compatible endpoint at `http://localhost:11434/v1` — drops into our
  `openai_compatible` provider, set `api_key_env` to a dummy (Ollama doesn't check it).
- Quantization caveat: Ollama defaults to Q4_K_M (4-bit). For a "what does this model
  default to?" benchmark this may not matter much, but it's worth noting in REPORT.md.
- Hardware limit: 70B models need ~40GB+ RAM. 7B–32B models run well on M-series Macs.
  For Chad's machine, realistic Ollama set: qwen3-coder (7B/32B), llama3.3 (depending
  on RAM), deepseek-r1:32b (the distilled variant).

## Plan

1. [ ] Update Ollama to 0.6.x+ and start the daemon
2. [ ] Decide: hosted (OpenRouter, full-precision) vs local (Ollama, quantized) vs both
3. [ ] Add 3 open models to `models.yaml` based on the chosen host
4. [ ] Run benchmark on just those models (`--models <ids>`); ~$0.50–1.00 on OpenRouter
5. [ ] Regenerate REPORT.md; commit JSONL + updated report
6. [ ] Document quantization caveat in README if Ollama path used
7. [ ] Retry Gemini once free-tier quota resets (or move to billed key) so the table is
       complete

## Why these picks specifically?

The benchmark is most interesting when the model set *spans the space of defaults*.
Three Anthropic + two OpenAI models all defaulted to Python — not surprising, similar
training data. The open model picks above are chosen to **stress-test that assumption**:

- **DeepSeek** is Chinese training data, MoE architecture, distinct lineage.
- **Qwen Coder** is explicitly coding-tuned and Chinese-origin — most likely to surface
  a different default if one exists in the open-model space.
- **Llama** is the most-deployed open baseline; differences from frontier models tell us
  whether "the default is Python" is a frontier phenomenon or universal.

If all three also default to Python, that's itself the story: it's not training-data bias
or RLHF preference, it's that Python *is* the right answer for these prompts.
