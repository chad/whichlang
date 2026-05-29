# whichlang — what language do LLMs reach for?

Generated from `results/runs.jsonl`. Counts: **643** classified runs across **10** models and **16** tasks (157 errors excluded).

Each task prompt describes WHAT to build, never HOW or in what language. Responses are classified by a separate judge LLM. See `tasks.yaml` for prompts.

## Default language by model

Modal language across every task this model was run on.

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **python** | python 51, javascript 13, go 11, html 5 |
| Claude Sonnet 4.6 | **python** | python 59, javascript 9, go 7, html 5 |
| Claude Haiku 4.5 | **python** | python 55, javascript 23, html 2 |
| GPT-5 | **python** | python 56, javascript 13, go 6, html 5 |
| GPT-5 mini | **python** | python 56, javascript 12, go 8, html 4 |
| Gemini 2.5 Flash | **python** | python 3 |
| DeepSeek V3.2 | **python** | python 59, javascript 18, html 2, go 1 |
| Qwen3 Coder 480B | **python** | python 70, javascript 8, html 2 |
| Llama 4 Maverick | **python** | python 71, javascript 8, rust 1 |

## Category: scripting

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **python** | python 20 |
| Claude Sonnet 4.6 | **python** | python 20 |
| Claude Haiku 4.5 | **python** | python 20 |
| GPT-5 | **python** | python 20 |
| GPT-5 mini | **python** | python 20 |
| Gemini 2.5 Flash | **python** | python 3 |
| DeepSeek V3.2 | **python** | python 20 |
| Qwen3 Coder 480B | **python** | python 20 |
| Llama 4 Maverick | **python** | python 20 |

## Category: backend

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **python** | python 9, go 6, javascript 5 |
| Claude Sonnet 4.6 | **python** | python 17, javascript 2, go 1 |
| Claude Haiku 4.5 | **javascript** | javascript 11, python 9 |
| GPT-5 | **python** | python 11, go 6, javascript 3 |
| GPT-5 mini | **python** | python 11, go 8, javascript 1 |
| DeepSeek V3.2 | **python** | python 12, javascript 7, go 1 |
| Qwen3 Coder 480B | **python** | python 20 |
| Llama 4 Maverick | **python** | python 18, javascript 2 |

## Category: cli

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **python** | python 15, go 5 |
| Claude Sonnet 4.6 | **python** | python 14, go 6 |
| Claude Haiku 4.5 | **python** | python 20 |
| GPT-5 | **python** | python 20 |
| GPT-5 mini | **python** | python 20 |
| DeepSeek V3.2 | **python** | python 20 |
| Qwen3 Coder 480B | **python** | python 20 |
| Llama 4 Maverick | **python** | python 19, rust 1 |

## Category: web

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **javascript** | javascript 8, python 7, html 5 |
| Claude Sonnet 4.6 | **python** | python 8, javascript 7, html 5 |
| Claude Haiku 4.5 | **javascript** | javascript 12, python 6, html 2 |
| GPT-5 | **javascript** | javascript 10, html 5, python 5 |
| GPT-5 mini | **javascript** | javascript 11, python 5, html 4 |
| DeepSeek V3.2 | **javascript** | javascript 11, python 7, html 2 |
| Qwen3 Coder 480B | **python** | python 10, javascript 8, html 2 |
| Llama 4 Maverick | **python** | python 14, javascript 6 |

## Full grid (model × task)

| Model | csv_to_json | rename_photos | scrape_h1 | dedupe_lines | hello_api | todo_api | webhook_receiver | rate_limited_proxy | cli_word_count | cli_json_grep | cli_port_check | cli_dir_size | web_counter | web_chat | web_markdown_preview | web_url_shortener |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 4.7 | python 5 | python 5 | python 5 | python 5 | python 4, go 1 | python 5 | javascript 5 | go 5 | python 5 | python 5 | go 5 | python 5 | javascript 3, python 2 | javascript 5 | html 5 | python 5 |
| Claude Sonnet 4.6 | python 5 | python 5 | python 5 | python 5 | python 4, go 1 | python 5 | python 3, javascript 2 | python 5 | go 5 | python 5 | python 4, go 1 | python 5 | python 3, javascript 2 | javascript 5 | html 5 | python 5 |
| Claude Haiku 4.5 | python 5 | python 5 | python 5 | python 5 | python 4, javascript 1 | javascript 5 | javascript 5 | python 5 | python 5 | python 5 | python 5 | python 5 | javascript 4, python 1 | javascript 5 | javascript 3, html 2 | python 5 |
| GPT-5 | python 5 | python 5 | python 5 | python 5 | go 3, javascript 1, +1 other | python 4, javascript 1 | python 3, javascript 1, +1 other | python 3, go 2 | python 5 | python 5 | python 5 | python 5 | javascript 5 | javascript 5 | html 5 | python 5 |
| GPT-5 mini | python 5 | python 5 | python 5 | python 5 | python 3, go 2 | python 4, go 1 | python 4, javascript 1 | go 5 | python 5 | python 5 | python 5 | python 5 | javascript 5 | javascript 5 | html 4, javascript 1 | python 5 |
| Gemini 2.5 Pro | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Gemini 2.5 Flash | python 2 | — | python 1 | — | — | — | — | — | — | — | — | — | — | — | — | — |
| DeepSeek V3.2 | python 5 | python 5 | python 5 | python 5 | python 4, javascript 1 | javascript 4, python 1 | python 3, javascript 2 | python 4, go 1 | python 5 | python 5 | python 5 | python 5 | javascript 3, python 2 | javascript 5 | javascript 3, html 2 | python 5 |
| Qwen3 Coder 480B | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | javascript 5 | javascript 3, html 2 | python 5 |
| Llama 4 Maverick | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 3, javascript 2 | python 5 | python 4, rust 1 | python 5 | python 5 | python 5 | python 4, javascript 1 | javascript 5 | python 5 | python 5 |

---

_Reproduce: `python3 -m whichlang.run` then `python3 -m whichlang.report`._
