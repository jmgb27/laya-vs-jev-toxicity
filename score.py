"""Score prediction files against the human vote fractions in test.jsonl.

  python score.py preds_laya_base.jsonl preds_laya_ft.jsonl preds_jev.jsonl

Per model: agreement with the rater fraction (Brier, MAE, Pearson, Spearman, calibration error),
classification at the 0.5 majority line (AUROC, F1), the toxicity split-vote slice (0.3-0.7),
and latency. All comments a model failed to answer are reported, not silently dropped.
"""

import json
import sys

import numpy as np

SPLIT = (0.3, 0.7)


def ranks(x):
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    r[order] = np.arange(len(x))
    # average ties so Spearman and AUROC are exact
    _, inv, counts = np.unique(x, return_inverse=True, return_counts=True)
    sums = np.bincount(inv, weights=r)
    return sums[inv] / counts[inv]


def auroc(y, p):
    pos, n_pos = y.astype(bool), int(y.sum())
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    return float((ranks(p)[pos].sum() - n_pos * (n_pos - 1) / 2) / (n_pos * n_neg))


def calib_error(p, f, bins=10):
    idx = np.minimum((p * bins).astype(int), bins - 1)
    return float(sum(abs(p[idx == b].mean() - f[idx == b].mean()) * (idx == b).mean() for b in range(bins) if (idx == b).any()))


def metrics(p, f):
    y = (f >= 0.5).astype(int)
    yhat = (p >= 0.5).astype(int)
    tp = int((y & yhat).sum())
    f1 = 2 * tp / max(1, y.sum() + yhat.sum())
    corr = lambda a, b: float(np.corrcoef(a, b)[0, 1]) if a.std() and b.std() else float("nan")
    return {
        "brier": float(((p - f) ** 2).mean()),
        "mae": float(abs(p - f).mean()),
        "pearson": corr(p, f),
        "spearman": corr(ranks(p), ranks(f)),
        "calib_err": calib_error(p, f),
        "auroc": auroc(y, p),
        "f1@0.5": f1,
    }


def main():
    with open("test.jsonl", encoding="utf-8") as fh:
        gold = {c["id"]: {q: g["probabilities"]["true"] for q, g in c["gold"].items()} for c in map(json.loads, fh)}
    attrs = list(next(iter(gold.values())))

    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as fh:
            rows = [json.loads(line) for line in fh]
        ok = [r for r in rows if "p" in r and r["id"] in gold]
        print(f"\n## {path}  answered {len(ok)}/{len(gold)}, errors {len(rows) - len(ok)}")
        print("| attribute | brier | mae | pearson | spearman | calib_err | auroc | f1@0.5 |\n|---|---|---|---|---|---|---|---|")
        macro = []
        for q in attrs:
            p = np.array([r["p"][q] for r in ok])
            f = np.array([gold[r["id"]][q] for r in ok])
            m = metrics(p, f)
            macro.append(m)
            print(f"| {q} | " + " | ".join(f"{v:.3f}" for v in m.values()) + " |")
        print("| **macro** | " + " | ".join(f"{np.nanmean([m[k] for m in macro]):.3f}" for k in macro[0]) + " |")

        p = np.array([r["p"]["toxicity"] for r in ok])
        f = np.array([gold[r["id"]]["toxicity"] for r in ok])
        s = (f >= SPLIT[0]) & (f <= SPLIT[1])
        print(f"\nsplit-vote toxicity slice (n={int(s.sum())}): mae {abs(p[s] - f[s]).mean():.3f}, "
              f"brier {((p[s] - f[s]) ** 2).mean():.3f}, mean p {p[s].mean():.3f} vs mean votes {f[s].mean():.3f}")
        lat = np.array([r["latency_ms"] for r in ok])
        print(f"latency per comment (7 questions): p50 {np.percentile(lat, 50):.0f} ms, p95 {np.percentile(lat, 95):.0f} ms")


def _selfcheck():
    y = np.array([0, 0, 1, 1])
    assert auroc(y, np.array([0.1, 0.2, 0.8, 0.9])) == 1.0
    assert auroc(y, np.array([0.9, 0.8, 0.2, 0.1])) == 0.0
    assert auroc(y, np.array([0.5, 0.5, 0.5, 0.5])) == 0.5
    f = np.array([0.0, 0.3, 0.6, 1.0])
    m = metrics(f.copy(), f)
    assert m["brier"] == 0 and m["calib_err"] < 1e-9 and abs(m["spearman"] - 1) < 1e-9


if __name__ == "__main__":
    _selfcheck()
    main()
