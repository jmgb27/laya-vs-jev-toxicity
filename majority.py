"""Plain-language metric: how often each model makes the same yes/no call as most raters.

  python majority.py            # wording 1 (test.jsonl questions)
  python majority.py --w2       # the second question wording

A model "matches" a label when (P >= cut-off) equals (rater share >= 0.5). Reports the default 0.5
cut-off per question and for all 7 at once, a per-label cut-off tuned on one half of the test
comments and scored on the other half (two-fold, averaged), and paired bootstrap intervals.
"""

import json
import random
import sys

import numpy as np

W2 = "--w2" in sys.argv
FILES = {"Always says fine": "preds_constant.jsonl",
         "Jev": "preds_jev_w2.jsonl" if W2 else "preds_jev.jsonl",
         "Laya, as shipped": "preds_laya_base_w2.jsonl" if W2 else "preds_laya_base.jsonl",
         "First fine-tune (toxicity only)": "preds_laya_ft_w2.jsonl" if W2 else "preds_laya_ft.jsonl"}
if not W2:
    FILES["Laya, fine-tuned (final)"] = "preds_laya_replay.jsonl"
gold = {c["id"]: {q: g["probabilities"]["true"] for q, g in c["gold"].items()} for c in map(json.loads, open("test.jsonl"))}
Q = list(next(iter(gold.values())))
ids = sorted(gold)
F = np.array([[gold[i][q] >= 0.5 for q in Q] for i in ids])
half = np.zeros(len(ids), bool)
half[random.Random(13).sample(range(len(ids)), len(ids) // 2)] = True
grid = np.round(np.arange(0.05, 1.0, 0.05), 2)


def tuned(P, fit, test):
    out = np.zeros((test.sum(), len(Q)), bool)
    for j in range(len(Q)):
        best = max(grid, key=lambda t: ((P[fit, j] >= t) == F[fit, j]).mean())
        out[:, j] = (P[test, j] >= best) == F[test, j]
    return out


M = {}
print("| model | " + " | ".join(Q) + " | all 7 | all 7, tuned |\n|" + "---|" * (len(Q) + 3))
for name, f in FILES.items():
    r = {x["id"]: x["p"] for x in map(json.loads, open(f))}
    P = np.array([[r[i][q] for q in Q] for i in ids])
    m = (P >= 0.5) == F
    M[name] = m.all(1)
    t = np.vstack([tuned(P, half, ~half), tuned(P, ~half, half)])
    print(f"| {name} | " + " | ".join(f"{m[:, j].mean():.1%}" for j in range(len(Q))) + f" | {m.all(1).mean():.1%} | {t.all(1).mean():.1%} |")

rng = np.random.default_rng(13)
names = list(M)
for a, b in [(names[-1], "Jev"), ("Laya, as shipped", "Jev"), (names[-1], "Laya, as shipped")]:
    d = [M[a][idx].mean() - M[b][idx].mean() for idx in (rng.integers(0, len(ids), len(ids)) for _ in range(2000))]
    lo, hi = np.percentile(d, [2.5, 97.5])
    print(f"all 7, {a} minus {b}: {M[a].mean() - M[b].mean():+.3f} [{lo:+.3f}, {hi:+.3f}]")
