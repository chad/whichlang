# whichlang — what language do LLMs reach for?

Generated from `results/runs.jsonl`. Counts: **1268** classified runs across **13** models and **23** tasks (157 errors excluded).

Each task prompt describes WHAT to build, never HOW or in what language. Responses are classified by a separate judge LLM. See `tasks.yaml` for prompts.

## Default language by model

Modal language across every task this model was run on.

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **python** | python 62, go 20, javascript 16, html 5, swift 5, +7 other |
| Claude Sonnet 4.6 | **python** | python 74, javascript 14, go 13, html 5, rust 5, +4 other |
| Claude Haiku 4.5 | **python** | python 74, javascript 28, rust 4, solidity 4, html 2, +3 other |
| GPT-5 | **python** | python 62, javascript 18, go 15, html 5, solidity 5, +10 other |
| GPT-5 mini | **python** | python 66, javascript 16, go 13, swift 5, solidity 5, +10 other |
| Gemini 2.5 Flash | **python** | python 3 |
| DeepSeek V3.2 | **python** | python 67, javascript 22, go 9, swift 5, solidity 5, +7 other |
| Qwen3 Coder 480B | **python** | python 91, javascript 12, go 5, solidity 5, html 2 |
| Llama 4 Maverick | **python** | python 86, javascript 13, rust 6, swift 5, solidity 5 |
| Mistral Large 2512 | **python** | python 60, go 20, javascript 16, rust 5, swift 5, +9 other |
| Grok 4.3 | **python** | python 65, go 18, html 11, javascript 8, swift 5, +8 other |
| Kimi K2.6 | **python** | python 61, javascript 14, go 13, rust 8, html 6, +13 other |

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
| Mistral Large 2512 | **python** | python 20 |
| Grok 4.3 | **python** | python 20 |
| Kimi K2.6 | **python** | python 20 |

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
| Mistral Large 2512 | **python** | python 10, go 10 |
| Grok 4.3 | **python** | python 10, go 7, javascript 3 |
| Kimi K2.6 | **python** | python 13, go 5, javascript 2 |

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
| Mistral Large 2512 | **python** | python 20 |
| Grok 4.3 | **python** | python 19, go 1 |
| Kimi K2.6 | **python** | python 17, go 3 |

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
| Mistral Large 2512 | **javascript** | javascript 15, python 5 |
| Grok 4.3 | **html** | html 9, python 8, javascript 3 |
| Kimi K2.6 | **javascript** | javascript 9, html 6, python 5 |

## Category: fullstack

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **javascript** | javascript 3, python 1, typescript 1 |
| Claude Sonnet 4.6 | **javascript** | javascript 5 |
| Claude Haiku 4.5 | **javascript** | javascript 5 |
| GPT-5 | **javascript** | javascript 4, python 1 |
| GPT-5 mini | **javascript** | javascript 4, typescript 1 |
| DeepSeek V3.2 | **javascript** | javascript 4, typescript 1 |
| Qwen3 Coder 480B | **javascript** | javascript 4, python 1 |
| Llama 4 Maverick | **javascript** | javascript 5 |
| Mistral Large 2512 | **typescript** | typescript 4, javascript 1 |
| Grok 4.3 | **javascript** | javascript 2, html 2, python 1 |
| Kimi K2.6 | **typescript** | typescript 3, javascript 2 |

## Category: systems

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **go** | go 6, python 3, rust 1 |
| Claude Sonnet 4.6 | **rust** | rust 5, python 5 |
| Claude Haiku 4.5 | **python** | python 5, rust 4, go 1 |
| GPT-5 | **go** | go 4, rust 3, c 2, bash 1 |
| GPT-5 mini | **python** | python 5, c 4, rust 1 |
| DeepSeek V3.2 | **python** | python 6, rust 2, c 2 |
| Qwen3 Coder 480B | **go** | go 5, python 5 |
| Llama 4 Maverick | **rust** | rust 5, python 5 |
| Mistral Large 2512 | **rust** | rust 5, python 5 |
| Grok 4.3 | **go** | go 6, c 2, python 1, bash 1 |
| Kimi K2.6 | **rust** | rust 8, none 1, python 1 |

## Category: realtime

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **go** | go 3, python 2 |
| Claude Sonnet 4.6 | **go** | go 5 |
| Claude Haiku 4.5 | **python** | python 5 |
| GPT-5 | **go** | go 5 |
| GPT-5 mini | **go** | go 5 |
| DeepSeek V3.2 | **go** | go 3, python 2 |
| Qwen3 Coder 480B | **python** | python 5 |
| Llama 4 Maverick | **python** | python 5 |
| Mistral Large 2512 | **go** | go 5 |
| Grok 4.3 | **go** | go 3, python 2 |
| Kimi K2.6 | **go** | go 3, python 2 |

## Category: desktop

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **swift** | swift 5 |
| Claude Sonnet 4.6 | **python** | python 5 |
| Claude Haiku 4.5 | **python** | python 4, swift 1 |
| GPT-5 | **swift** | swift 4, javascript 1 |
| GPT-5 mini | **swift** | swift 5 |
| DeepSeek V3.2 | **swift** | swift 5 |
| Qwen3 Coder 480B | **python** | python 5 |
| Llama 4 Maverick | **swift** | swift 5 |
| Mistral Large 2512 | **swift** | swift 5 |
| Grok 4.3 | **swift** | swift 5 |
| Kimi K2.6 | **swift** | swift 4, javascript 1 |

## Category: domain

| Model | Default | Distribution |
|---|---|---|
| Claude Opus 4.7 | **solidity** | solidity 5, python 5 |
| Claude Sonnet 4.6 | **python** | python 5, solidity 4, go 1 |
| Claude Haiku 4.5 | **python** | python 5, solidity 4, cpp 1 |
| GPT-5 | **solidity** | solidity 5, python 5 |
| GPT-5 mini | **solidity** | solidity 5, python 5 |
| DeepSeek V3.2 | **solidity** | solidity 5, go 5 |
| Qwen3 Coder 480B | **solidity** | solidity 5, python 5 |
| Llama 4 Maverick | **solidity** | solidity 5, python 5 |
| Mistral Large 2512 | **solidity** | solidity 5, go 5 |
| Grok 4.3 | **solidity** | solidity 5, python 4, go 1 |
| Kimi K2.6 | **solidity** | solidity 5, python 3, go 2 |

## Full grid (model × task)

| Model | csv_to_json | rename_photos | scrape_h1 | dedupe_lines | hello_api | todo_api | webhook_receiver | rate_limited_proxy | cli_word_count | cli_json_grep | cli_port_check | cli_dir_size | web_counter | web_chat | web_markdown_preview | web_url_shortener | fullstack_todo | tcp_echo_100k | log_histogram_500gb | job_runner_5k | mac_menubar_llm | governance_contract | k8s_operator_backup |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 4.7 | python 5 | python 5 | python 5 | python 5 | python 4, go 1 | python 5 | javascript 5 | go 5 | python 5 | python 5 | go 5 | python 5 | javascript 3, python 2 | javascript 5 | html 5 | python 5 | javascript 3, python 1, +1 other | go 4, rust 1 | python 3, go 2 | go 3, python 2 | swift 5 | solidity 5 | python 5 |
| Claude Sonnet 4.6 | python 5 | python 5 | python 5 | python 5 | python 4, go 1 | python 5 | python 3, javascript 2 | python 5 | go 5 | python 5 | python 4, go 1 | python 5 | python 3, javascript 2 | javascript 5 | html 5 | python 5 | javascript 5 | rust 5 | python 5 | go 5 | python 5 | solidity 4, python 1 | python 4, go 1 |
| Claude Haiku 4.5 | python 5 | python 5 | python 5 | python 5 | python 4, javascript 1 | javascript 5 | javascript 5 | python 5 | python 5 | python 5 | python 5 | python 5 | javascript 4, python 1 | javascript 5 | javascript 3, html 2 | python 5 | javascript 5 | rust 4, go 1 | python 5 | python 5 | python 4, swift 1 | solidity 4, cpp 1 | python 5 |
| GPT-5 | python 5 | python 5 | python 5 | python 5 | go 3, javascript 1, +1 other | python 4, javascript 1 | python 3, javascript 1, +1 other | python 3, go 2 | python 5 | python 5 | python 5 | python 5 | javascript 5 | javascript 5 | html 5 | python 5 | javascript 4, python 1 | rust 3, c 2 | go 4, bash 1 | go 5 | swift 4, javascript 1 | solidity 5 | python 5 |
| GPT-5 mini | python 5 | python 5 | python 5 | python 5 | python 3, go 2 | python 4, go 1 | python 4, javascript 1 | go 5 | python 5 | python 5 | python 5 | python 5 | javascript 5 | javascript 5 | html 4, javascript 1 | python 5 | javascript 4, typescript 1 | c 4, rust 1 | python 5 | go 5 | swift 5 | solidity 5 | python 5 |
| Gemini 2.5 Pro | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| Gemini 2.5 Flash | python 2 | — | python 1 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| DeepSeek V3.2 | python 5 | python 5 | python 5 | python 5 | python 4, javascript 1 | javascript 4, python 1 | python 3, javascript 2 | python 4, go 1 | python 5 | python 5 | python 5 | python 5 | javascript 3, python 2 | javascript 5 | javascript 3, html 2 | python 5 | javascript 4, typescript 1 | rust 2, c 2, +1 other | python 5 | go 3, python 2 | swift 5 | solidity 5 | go 5 |
| Qwen3 Coder 480B | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | javascript 5 | javascript 3, html 2 | python 5 | javascript 4, python 1 | go 5 | python 5 | python 5 | python 5 | solidity 5 | python 5 |
| Llama 4 Maverick | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | python 3, javascript 2 | python 5 | python 4, rust 1 | python 5 | python 5 | python 5 | python 4, javascript 1 | javascript 5 | python 5 | python 5 | javascript 5 | rust 5 | python 5 | python 5 | swift 5 | solidity 5 | python 5 |
| Mistral Large 2512 | python 5 | python 5 | python 5 | python 5 | python 5 | python 5 | go 5 | go 5 | python 5 | python 5 | python 5 | python 5 | javascript 5 | javascript 5 | javascript 5 | python 5 | typescript 4, javascript 1 | rust 5 | python 5 | go 5 | swift 5 | solidity 5 | go 5 |
| Grok 4.3 | python 5 | python 5 | python 5 | python 5 | go 3, javascript 1, +1 other | python 5 | javascript 2, python 2, +1 other | go 3, python 2 | python 5 | python 5 | python 4, go 1 | python 5 | python 4, html 1 | html 4, javascript 1 | html 4, javascript 1 | python 4, javascript 1 | javascript 2, html 2, +1 other | go 3, c 2 | go 3, python 1, +1 other | go 3, python 2 | swift 5 | solidity 5 | python 4, go 1 |
| Kimi K2.6 | python 5 | python 5 | python 5 | python 5 | go 3, python 1, +1 other | python 5 | python 4, javascript 1 | python 3, go 2 | python 5 | python 5 | go 3, python 2 | python 5 | javascript 4, python 1 | javascript 5 | html 5 | python 4, html 1 | typescript 3, javascript 2 | rust 5 | rust 3, none 1, +1 other | go 3, python 2 | swift 4, javascript 1 | solidity 5 | python 3, go 2 |

---

_Reproduce: `python3 -m whichlang.run` then `python3 -m whichlang.report`._
