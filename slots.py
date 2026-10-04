import collections, laya, pyarrow.parquet as pq
from forget import AG_CRIT, EMOTIONS, top
ag = pq.read_table("data/ag_news_test.parquet").to_pylist()[:200]
emo = pq.read_table("data/emotion_test.parquet").to_pylist()[:200]
labels = list(AG_CRIT)
a = laya.load("out/laya_civil", device="cuda")
for name, order in [("original", labels), ("reversed", labels[::-1])]:
    q = {"topic": {"type": "choice", "instructions": "What is the topic of `article`?", "criteria": {k: AG_CRIT[k] for k in order}}}
    slot, ok = collections.Counter(), 0
    for r in ag:
        p = top(a.predict({"article": r["text"]}, q)["answers"]["topic"])
        slot[order.index(p)] += 1; ok += p == labels[r["label"]]
    print(f"AG {name} order {order}: acc {ok/len(ag):.3f}, picks by slot {dict(sorted(slot.items()))}")
q = {"emotion": {"type": "choice", "instructions": "Which emotion is most strongly expressed in `text`?", "criteria": {n: None for n in EMOTIONS}}}
slot, gold_slot = collections.Counter(), collections.Counter()
for r in emo:
    slot[EMOTIONS.index(top(a.predict({"text": r["text"]}, q)["answers"]["emotion"]))] += 1; gold_slot[r["label"]] += 1
print(f"Emotion picks by slot {dict(sorted(slot.items()))} | gold by slot {dict(sorted(gold_slot.items()))}")
