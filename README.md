# Laya vs Jev on toxicity

These are the scripts, test comments and every model's answers behind this blog post:

**[Laya vs Jev on toxicity: 83% vs 27% agreement with raters after fine-tuning](https://johnmark.dev/blog/laya-vs-jev-toxicity-fine-tune)**

I asked two decision models the same seven yes/no questions about 2,000 [Civil Comments](https://huggingface.co/datasets/google/civil_comments): TypeSafe's paid Jev API and [Laya](https://github.com/NandhaKishorM/laya), an open model. Then I fine-tuned Laya for about two hours on one RTX 4090. The table shows how often each model gave the same yes/no as most human raters on all seven questions:

| | All 7 questions, answers at face value | All 7, cut-off tuned |
|---|---|---|
| A judge that always says "fine" | 71% | 71% |
| Jev 1.13 (OpenRouter) | 27% | 68% |
| Laya, out of the box | 61% | 79% |
| Laya, fine-tuned | 83% | 81% |

The first fine-tune used yes/no questions only, and it broke multiple-choice answers (AG News topics fell from 95% to 4%). Mixing AG News questions into a second run brought them back to 94%. The post has the whole story and its caveats.

## Files

| File | What it is |
|---|---|
| `prep.py` | Builds `train.jsonl` (20,000 comments) and `test.jsonl` (2,000) from Civil Comments, with the raters' share as soft targets |
| `replay.py` | Mixes 14,000 AG News questions into the training file (the fix for the forgetting) |
| `predict.py` | Answers the test set with Laya (local) or Jev (OpenRouter), one line per comment |
| `score.py` | Agreement with the raters: correlation, Brier, AUROC, the split-vote slice and latency |
| `majority.py` | The plain-language headline metric: same yes/no as most raters, at face value and with tuned cut-offs |
| `ci.py` | Paired bootstrap 95% intervals between two models |
| `forget.py` | The forgetting check: AG News, DAIR Emotion and typed-decisions accuracy |
| `slots.py`, `diag.py` | The checks that the broken checkpoint wasn't stuck on an option position |
| `charts.py` | The post's charts |
| `test.jsonl`, `test_w2.jsonl` | The 2,000 test comments with both question wordings, and the raters' shares |
| `preds_*.jsonl` | Every model's answer to every test comment, including Jev's |
| `results.md`, `numbers.md` | The score tables and every number quoted in the post |

## Reproduce

You need Python 3.12 and, for training, a CUDA GPU (I used a 24 GB RTX 4090).

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv -r requirements.txt
.venv/bin/python prep.py                         # downloads Civil Comments, writes train/test
.venv/bin/python predict.py laya --device cuda --out preds_laya_base.jsonl
```

For fine-tuning I used Laya's own script, unmodified (download it into this folder): [`research/scripts/finetune_single_device.py`](https://github.com/NandhaKishorM/laya/blob/main/research/scripts/finetune_single_device.py). Point it at the English checkpoint (`huggingface_hub.snapshot_download("convaiinnovations/laya")`) and run 2 epochs:

```bash
.venv/bin/python replay.py                       # writes train_replay.jsonl
.venv/bin/python finetune_single_device.py --data train_replay.jsonl \
    --model-dir <snapshot> --output-dir out/laya_civil_replay --device cuda --epochs 2
.venv/bin/python predict.py laya --model out/laya_civil_replay --device cuda --out preds_laya_replay.jsonl
```

For Jev, put an OpenRouter key in `OPENROUTER_API_KEY`. All 2,000 comments cost me about 4 cents.

```bash
.venv/bin/python predict.py jev --out preds_jev.jsonl
```

Then score:

```bash
.venv/bin/python score.py preds_laya_base.jsonl preds_laya_replay.jsonl preds_jev.jsonl
.venv/bin/python majority.py
.venv/bin/python ci.py preds_laya_replay.jsonl preds_jev.jsonl
.venv/bin/python forget.py convaiinnovations/laya out/laya_civil_replay
```

## License

The code is MIT. Civil Comments is CC0. The `preds_jev*.jsonl` files are Jev's answers as returned by its API.
