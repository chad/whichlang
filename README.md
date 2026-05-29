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

11 models × 23 tasks × 5 samples. Full table in [REPORT.md](REPORT.md).

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
| `fullstack_todo`      | **JavaScript** dominant; **Mistral & Kimi default to TypeScript**; Grok picks plain HTML twice |
| `tcp_echo_100k`       | **Rust** dominant; **Qwen → Go 5/5**, **Grok → Go/C 5/5**, **GPT-5 mini → C 4/5** — Rust is not unanimous |
| `log_histogram_500gb` | **Python** (8/11); **GPT-5 → Go + awk**, **Kimi → Rust 3/5**, **Grok → Go**   |
| `job_runner_5k`       | **Go** (7/11); Haiku, Qwen, Llama stayed on Python              |
| `mac_menubar_llm`     | **Swift** (7/11); Sonnet, Haiku, Qwen went **Python** (rumps/pyobjc) |
| `governance_contract` | **Solidity** (11/11) — universal, no exceptions across any model |
| `k8s_operator_backup` | **Python** (8/11); **DeepSeek & Mistral → Go 5/5** (idiomatic kubebuilder); Kimi splits 3/2 |

**Stand-out divergences worth calling out:**

- **TypeScript bias is European/Chinese, not US.** Mistral Large (4/5 TS) and Kimi
  K2.6 (3/5 TS) are the only models that default to TypeScript for the fullstack
  app. Every US model goes plain JavaScript. New axis of differentiation.
- **Qwen3 Coder picks Go (not Rust) for 100K TCP connections** (5/5 Go). Every
  Western frontier model went Rust. Qwen reaches for goroutines.
- **Grok 4.3 split Go/C for 100K TCP** (3 Go, 2 C, zero Rust). Only model that
  refused Rust entirely for this task. Also produced 11 HTML responses across
  categories — likes shipping a single-file HTML app where others build a stack.
- **Kimi K2.6 is the only model to flip log-500gb to Rust** (3/5 Rust). The
  Rust-friendliest model in the dataset overall (8 Rust picks, more than any other).
- **GPT-5 mini picks C, not Rust**, for the same TCP server. 4/5 samples in plain C.
- **DeepSeek and Mistral both write idiomatic Go for the k8s operator** (5/5 each).
  Every other model wrote a Python script wrapping kubectl.
- **Sonnet, Haiku, and Qwen stay on Python for the Mac menu-bar app** while the
  rest default to Swift. Python pickers know `rumps`/`pyobjc`.
- **Mistral Large is the most-diverse-overall model.** Top categories: python 60,
  go 20, javascript 16, rust 5, swift 5, solidity 5, typescript 4. Picks
  appropriately by task more than any other model in the test.
- **Solidity recognition is universal.** 11/11 models wrote Solidity unprompted
  for the DAO contract. No model hallucinated a "smart-contract.py" anywhere.

### Default language overall (tier-1 + tier-2 combined)

| Model               | Default    | Distribution                                            |
| ---                 | ---        | ---                                                     |
| Claude Opus 4.7     | **python** | python 62, go 20, javascript 16, html 5, swift 5, solidity 5, rust 1, typescript 1 |
| Claude Sonnet 4.6   | **python** | python 74, javascript 14, go 13, html 5, rust 5, solidity 4, +1 other |
| Claude Haiku 4.5    | **python** | python 74, javascript 28, rust 4, solidity 4, html 2, swift 1, cpp 1, go 1 |
| GPT-5               | **python** | python 62, javascript 18, go 15, html 5, solidity 5, swift 4, rust 3, c 2, bash 1 |
| GPT-5 mini          | **python** | python 66, javascript 16, go 13, swift 5, solidity 5, html 4, c 4, rust 1, typescript 1 |
| DeepSeek V3.2       | **python** | python 67, javascript 22, go 9, swift 5, solidity 5, html 2, rust 2, c 2, typescript 1 |
| Qwen3 Coder 480B    | **python** | python 91, javascript 12, go 5, solidity 5, html 2     |
| Llama 4 Maverick    | **python** | python 86, javascript 13, rust 6, swift 5, solidity 5  |
| Mistral Large 2512  | **python** | python 60, go 20, javascript 16, rust 5, swift 5, solidity 5, typescript 4 |
| Grok 4.3            | **python** | python 65, go 18, html 11, javascript 8, swift 5, solidity 5, c 2, bash 1 |
| Kimi K2.6           | **python** | python 61, javascript 14, go 13, rust 8, html 6, solidity 5, swift 4, typescript 3 |

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
