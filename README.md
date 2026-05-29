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

8 models × 23 tasks × 5 samples. Full table in [REPORT.md](REPORT.md).

The task set is split into two tiers:

- **Tier 1 — small, common tasks** (16 tasks across scripting, backend, cli, web). What
  do models reach for when you ask for "a script to ..." or "a small ... app"?
- **Tier 2 — substantial tasks** (7 tasks across fullstack, systems, realtime, desktop,
  domain). Tasks with scale, platform, or domain constraints that make the universal
  Python default actually wrong — designed to surface real differentiation.

### Headline findings

**On tier-1 (small tasks): Python is the universal default.** All 8 models default to
Python overall. Scripting and CLI tasks are Python ~100% of the time across the board.
The only category where the default flips is `web` (4 of 6 well-tested models switch to
JavaScript; Qwen3 Coder and Llama 4 stay on Python).

**On tier-2 (substantial tasks): the default explodes into diversity.** This is the more
interesting finding. Each model picks a *different* primary tool depending on the actual
constraint, and the picks across models diverge meaningfully:

| Task                  | What most models reached for                                    |
| ---                   | ---                                                             |
| `fullstack_todo`      | **JavaScript** (7/7) — universal; one Opus run picked TS        |
| `tcp_echo_100k`       | **Rust** (5/6) — Sonnet, Haiku, Llama all 4–5/5 Rust; GPT-5 mini went **C** |
| `log_histogram_500gb` | **Python** (4/6), but GPT-5 went **Go** 4/5 + awk/bash          |
| `job_runner_5k`       | **Go** (5/6); Claude Haiku stayed on Python                     |
| `mac_menubar_llm`     | **Swift** (4/6); Sonnet went **Python** (rumps/pyobjc); Haiku mostly Python |
| `governance_contract` | **Solidity** (6/6) — universal                                  |
| `k8s_operator_backup` | **Python** (5/6); **DeepSeek went pure Go** 5/5 (idiomatic for k8s) |

**Stand-out divergences worth calling out:**

- **GPT-5 mini picked C, not Rust**, for the 100K-connection TCP server. 4/5 samples
  in plain C. None of the other 5 frontier models chose C — they all went Rust.
- **Claude Sonnet 4.6 chose Python for the Mac menu-bar app** (5/5) while every other
  frontier model defaulted to Swift. Sonnet knows `rumps`/`pyobjc` and reaches for them.
- **DeepSeek defaulted to Go for the Kubernetes operator** while every other model wrote
  a Python script wrapping kubectl. DeepSeek is the only model that wrote idiomatic
  kubebuilder-style code unprompted.
- **Solidity recognition is universal.** Every model — including the open ones — wrote
  Solidity unprompted for the DAO contract. No model hallucinated a "smart-contract.py".

### Default language overall (tier-1 + tier-2 combined)

| Model               | Default    | Distribution                                            |
| ---                 | ---        | ---                                                     |
| Claude Opus 4.7     | **python** | python 56, javascript 16, go 14, html 5, swift 5, solidity 5, rust 1, typescript 1 |
| Claude Sonnet 4.6   | **python** | python 70, javascript 14, go 8, rust 5, html 5, solidity 4 |
| Claude Haiku 4.5    | **python** | python 64, javascript 23, solidity 4, rust 4, html 2, swift 1, cpp 1, go 1 |
| GPT-5               | **python** | python 62, javascript 14, go 10, swift 4, html 5, rust 3, solidity 5, c 2, bash 1 |
| GPT-5 mini          | **python** | python 61, javascript 13, go 13, html 4, swift 5, solidity 5, c 4, rust 1, typescript 1 |
| DeepSeek V3.2       | **python** | python 65, javascript 23, go 9, swift 5, solidity 5, html 2, rust 2, c 2, typescript 1 |
| Qwen3 Coder 480B    | **python** | python 70, javascript 8, html 2 *(tier-2 partial — see below)* |
| Llama 4 Maverick    | **python** | python 79, javascript 13, rust 6 *(tier-2 partial — see below)* |

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
- **Qwen3 Coder + Llama 4 Maverick have only partial tier-2 data.** The OpenRouter
  account ran out of credit mid-run. Qwen3 Coder is missing all 7 tier-2 tasks;
  Llama 4 Maverick has some. Resuming with credit will fill these in.
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
