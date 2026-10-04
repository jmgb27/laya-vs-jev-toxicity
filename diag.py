import collections, laya, pyarrow.parquet as pq
from forget import AG_CRIT, top
ag = pq.read_table("data/ag_news_test.parquet").to_pylist()[:200]
labels = list(AG_CRIT)
q = {"topic": {"type": "choice", "instructions": "What is the topic of `article`?", "criteria": AG_CRIT}}
for m in ["convaiinnovations/laya", "out/laya_civil"]:
    a = laya.load(m, device="cuda")
    pred, conf = collections.Counter(), collections.Counter()
    ok = 0
    for r in ag:
        ans = a.predict({"article": r["text"]}, q)["answers"]["topic"]
        p = top(ans); pred[p] += 1; conf[(labels[r["label"]], p)] += 1; ok += p == labels[r["label"]]
    print(m, "acc", ok / len(ag), "predicted", dict(pred))
    print("  top confusions", conf.most_common(6))
    print("  example probs", ans["probabilities"], "gold", labels[ag[-1]["label"]])
