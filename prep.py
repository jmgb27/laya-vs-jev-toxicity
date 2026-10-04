"""Build the Civil Comments train/test files with human vote fractions as soft targets.

Each output line is one comment in the Laya/Jev shape:
  {"id", "state", "questions": {7 noul questions}, "gold": {q: {"probabilities": {"true": f, "false": 1-f}}}}
where f is the fraction of human raters who said yes. Train comes from the official train
split, test from the official test split, so nothing leaks between them.

Usage: python prep.py [--train 20000] [--test 2000] [--seed 13]
"""

import argparse
import hashlib
import json
import os
import random
import urllib.request

import pyarrow.parquet as pq

BASE = "https://huggingface.co/api/datasets/google/civil_comments/parquet/default"
FILES = {"train": ["train/0.parquet", "train/1.parquet"], "test": ["test/0.parquet"]}

# Wording follows the Jigsaw annotation guidelines for each attribute.
QUESTIONS = {
    "toxicity": "Is this comment toxic: rude, disrespectful or unreasonable enough to make someone leave a discussion?",
    "severe_toxicity": "Is this comment severely toxic: very hateful, aggressive or disrespectful?",
    "obscene": "Does this comment contain swear words, curse words or other obscene or profane language?",
    "threat": "Does this comment describe an intention to inflict pain, injury or violence against a person or group?",
    "insult": "Is this comment an insulting, inflammatory or negative comment towards a person or group?",
    "identity_attack": "Does this comment attack or demean someone because of their identity (race, religion, gender, sexuality, disability)?",
    "sexual_explicit": "Does this comment contain references to sexual acts, body parts or other lewd content?",
}
QS = {k: {"type": "noul", "instructions": v} for k, v in QUESTIONS.items()}

# Strata on the toxicity vote share, sampled equally so toxic and split-vote comments are not
# drowned out by the ~92% of comments nobody flagged.
# ponytail: equal strata skew prevalence vs the natural distribution; score.py reports per stratum.
BUCKETS = [(0.0, 0.0), (1e-9, 0.2), (0.2, 0.5), (0.5, 1.0)]


def bucket(t):
    for i, (lo, hi) in enumerate(BUCKETS):
        if lo <= t <= hi:
            return i
    return len(BUCKETS) - 1


def load(split, cache="data"):
    os.makedirs(cache, exist_ok=True)
    tables = []
    for f in FILES[split]:
        path = os.path.join(cache, f.replace("/", "_"))
        if not os.path.exists(path):
            urllib.request.urlretrieve(f"{BASE}/{f}", path)
        tables.append(pq.read_table(path, columns=["text", *QUESTIONS]).to_pylist())
    return [r for t in tables for r in t]


def sample(rows, n, rng, split):
    by_bucket = [[] for _ in BUCKETS]
    for i, r in enumerate(rows):
        if r["text"] and r["text"].strip():
            by_bucket[bucket(r["toxicity"])].append(i)
    per = n // len(BUCKETS)
    picked = []
    for b in by_bucket:
        picked += rng.sample(b, min(per, len(b)))
    rng.shuffle(picked)
    return [
        {
            "id": f"{split}-{i}",
            "state": rows[i]["text"],
            "questions": QS,
            "gold": {q: {"probabilities": {"true": float(rows[i][q]), "false": 1.0 - float(rows[i][q])}} for q in QUESTIONS},
        }
        for i in picked
    ]


def write(cases, path):
    with open(path, "w", encoding="utf-8") as f:
        for c in cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", type=int, default=20000)
    ap.add_argument("--test", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=13)
    a = ap.parse_args()
    for split, n in (("train", a.train), ("test", a.test)):
        cases = sample(load(split), n, random.Random(a.seed), split)
        digest = write(cases, f"{split}.jsonl")
        print(f"{split}.jsonl: {len(cases)} comments, sha256 {digest}")


if __name__ == "__main__":
    main()
