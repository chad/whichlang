"""Aggregate results/runs.jsonl → REPORT.md.

Renders:
  1. Per-model "default language" summary (modal language across all tasks).
  2. Per-category model × language table (which language each model reaches for
     when asked for, e.g., a backend service).
  3. Full model × task grid (compact distribution per cell).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

import yaml

from .providers import load_models


ROOT = Path(__file__).resolve().parent.parent


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def _fmt_dist(counter: Counter, *, top: int = 3) -> str:
    """`python 4, go 1` — most frequent first; cap at `top` entries with a trailing +N."""
    if not counter:
        return "—"
    items = counter.most_common()
    head = items[:top]
    tail = items[top:]
    s = ", ".join(f"{lang} {n}" for lang, n in head)
    if tail:
        s += f", +{sum(n for _, n in tail)} other"
    return s


def _modal(counter: Counter) -> str:
    if not counter:
        return "—"
    return counter.most_common(1)[0][0]


def render(rows: list[dict], models_yaml: Path, tasks_yaml: Path) -> str:
    models = load_models(str(models_yaml))
    with open(tasks_yaml) as f:
        tasks = yaml.safe_load(f)["tasks"]

    model_ids = [m.id for m in models]
    model_display = {m.id: m.display_name for m in models}
    task_ids = [t["id"] for t in tasks]
    task_meta = {t["id"]: t for t in tasks}
    categories: list[str] = []
    for t in tasks:
        if t["category"] not in categories:
            categories.append(t["category"])

    # Dedup: keep the LATEST row per (model, task, sample_idx). If a sample errored
    # or was empty the first time and got retried later, the retry wins.
    latest: dict[tuple[str, str, int], dict] = {}
    for row in rows:
        key = (row["model_id"], row["task_id"], row.get("sample_idx", 0))
        latest[key] = row

    # Index: (model, task) → Counter, (model, category) → Counter, model → Counter
    per_cell: dict[tuple[str, str], Counter] = defaultdict(Counter)
    per_category: dict[tuple[str, str], Counter] = defaultdict(Counter)
    per_model: dict[str, Counter] = defaultdict(Counter)
    total_runs = 0
    errors = 0
    for row in latest.values():
        if row.get("error"):
            errors += 1
            continue
        lang = row.get("language") or "none"
        if lang == "error":
            errors += 1
            continue
        m = row["model_id"]
        t = row["task_id"]
        c = row.get("category") or task_meta.get(t, {}).get("category", "?")
        per_cell[(m, t)][lang] += 1
        per_category[(m, c)][lang] += 1
        per_model[m][lang] += 1
        total_runs += 1

    out: list[str] = []
    out.append("# whichlang — what language do LLMs reach for?\n")
    out.append(
        f"Generated from `results/runs.jsonl`. Counts: **{total_runs}** classified runs "
        f"across **{len(model_ids)}** models and **{len(task_ids)}** tasks "
        f"({errors} errors excluded).\n"
    )
    out.append(
        "Each task prompt describes WHAT to build, never HOW or in what language. "
        "Responses are classified by a separate judge LLM. See `tasks.yaml` for prompts.\n"
    )

    # --- 1. per-model default ---
    out.append("## Default language by model\n")
    out.append("Modal language across every task this model was run on.\n")
    out.append("| Model | Default | Distribution |")
    out.append("|---|---|---|")
    for mid in model_ids:
        if mid not in per_model:
            continue
        out.append(
            f"| {model_display[mid]} | **{_modal(per_model[mid])}** | "
            f"{_fmt_dist(per_model[mid], top=5)} |"
        )
    out.append("")

    # --- 2. per-category × model ---
    for cat in categories:
        out.append(f"## Category: {cat}\n")
        out.append("| Model | Default | Distribution |")
        out.append("|---|---|---|")
        for mid in model_ids:
            c = per_category.get((mid, cat))
            if not c:
                continue
            out.append(
                f"| {model_display[mid]} | **{_modal(c)}** | {_fmt_dist(c, top=4)} |"
            )
        out.append("")

    # --- 3. full grid ---
    out.append("## Full grid (model × task)\n")
    header = "| Model | " + " | ".join(task_ids) + " |"
    sep = "|" + "---|" * (len(task_ids) + 1)
    out.append(header)
    out.append(sep)
    for mid in model_ids:
        row_cells = []
        for tid in task_ids:
            c = per_cell.get((mid, tid))
            row_cells.append(_fmt_dist(c, top=2) if c else "—")
        out.append(f"| {model_display[mid]} | " + " | ".join(row_cells) + " |")
    out.append("")

    out.append("---")
    out.append("\n_Reproduce: `python3 -m whichlang.run` then `python3 -m whichlang.report`._")

    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--results", type=str, default=str(ROOT / "results" / "runs.jsonl"))
    p.add_argument("--models-yaml", type=str, default=str(ROOT / "models.yaml"))
    p.add_argument("--tasks-yaml", type=str, default=str(ROOT / "tasks.yaml"))
    p.add_argument("--out", type=str, default=str(ROOT / "REPORT.md"))
    args = p.parse_args(argv)

    rows = _read_jsonl(Path(args.results))
    if not rows:
        print("no results to report — run `python3 -m whichlang.run` first.", file=sys.stderr)
        return 1
    md = render(rows, Path(args.models_yaml), Path(args.tasks_yaml))
    Path(args.out).write_text(md)
    print(f"wrote {args.out} ({len(rows)} rows)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
