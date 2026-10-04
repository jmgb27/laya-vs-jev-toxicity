"""Forgetting check: did the Civil Comments fine-tune hurt Laya on tasks it already did?

  python forget.py convaiinnovations/laya out/laya_civil

AG News (in Laya's training mix) and DAIR Emotion (held out), first 600 test rows each with the
same questions as Laya's own T4 benchmark, plus the full typed-decisions test split (400 cases,
2,000 decisions). Accuracy = argmax answer vs gold label.
"""

import json
import os
import sys
import urllib.request

import laya
import pyarrow.parquet as pq

HF = "https://huggingface.co/api/datasets"
AG_CRIT = {"world": "world news and international politics", "sports": "sports",
           "business": "business and economy", "sci_tech": "science and technology"}
EMOTIONS = ["sadness", "joy", "love", "anger", "fear", "surprise"]


def rows(url, path):
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    return pq.read_table(path).to_pylist()


def top(answer):
    if answer["type"] == "noul":
        return "true" if answer["noul"] >= 0.5 else "false"
    probs = answer["probabilities"]
    return max(probs, key=probs.get)


def main():
    os.makedirs("data", exist_ok=True)
    ag = rows(f"{HF}/fancyzhx/ag_news/parquet/default/test/0.parquet", "data/ag_news_test.parquet")[:600]
    emo = rows(f"{HF}/dair-ai/emotion/parquet/split/test/0.parquet", "data/emotion_test.parquet")[:600]
    td = rows(f"{HF}/LocalLLaMA/typed-decisions/parquet/all/test/0.parquet", "data/typed_decisions_test.parquet")
    ag_q = {"topic": {"type": "choice", "instructions": "What is the topic of `article`?", "criteria": AG_CRIT}}
    emo_q = {"emotion": {"type": "choice", "instructions": "Which emotion is most strongly expressed in `text`?",
                         "criteria": {n: None for n in EMOTIONS}}}
    labels = list(AG_CRIT)

    for model in sys.argv[1:]:
        agent = laya.load(model, device="cuda")
        ag_ok = sum(top(agent.predict({"article": r["text"]}, ag_q)["answers"]["topic"]) == labels[r["label"]] for r in ag)
        emo_ok = sum(top(agent.predict({"text": r["text"]}, emo_q)["answers"]["emotion"]) == EMOTIONS[r["label"]] for r in emo)
        td_ok = td_n = 0
        for r in td:
            qs, gold = json.loads(r["questions"]), json.loads(r["gold"])
            ans = agent.predict(r["state"], qs)["answers"]
            for q in qs:
                td_n += 1
                td_ok += top(ans[q]) == str(gold[q]["label"])
        print(f"{model}: ag_news {ag_ok / len(ag):.3f} | emotion {emo_ok / len(emo):.3f} | typed-decisions {td_ok / td_n:.3f} (n={td_n})", flush=True)


if __name__ == "__main__":
    main()
