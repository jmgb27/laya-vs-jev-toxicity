"""Mix AG News choice questions into the Civil Comments training file (replay against forgetting).

  python replay.py [--n 14000]   # writes train_replay.jsonl

The noul-only fine-tune broke choice questions (AG News 0.948 -> 0.037). AG News was already in
Laya's training mix, so replaying its train split adds no new task; DAIR Emotion stays held out
as the clean check that the fix generalises. 14k items is ~10% of the 140k Civil Comments items.
"""

import argparse
import json
import random

from forget import AG_CRIT, rows, HF

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=14000)
ap.add_argument("--seed", type=int, default=13)
a = ap.parse_args()

labels = list(AG_CRIT)
q = {"topic": {"type": "choice", "instructions": "What is the topic of `article`?", "criteria": AG_CRIT}}
ag = random.Random(a.seed).sample(rows(f"{HF}/fancyzhx/ag_news/parquet/default/train/0.parquet", "data/ag_news_train.parquet"), a.n)
cases = [json.loads(line) for line in open("train.jsonl", encoding="utf-8")]
cases += [{"id": f"ag-{i}", "state": {"article": r["text"]}, "questions": q,
           "gold": {"topic": {"probabilities": {l: float(l == labels[r["label"]]) for l in labels}}}}
          for i, r in enumerate(ag)]
random.Random(a.seed).shuffle(cases)
with open("train_replay.jsonl", "w", encoding="utf-8") as f:
    for c in cases:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
print(f"train_replay.jsonl: {len(cases)} cases ({a.n} AG News replay)")
