# whichlang

**When you hand an LLM a coding task and don't tell it what language to use, what does it reach for?**

`whichlang` is a small benchmark harness that asks frontier LLMs to write code for common,
language-agnostic tasks and tallies which programming language each one picks. The output
is a table that tells a developer at a glance: *if I ask Claude / GPT / Gemini for "a
script that..." or "a small web app for...", what am I going to get back?*

The whole point is the **defaults**. Prompts deliberately never mention a language and
never invite the model to choose one — that would change what's being measured.

---

## Latest results

8 models × 16 tasks × 5 samples = 640 classified runs (Gemini results pending — see
[Limitations](#limitations)). Full table in [REPORT.md](REPORT.md).

### Default language across all tasks

| Model               | Default    | Distribution                                |
| ---                 | ---        | ---                                         |
| Claude Opus 4.7     | **python** | python 51, javascript 13, go 11, html 5     |
| Claude Sonnet 4.6   | **python** | python 59, javascript 9, go 7, html 5       |
| Claude Haiku 4.5    | **python** | python 55, javascript 23, html 2            |
| GPT-5               | **python** | python 56, javascript 13, go 6, html 5      |
| GPT-5 mini          | **python** | python 56, javascript 12, go 8, html 4      |
| DeepSeek V3.2       | **python** | python 59, javascript 18, html 2, go 1      |
| Qwen3 Coder 480B    | **python** | python 70, javascript 8, html 2             |
| Llama 4 Maverick    | **python** | python 71, javascript 8, rust 1             |

### Headline findings

- **Python is the universal default.** All 8 models — frontier closed and open
  weights alike — default to Python overall. **Scripting and CLI tasks are Python
  ~100% of the time** across the board.
- **The "switch to JavaScript for web" is a frontier reflex.** All 5 closed-source
  frontier models + DeepSeek flip their default to JavaScript for web-app tasks.
  The two open flagship models (Qwen3 Coder, Llama 4 Maverick) **stay on Python**
  for most web tasks — they only switch to JS for `web_chat`.
- **Qwen3 Coder is the most Python-heavy model in the test** at 70/80 — more than
  any frontier model. Despite being a coding-tuned model, it almost never reaches
  for an alternative.
- **Backend service defaults split.** Sonnet, GPT-5, GPT-5 mini, DeepSeek, Qwen,
  and Llama all default to Python. Claude Haiku actually prefers JavaScript over
  Python here (11 vs 9). Opus leans Python with Go as a near-equal second.
- **Go shows up almost exclusively for `rate_limited_proxy` and a few CLI tasks**
  on Claude / GPT-5 — open models picked Go just once across 240 runs.
- **Llama 4 Maverick is the only model to pick Rust** (1/5 on `cli_word_count`).
  The first non-`{python, javascript, go, html}` choice in the entire dataset.

See [REPORT.md](REPORT.md) for the full model × task grid and per-category breakdown.

---

## How it works

1. **`tasks.yaml`** — 16 language-neutral prompts across 4 categories (scripting, backend,
   CLI, web). Each describes WHAT to build, never HOW or in what language.
2. **`models.yaml`** — the models under test. Provider abstraction supports Anthropic,
   OpenAI, Google, and any OpenAI-compatible endpoint (which covers Ollama, OpenRouter,
   Together, Fireworks, DeepInfra, vLLM, etc. — adding open models is a YAML edit).
3. **`whichlang/run.py`** — for each `(model, task, sample_idx)` not already in
   `results/runs.jsonl`, calls the model, classifies the response, appends one JSONL line.
   Resumable; safe to ctrl-C and re-run.
4. **`whichlang/classify.py`** — a judge LLM (Claude Haiku 4.5) reads the response and
   emits a single canonical language token. The judge sees only the response, never which
   model produced it, so it can't bias toward expected defaults.
5. **`whichlang/report.py`** — aggregates JSONL → `REPORT.md`: per-model defaults,
   per-category breakdowns, and the full model × task grid.

### Methodology notes

- **5 samples per (model, task)** to surface non-determinism (a model that's 4/5 Python,
  1/5 Go is genuinely split). Default temperature; no seed.
- **Same system prompt for every model**: "write working code, pick whatever language and
  tools you think are best, don't ask clarifying questions, don't list multiple options."
  Without the last clause many models offer 2–3 alternatives, which obscures the default.
- **Reasoning models** (GPT-5, o-series) burn token budget on hidden chain-of-thought
  before producing visible output. The OpenAI call uses `max_completion_tokens=16384` so
  reasoning + response both fit.
- **Errors are kept in JSONL but excluded from totals** and get re-attempted on resume.

---

## Limitations

- **No Gemini data yet.** The first benchmark run hit Google's free-tier quota
  mid-flight: Gemini 2.5 Pro is at 0/80 runs, Flash at 3/80. Re-run with a billed
  Google AI Studio key or wait for quota reset.
- **Open models served via OpenRouter** (full-precision hosted, not local-quantized).
  Same prompts + harness; different host. A local-Ollama comparison would be a
  useful follow-up to see whether Q4 quantization shifts defaults.
- **Single judge** (Claude Haiku 4.5). A judge that's wrong systematically would be
  hard to catch from this side. The judge prompt is constrained to one token and the
  raw response is stored, so a second judge could rescore the existing JSONL without
  re-running.
- **English prompts only.** Defaults may differ in other languages.
- **Snapshot in time.** Model defaults change with versions; results are dated by commit.

---

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...
export GEMINI_API_KEY=...   # optional
```

## Run

```bash
# default: every model in models.yaml × every task in tasks.yaml × 5 samples
.venv/bin/python -m whichlang.run

# subset
.venv/bin/python -m whichlang.run --models claude-opus-4-7,gpt-5 --tasks csv_to_json --samples 3

# render REPORT.md from results/runs.jsonl
.venv/bin/python -m whichlang.report
```

## Adding models

Edit `models.yaml`. For an OpenAI-compatible host (OpenRouter, Together, Ollama, vLLM, …):

```yaml
- id: deepseek-v3.1
  provider: openai_compatible
  model_id: deepseek/deepseek-chat
  display_name: DeepSeek V3.1
  base_url: https://openrouter.ai/api/v1
  api_key_env: OPENROUTER_API_KEY
```

No code changes needed.

## Adding tasks

Edit `tasks.yaml`. Each task is `{id, category, prompt}`. Keep prompts language-neutral —
if you mention a language or invite the model to choose, you change what's being measured.

## Files

```
tasks.yaml              # the prompts
models.yaml             # the models under test
whichlang/providers.py  # unified .complete() across providers
whichlang/classify.py   # judge LLM
whichlang/run.py        # main runner — resumable
whichlang/report.py     # JSONL → REPORT.md
results/runs.jsonl      # raw per-run data (committed so others can re-aggregate)
REPORT.md               # generated table
plan.md                 # roadmap and open questions
```

## Contributing

Open to PRs that add models, tasks, or alternative judges. If you add a model, please
include the run output (a new `results/runs.jsonl` is fine to commit — it's append-only
and others can re-aggregate it).

## License

MIT.
