"""Plain-language metric: how often each model makes the same yes/no call as most raters.

  python majority.py            # wording 1 (test.jsonl questions)
  python majority.py --w2       # the second question wording

A model "matches" a label when (P >= cut-off) equals (rater share >= 0.5), so an exact 50/50 rater split counts as yes. Reports the default 0.5
cut-off per question and for all 7 at once, a per-label cut-off (0 to 1 in steps of 0.01, or never yes) tuned on one half of the test
comments and scored on the other half (two-fold, averaged), paired bootstrap intervals, and a rough
estimate for a natural mix of comments (the four equal toxicity groups reweighted to the full test split).
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
    FILES["Trial fine-tune (1,000 comments, 1 epoch)"] = "preds_laya_smoke.jsonl"
    FILES["Laya, fine-tuned (final)"] = "preds_laya_replay.jsonl"
gold = {c["id"]: {q: g["probabilities"]["true"] for q, g in c["gold"].items()} for c in map(json.loads, open("test.jsonl"))}
Q = list(next(iter(gold.values())))
ids = sorted(gold)
F = np.array([[gold[i][q] >= 0.5 for q in Q] for i in ids])
half = np.zeros(len(ids), bool)
half[random.Random(13).sample(range(len(ids)), len(ids) // 2)] = True
# 1.01 means "never yes". A 0.05-0.95 grid capped Jev, whose best cut-offs sit at the top (fixed 2026-10-09).
grid = np.append(np.round(np.arange(0, 1.0001, 0.01), 2), 1.01)


def tuned(P, fit, test):
    out = np.zeros((test.sum(), len(Q)), bool)
    for j in range(len(Q)):
        best = max(grid, key=lambda t: ((P[fit, j] >= t) == F[fit, j]).mean())
        out[:, j] = (P[test, j] >= best) == F[test, j]
    return out


M, T = {}, {}
print("| model | " + " | ".join(Q) + " | all 7 | all 7, tuned |\n|" + "---|" * (len(Q) + 3))
for name, f in FILES.items():
    r = {x["id"]: x["p"] for x in map(json.loads, open(f))}
    P = np.array([[r[i][q] for q in Q] for i in ids])
    m = (P >= 0.5) == F
    M[name] = m.all(1)
    t = np.vstack([tuned(P, half, ~half), tuned(P, ~half, half)])
    T[name] = t.all(1)  # rows are fold 2's test half, then fold 1's, so paired across models
    print(f"| {name} | " + " | ".join(f"{m[:, j].mean():.1%}" for j in range(len(Q))) + f" | {m.all(1).mean():.1%} | {t.all(1).mean():.1%} |")

rng = np.random.default_rng(13)
names = list(M)
for label, X in [("all 7", M), ("all 7, tuned", T)]:
    for a, b in [(names[-1], "Jev"), ("Laya, as shipped", "Jev"), (names[-1], "Laya, as shipped"), ("Jev", "Always says fine")]:
        d = [X[a][idx].mean() - X[b][idx].mean() for idx in (rng.integers(0, len(ids), len(ids)) for _ in range(2000))]
        lo, hi = np.percentile(d, [2.5, 97.5])
        print(f"{label}, {a} minus {b}: {X[a].mean() - X[b].mean():+.3f} [{lo:+.3f}, {hi:+.3f}]")

# The test set samples four toxicity groups equally (prep.py). Reweight them to their shares of the
# whole Civil Comments test split (numbers.md) for a rough natural-mix estimate.
# ponytail: tuned cut-offs were fitted on the balanced mix, so the tuned estimate is pessimistic.
GROUPS = [(0.0, 0.0), (1e-9, 0.2), (0.2, 0.5), (0.5, 1.0)]
SHARE = np.array([0.702, 0.090, 0.128, 0.080])
tox = {c["id"]: c["gold"]["toxicity"]["probabilities"]["true"] for c in map(json.loads, open("test.jsonl"))}
g = np.array([next(k for k, (lo, hi) in enumerate(GROUPS) if lo <= tox[i] <= hi) for i in ids])
gt = np.concatenate([g[~half], g[half]])  # row order of T
print("\nnatural mix (rough):")
for name in M:
    face = sum(SHARE[k] * M[name][g == k].mean() for k in range(4))
    tun = sum(SHARE[k] * T[name][gt == k].mean() for k in range(4))
    print(f"{name}: {face:.1%} at face value, {tun:.1%} tuned")
