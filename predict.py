"""Answer test.jsonl with Laya or Jev and write one prediction line per comment.

  python predict.py laya --model convaiinnovations/laya --out preds_laya_base.jsonl
  python predict.py laya --model out/laya_civil --out preds_laya_ft.jsonl
  OPENROUTER_API_KEY=... python predict.py jev --out preds_jev.jsonl   # OpenRouter System One API

Both backends get the identical {state, questions} body. Resumable: ids already in --out are skipped.
"""

import argparse
import json
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor


def load_done(path):
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return {json.loads(line)["id"] for line in f}


def noul_probs(answers):
    return {q: float(a["noul"]) for q, a in answers.items()}


def run_laya(cases, args, out):
    import laya

    agent = laya.load(args.model, device=args.device)
    for c in cases:
        t = time.perf_counter()
        r = agent.predict(c["state"], c["questions"])
        ms = (time.perf_counter() - t) * 1000
        out({"id": c["id"], "p": noul_probs(r["answers"]), "latency_ms": ms})


def run_jev(cases, args, out):
    headers = {"content-type": "application/json", "authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}

    def call(c):
        body = json.dumps({"model": args.jev_model, "state": c["state"], "questions": c["questions"]}).encode()
        for attempt in range(4):
            try:
                t = time.perf_counter()
                with urllib.request.urlopen(urllib.request.Request(args.url, body, headers), timeout=60) as resp:
                    o = json.load(resp)
                ms = (time.perf_counter() - t) * 1000
                usage = o.get("usage") or {}
                return {"id": c["id"], "p": noul_probs(o["answers"]), "latency_ms": ms, "model": o.get("model"),
                        "input_tokens": usage.get("input_tokens"), "cost": usage.get("cost")}
            except Exception as e:  # noqa: BLE001 - retry any transport or 5xx failure
                err = e
                time.sleep(2 ** attempt)
        return {"id": c["id"], "error": str(err)}

    with ThreadPoolExecutor(args.workers) as pool:
        for row in pool.map(call, cases):
            out(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backend", choices=["laya", "jev"])
    ap.add_argument("--data", default="test.jsonl")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="convaiinnovations/laya")
    ap.add_argument("--device", default=None)
    ap.add_argument("--url", default="https://openrouter.ai/api/v1/systemone")
    ap.add_argument("--jev-model", default="typesafe/jev-1.13")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    done = load_done(args.out)
    with open(args.data, encoding="utf-8") as f:
        cases = [c for c in map(json.loads, f) if c["id"] not in done][: args.limit]
    print(f"{len(cases)} to answer ({len(done)} already done)")

    with open(args.out, "a", encoding="utf-8") as f:
        def out(row):
            f.write(json.dumps(row) + "\n")
            f.flush()
        (run_laya if args.backend == "laya" else run_jev)(cases, args, out)


if __name__ == "__main__":
    main()
