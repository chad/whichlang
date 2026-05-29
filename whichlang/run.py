"""Main runner: for each (model, task, sample_idx) not already in results/runs.jsonl,
call the model, classify the response, append a JSONL line.

Resumable — append-only. Ctrl-C and re-run; it picks up where it left off.

Usage:
    python3 -m whichlang.run                       # default: 5 samples, all models, all tasks
    python3 -m whichlang.run --samples 3
    python3 -m whichlang.run --models claude-opus-4-7,gpt-5
    python3 -m whichlang.run --tasks csv_to_json,hello_api
    python3 -m whichlang.run --concurrency 6
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable

import yaml

from .classify import classify_language
from .providers import ModelSpec, complete, load_models


ROOT = Path(__file__).resolve().parent.parent
RESULTS_PATH = ROOT / "results" / "runs.jsonl"

SYSTEM_PROMPT = (
    "You are helping a developer with a coding task. Write working code that solves the "
    "problem. Pick whatever language and tools you think are best — do not ask the developer "
    "to choose. Do not ask clarifying questions; make reasonable assumptions and proceed. "
    "Keep the response focused: a brief intro sentence is fine, then the code, then any "
    "short usage note. Do not list multiple language options."
)


def _load_tasks(path: Path) -> list[dict]:
    with open(path) as f:
        return yaml.safe_load(f)["tasks"]


def _load_done(path: Path) -> set[tuple[str, str, int]]:
    if not path.exists():
        return set()
    done: set[tuple[str, str, int]] = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            # Only count as "done" if the run actually produced a classified language
            # with a non-empty response. Errored rows and empty-response "none" rows
            # (transient provider failures) stay in the JSONL for the record but get
            # retried on resume. A real "none" with prose-only output is kept as done.
            if row.get("error") or row.get("language") in (None, "error"):
                continue
            if row.get("language") == "none" and not (row.get("response") or "").strip():
                continue
            try:
                done.add((row["model_id"], row["task_id"], row["sample_idx"]))
            except KeyError:
                continue
    return done


def _append_jsonl(path: Path, row: dict, lock: threading.Lock) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(row, ensure_ascii=False)
    with lock:
        with open(path, "a") as f:
            f.write(line + "\n")


def _run_one(
    spec: ModelSpec,
    task: dict,
    sample_idx: int,
) -> dict:
    t0 = time.time()
    try:
        response = complete(spec, task["prompt"], system=SYSTEM_PROMPT)
        elapsed_ms = int((time.time() - t0) * 1000)
        try:
            language = classify_language(response)
            classify_err = None
        except Exception as e:
            language = "error"
            classify_err = f"{type(e).__name__}: {e}"
        return {
            "model_id": spec.id,
            "task_id": task["id"],
            "category": task["category"],
            "sample_idx": sample_idx,
            "language": language,
            "elapsed_ms": elapsed_ms,
            "response": response,
            "classify_error": classify_err,
            "error": None,
        }
    except Exception as e:
        return {
            "model_id": spec.id,
            "task_id": task["id"],
            "category": task["category"],
            "sample_idx": sample_idx,
            "language": "error",
            "elapsed_ms": int((time.time() - t0) * 1000),
            "response": None,
            "classify_error": None,
            "error": f"{type(e).__name__}: {e}",
        }


def _plan(
    models: list[ModelSpec],
    tasks: list[dict],
    samples: int,
    done: set[tuple[str, str, int]],
) -> list[tuple[ModelSpec, dict, int]]:
    todo = []
    for spec in models:
        for task in tasks:
            for i in range(samples):
                if (spec.id, task["id"], i) in done:
                    continue
                todo.append((spec, task, i))
    return todo


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--samples", type=int, default=5, help="samples per (model, task)")
    p.add_argument("--models", type=str, default="", help="comma-separated model ids; empty = all")
    p.add_argument("--tasks", type=str, default="", help="comma-separated task ids; empty = all")
    p.add_argument("--concurrency", type=int, default=4, help="parallel in-flight calls")
    p.add_argument("--models-yaml", type=str, default=str(ROOT / "models.yaml"))
    p.add_argument("--tasks-yaml", type=str, default=str(ROOT / "tasks.yaml"))
    p.add_argument("--results", type=str, default=str(RESULTS_PATH))
    args = p.parse_args(argv)

    all_models = load_models(args.models_yaml)
    all_tasks = _load_tasks(Path(args.tasks_yaml))

    if args.models:
        wanted = set(args.models.split(","))
        all_models = [m for m in all_models if m.id in wanted]
        missing = wanted - {m.id for m in all_models}
        if missing:
            print(f"warning: unknown model ids: {sorted(missing)}", file=sys.stderr)
    if args.tasks:
        wanted = set(args.tasks.split(","))
        all_tasks = [t for t in all_tasks if t["id"] in wanted]
        missing = wanted - {t["id"] for t in all_tasks}
        if missing:
            print(f"warning: unknown task ids: {sorted(missing)}", file=sys.stderr)

    results_path = Path(args.results)
    done = _load_done(results_path)
    todo = _plan(all_models, all_tasks, args.samples, done)

    total = len(all_models) * len(all_tasks) * args.samples
    print(
        f"plan: {len(all_models)} models × {len(all_tasks)} tasks × {args.samples} samples "
        f"= {total} total; {len(done)} already done; {len(todo)} to run",
        file=sys.stderr,
    )
    if not todo:
        print("nothing to do.", file=sys.stderr)
        return 0

    lock = threading.Lock()
    completed = 0
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = {
            ex.submit(_run_one, spec, task, i): (spec.id, task["id"], i)
            for (spec, task, i) in todo
        }
        for fut in as_completed(futures):
            row = fut.result()
            _append_jsonl(results_path, row, lock)
            completed += 1
            status = row["language"] if not row["error"] else f"ERROR {row['error'][:60]}"
            print(
                f"[{completed}/{len(todo)}] {row['model_id']:24s} "
                f"{row['task_id']:24s} #{row['sample_idx']} -> {status}",
                file=sys.stderr,
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
