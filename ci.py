"""Paired bootstrap 95% intervals for the headline differences between two prediction files.

  python ci.py preds_laya_ft.jsonl preds_jev.jsonl [--n 2000]

Resamples the same comments for both models each round, so the interval is on the difference.
"""

import json
import sys

import numpy as np

from score import auroc

SPLIT = (0.3, 0.7)


def load(path):
    with open(path, encoding="utf-8") as f:
        p = {r["id"]: r["p"] for r in map(json.loads, f) if "p" in r}
    return p


def headline(P, F, attrs):
    """P, F: (n, attrs) arrays of model probability and rater fraction."""
    pear = [np.corrcoef(P[:, j], F[:, j])[0, 1] for j in range(len(attrs)) if P[:, j].std() and F[:, j].std()]
    aucs = [auroc((F[:, j] >= 0.5).astype(int), P[:, j]) for j in range(len(attrs))]
    t = attrs.index("toxicity")
    s = (F[:, t] >= SPLIT[0]) & (F[:, t] <= SPLIT[1])
    return {
        "macro pearson": float(np.mean(pear)),
        "macro auroc": float(np.nanmean(aucs)),
        "macro mae": float(abs(P - F).mean()),
        "toxicity pearson": float(np.corrcoef(P[:, t], F[:, t])[0, 1]),
        "split-vote mae": float(abs(P[s, t] - F[s, t]).mean()),
    }


def main():
    a_path, b_path = sys.argv[1], sys.argv[2]
    n_boot = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 2000
    with open("test.jsonl", encoding="utf-8") as f:
        gold = {c["id"]: {q: g["probabilities"]["true"] for q, g in c["gold"].items()} for c in map(json.loads, f)}
    attrs = list(next(iter(gold.values())))
    a, b = load(a_path), load(b_path)
    ids = [i for i in gold if i in a and i in b]
    F = np.array([[gold[i][q] for q in attrs] for i in ids])
    A = np.array([[a[i][q] for q in attrs] for i in ids])
    B = np.array([[b[i][q] for q in attrs] for i in ids])

    point_a, point_b = headline(A, F, attrs), headline(B, F, attrs)
    rng = np.random.default_rng(13)
    diffs = {k: [] for k in point_a}
    for _ in range(n_boot):
        idx = rng.integers(0, len(ids), len(ids))
        ha, hb = headline(A[idx], F[idx], attrs), headline(B[idx], F[idx], attrs)
        for k in diffs:
            diffs[k].append(ha[k] - hb[k])

    print(f"\n{a_path} minus {b_path}  (n={len(ids)}, {n_boot} paired bootstrap rounds)")
    print("| metric | A | B | A - B | 95% CI |\n|---|---|---|---|---|")
    for k, d in diffs.items():
        lo, hi = np.nanpercentile(d, [2.5, 97.5])
        print(f"| {k} | {point_a[k]:.3f} | {point_b[k]:.3f} | {point_a[k] - point_b[k]:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")


if __name__ == "__main__":
    main()
