# whichlang

When you hand an LLM a coding task and don't tell it what language to use, what does it reach for?

`whichlang` is a small harness that asks a fleet of LLMs to write code for common,
language-agnostic tasks and tallies the languages they pick. The output is a markdown
table that lets a developer see at a glance what each model defaults to — useful for
understanding what you're going to get when you ask for "a script that..." or "a small
web app for...".

## How it works

1. `tasks.yaml` — language-neutral prompts. Each describes WHAT to build, never HOW or
   in what language. If a prompt mentions a language or hints "use whatever you like",
   it biases the measurement, so the prompts are kept clean.
2. `models.yaml` — the models under test (Anthropic / OpenAI / Google to start; any
   OpenAI-compatible endpoint slots in for open-weight models like DeepSeek, Llama,
   Qwen via OpenRouter, Together, Fireworks, vLLM, etc.).
3. `whichlang/run.py` — for each `(model, task, sample_idx)` not already in
   `results/runs.jsonl`, calls the model, sends the response to a judge LLM that
   identifies the primary language, and appends one JSONL line. Resumable; safe to
   ctrl-C and re-run.
4. `whichlang/report.py` — aggregates the JSONL into `REPORT.md`: a per-model default,
   a per-category breakdown, and a full model × task grid.

The judge LLM is a separate model from the ones under test, sees only the response
text (not which model produced it), and is constrained to emit a single lowercase
language token.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...
export GEMINI_API_KEY=...
```

## Run

```bash
# default: every model in models.yaml × every task in tasks.yaml × 5 samples
.venv/bin/python -m whichlang.run

# subset
.venv/bin/python -m whichlang.run --models claude-opus-4-7,gpt-5 --tasks csv_to_json --samples 3

# generate the markdown report from results/runs.jsonl
.venv/bin/python -m whichlang.report
```

## Adding models

Edit `models.yaml`. For an open-weight model behind an OpenAI-compatible host:

```yaml
- id: deepseek-v3
  provider: openai_compatible
  model_id: deepseek/deepseek-chat
  display_name: DeepSeek V3
  base_url: https://openrouter.ai/api/v1
  api_key_env: OPENROUTER_API_KEY
```

No code changes needed.

## Adding tasks

Edit `tasks.yaml`. Each task is `{id, category, prompt}`. Existing categories are
`scripting`, `backend`, `cli`, `web`; add new ones freely. Keep prompts language-neutral
— if you mention a language or invite the model to choose, you change what's being
measured.

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
```
