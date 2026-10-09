# Supporting numbers for the blog post (generated 2026-10-04)

## Paired bootstrap CIs (ci.py; replay = final fine-tuned checkpoint, ft = yes/no-only)

preds_laya_replay.jsonl minus preds_jev.jsonl  (n=2000, 2000 paired bootstrap rounds)
| metric | A | B | A - B | 95% CI |
|---|---|---|---|---|
| macro pearson | 0.742 | 0.492 | +0.250 | [+0.226, +0.273] |
| macro auroc | 0.969 | 0.902 | +0.066 | [+0.049, +0.082] |
| macro mae | 0.049 | 0.203 | -0.155 | [-0.160, -0.150] |
| toxicity pearson | 0.823 | 0.540 | +0.283 | [+0.252, +0.314] |
| split-vote mae | 0.127 | 0.223 | -0.096 | [-0.111, -0.081] |

preds_laya_replay.jsonl minus preds_laya_base.jsonl  (n=2000, 2000 paired bootstrap rounds)
| metric | A | B | A - B | 95% CI |
|---|---|---|---|---|
| macro pearson | 0.742 | 0.513 | +0.228 | [+0.209, +0.247] |
| macro auroc | 0.969 | 0.906 | +0.063 | [+0.043, +0.082] |
| macro mae | 0.049 | 0.182 | -0.134 | [-0.137, -0.130] |
| toxicity pearson | 0.823 | 0.799 | +0.024 | [+0.013, +0.035] |
| split-vote mae | 0.127 | 0.108 | +0.019 | [+0.013, +0.026] |

preds_laya_base.jsonl minus preds_jev.jsonl  (n=2000, 2000 paired bootstrap rounds)
| metric | A | B | A - B | 95% CI |
|---|---|---|---|---|
| macro pearson | 0.513 | 0.492 | +0.021 | [+0.002, +0.042] |
| macro auroc | 0.906 | 0.902 | +0.004 | [-0.013, +0.020] |
| macro mae | 0.182 | 0.203 | -0.021 | [-0.026, -0.017] |
| toxicity pearson | 0.799 | 0.540 | +0.259 | [+0.232, +0.287] |
| split-vote mae | 0.108 | 0.223 | -0.115 | [-0.128, -0.100] |

preds_laya_ft.jsonl minus preds_jev.jsonl  (n=2000, 2000 paired bootstrap rounds)
| metric | A | B | A - B | 95% CI |
|---|---|---|---|---|
| macro pearson | 0.736 | 0.492 | +0.244 | [+0.218, +0.269] |
| macro auroc | 0.963 | 0.902 | +0.061 | [+0.037, +0.079] |
| macro mae | 0.047 | 0.203 | -0.156 | [-0.161, -0.152] |
| toxicity pearson | 0.829 | 0.540 | +0.289 | [+0.260, +0.320] |
| split-vote mae | 0.128 | 0.223 | -0.095 | [-0.110, -0.080] |

## Second question wording (test_w2.jsonl; ft = yes/no-only checkpoint)

## preds_laya_base_w2.jsonl  answered 2000/2000, errors 0
| attribute | brier | mae | pearson | spearman | calib_err | auroc | f1@0.5 |
|---|---|---|---|---|---|---|---|
| toxicity | 0.029 | 0.133 | 0.796 | 0.782 | 0.050 | 0.937 | 0.756 |
| severe_toxicity | 0.124 | 0.295 | 0.311 | 0.451 | 0.294 | nan | 0.000 |
| obscene | 0.073 | 0.204 | 0.452 | 0.516 | 0.192 | 0.897 | 0.170 |
| threat | 0.058 | 0.192 | 0.528 | 0.378 | 0.189 | 0.934 | 0.158 |
| insult | 0.027 | 0.134 | 0.825 | 0.787 | 0.075 | 0.946 | 0.734 |
| identity_attack | 0.031 | 0.140 | 0.362 | 0.371 | 0.116 | 0.858 | 0.200 |
| sexual_explicit | 0.043 | 0.140 | 0.435 | 0.267 | 0.135 | 0.875 | 0.181 |
| **macro** | 0.055 | 0.177 | 0.530 | 0.507 | 0.150 | 0.908 | 0.314 |

split-vote toxicity slice (n=594): mae 0.111, brier 0.020, mean p 0.462 vs mean votes 0.507
latency per comment (7 questions): p50 29 ms, p95 30 ms

## preds_laya_ft_w2.jsonl  answered 2000/2000, errors 0
| attribute | brier | mae | pearson | spearman | calib_err | auroc | f1@0.5 |
|---|---|---|---|---|---|---|---|
| toxicity | 0.025 | 0.112 | 0.823 | 0.788 | 0.034 | 0.938 | 0.739 |
| severe_toxicity | 0.001 | 0.016 | 0.420 | 0.459 | 0.003 | nan | 0.000 |
| obscene | 0.006 | 0.040 | 0.801 | 0.564 | 0.016 | 0.981 | 0.725 |
| threat | 0.004 | 0.025 | 0.696 | 0.405 | 0.008 | 0.952 | 0.414 |
| insult | 0.022 | 0.103 | 0.837 | 0.788 | 0.035 | 0.942 | 0.762 |
| identity_attack | 0.006 | 0.041 | 0.748 | 0.556 | 0.010 | 0.974 | 0.302 |
| sexual_explicit | 0.003 | 0.017 | 0.777 | 0.368 | 0.005 | 0.991 | 0.471 |
| **macro** | 0.010 | 0.051 | 0.729 | 0.561 | 0.016 | 0.963 | 0.488 |

split-vote toxicity slice (n=594): mae 0.145, brier 0.034, mean p 0.412 vs mean votes 0.507
latency per comment (7 questions): p50 30 ms, p95 32 ms

## preds_jev_w2.jsonl  answered 2000/2000, errors 0
| attribute | brier | mae | pearson | spearman | calib_err | auroc | f1@0.5 |
|---|---|---|---|---|---|---|---|
| toxicity | 0.083 | 0.225 | 0.540 | 0.547 | 0.132 | 0.790 | 0.596 |
| severe_toxicity | 0.099 | 0.223 | 0.281 | 0.348 | 0.220 | nan | 0.000 |
| obscene | 0.029 | 0.093 | 0.625 | 0.454 | 0.072 | 0.962 | 0.420 |
| threat | 0.007 | 0.041 | 0.555 | 0.359 | 0.019 | 0.969 | 0.318 |
| insult | 0.235 | 0.403 | 0.517 | 0.593 | 0.383 | 0.824 | 0.475 |
| identity_attack | 0.042 | 0.121 | 0.504 | 0.396 | 0.096 | 0.930 | 0.250 |
| sexual_explicit | 0.007 | 0.033 | 0.540 | 0.322 | 0.018 | 0.955 | 0.270 |
| **macro** | 0.072 | 0.163 | 0.509 | 0.431 | 0.134 | 0.905 | 0.333 |

split-vote toxicity slice (n=594): mae 0.201, brier 0.061, mean p 0.557 vs mean votes 0.507
latency per comment (7 questions): p50 474 ms, p95 815 ms

## Train-split memorization check (base Laya on 2,000 train-split comments)
macro pearson 0.517, macro AUROC 0.909, toxicity pearson 0.817 (test split: 0.513 / 0.906 / 0.799)

## Option-order check on yes/no-only checkpoint (slots.py, 200 AG News articles)
original order acc 0.035, reversed order acc 0.035

## Jev cost and latency
preds_jev.jsonl: 2000 requests, $0.0425
preds_jev_w2.jsonl: 2000 requests, $0.0376
preds_jev_latency_seq.jsonl: 100 requests, $0.0021
total $0.0822; sequential latency n=100 p50 274 ms p95 403 ms

## Civil Comments test split (97,320 comments)
toxicity == 0: 70.2%; toxicity < 0.5: 92.0%; mean threat share 0.9%

## Training runs on RTX 4090
yes/no-only: 139,600 items (+400 calibration), 2 epochs, started 16:39, epoch 1 at 17:33, total ~1h45m
replay: 20k comments x7 + 14k AG News = 154k items, 2 epochs, 18:59 to ~20:52
smoke: 1,000 comments, 1 epoch, 2m44s

## AG News confusions, yes/no-only checkpoint (diag.py output, 200 articles, original option order)
predicted counts: world 73, sports 99, sci_tech 17, business 11
top (gold, predicted) pairs: (world, sports) 48, (sci_tech, sports) 36, (sports, world) 34, (sci_tech, world) 20, (business, sports) 14, (business, world) 13
Laya as shipped on the same 200: acc 0.96, top pairs all correct.
Emotion (slots.py, 200 items): picks love 89 times; gold love 15.

## Laya model card (huggingface.co/convaiinnovations/laya, eval/results.md, fetched 2026-10-04)
In-task families include "moderation and safety" (2,708 questions, accuracy 0.967); no dataset names given.

## typed-decisions random baseline
Laya BENCHMARKS.md: random guess 0.318, majority class 0.461.

## Borderline share, Civil Comments test split
20% < toxicity < 50%: 12.8%; 30% to 70%: 12.1%

## Majority match (majority.py): same yes/no call as most raters; cut-off 0.5 unless "tuned"
| model | toxicity | insult | all 7 labels | all 7, tuned cut-off |
|---|---|---|---|---|
| always no | 71.7% | 77.7% | 71.2% | 71.2% |
| Jev | 67.6% | 46.1% | 26.6% | 67.5% |
| Laya as shipped | 85.5% | 86.0% | 61.3% | 79.0% |
| Laya fine-tuned | 87.1% | 89.8% | 83.2% | 81.0% |

Paired bootstrap, all 7 labels at 0.5: fine-tuned minus Jev +0.567 [0.542, 0.591]; shipped minus Jev +0.347 [0.323, 0.371]; fine-tuned minus shipped +0.220 [0.199, 0.239]
Comments where most raters said no to all 7 labels: 71.2%; most raters said toxic: 28.4%
Split-vote slice (594 comments, 30-70% toxic): share called toxic (P>=0.5): Jev 70.9%, shipped 30.5%, fine-tuned 44.4%; share where most raters said toxic 61.4%

## Majority match, full (majority.py, supersedes the table above)
| model | toxicity | severe_toxicity | obscene | threat | insult | identity_attack | sexual_explicit | all 7 | all 7, tuned |
|---|---|---|---|---|---|---|---|---|---|
| Always says fine | 71.7% | 100.0% | 97.8% | 99.2% | 77.7% | 98.0% | 99.0% | 71.2% | 71.2% |
| Jev | 67.6% | 69.6% | 94.5% | 96.9% | 46.1% | 93.7% | 95.3% | 26.6% | 67.5% |
| Laya, as shipped | 85.5% | 82.7% | 90.5% | 93.8% | 86.0% | 95.9% | 95.2% | 61.3% | 79.0% |
| First fine-tune (toxicity only) | 88.0% | 100.0% | 98.7% | 99.3% | 90.1% | 98.2% | 99.2% | 83.8% | 81.0% |
| Laya, fine-tuned (final) | 87.1% | 100.0% | 98.6% | 99.3% | 89.8% | 98.6% | 99.2% | 83.2% | 81.0% |
all 7, Laya, fine-tuned (final) minus Jev: +0.567 [+0.542, +0.591]
all 7, Laya, as shipped minus Jev: +0.347 [+0.323, +0.371]
all 7, Laya, fine-tuned (final) minus Laya, as shipped: +0.220 [+0.199, +0.239]

### Second wording (majority.py --w2)
| model | toxicity | severe_toxicity | obscene | threat | insult | identity_attack | sexual_explicit | all 7 | all 7, tuned |
|---|---|---|---|---|---|---|---|---|---|
| Always says fine | 71.7% | 100.0% | 97.8% | 99.2% | 77.7% | 98.0% | 99.0% | 71.2% | 71.2% |
| Jev | 73.2% | 85.2% | 94.8% | 98.5% | 53.9% | 91.9% | 98.7% | 37.2% | 70.2% |
| Laya, as shipped | 87.5% | 79.8% | 84.9% | 92.5% | 89.8% | 96.8% | 93.7% | 61.6% | 80.0% |
| First fine-tune (toxicity only) | 87.4% | 100.0% | 98.8% | 99.2% | 90.0% | 98.2% | 99.1% | 83.0% | 82.8% |
all 7, First fine-tune (toxicity only) minus Jev: +0.457 [+0.433, +0.481]
all 7, Laya, as shipped minus Jev: +0.243 [+0.216, +0.270]
all 7, First fine-tune (toxicity only) minus Laya, as shipped: +0.214 [+0.195, +0.233]

## Majority match, finer cut-off grid (majority.py, 2026-10-09; supersedes the tuned column above)

The old 0.05-0.95 grid capped Jev, whose best cut-offs sat at 0.95 on 4 of 7 questions. Grid is now 0 to 1 in steps of 0.01 plus "never yes". Face-value (0.5) numbers are unchanged. An exact 50/50 rater split counts as yes: 67 of the 594 split-vote comments are exact ties, so the share where at least half of raters said toxic is 61.4%, or 50.2% if ties count as no.

| model | toxicity | severe_toxicity | obscene | threat | insult | identity_attack | sexual_explicit | all 7 | all 7, tuned |
|---|---|---|---|---|---|---|---|---|---|
| Always says fine | 71.7% | 100.0% | 97.8% | 99.2% | 77.7% | 98.0% | 99.0% | 71.2% | 71.2% |
| Jev | 67.6% | 69.6% | 94.5% | 96.9% | 46.1% | 93.7% | 95.3% | 26.6% | 70.8% |
| Laya, as shipped | 85.5% | 82.7% | 90.5% | 93.8% | 86.0% | 95.9% | 95.2% | 61.3% | 78.5% |
| First fine-tune (toxicity only) | 88.0% | 100.0% | 98.7% | 99.3% | 90.1% | 98.2% | 99.2% | 83.8% | 81.5% |
| Trial fine-tune (1,000 comments, 1 epoch) | 87.0% | 100.0% | 98.0% | 99.2% | 89.1% | 98.1% | 99.2% | 81.0% | 79.8% |
| Laya, fine-tuned (final) | 87.1% | 100.0% | 98.6% | 99.3% | 89.8% | 98.6% | 99.2% | 83.2% | 81.2% |
all 7, Laya, fine-tuned (final) minus Jev: +0.567 [+0.542, +0.591]
all 7, Laya, as shipped minus Jev: +0.347 [+0.323, +0.371]
all 7, Laya, fine-tuned (final) minus Laya, as shipped: +0.220 [+0.199, +0.239]
all 7, Jev minus Always says fine: -0.446 [-0.469, -0.421]
all 7, tuned, Laya, fine-tuned (final) minus Jev: +0.104 [+0.084, +0.124]
all 7, tuned, Laya, as shipped minus Jev: +0.078 [+0.059, +0.097]
all 7, tuned, Laya, fine-tuned (final) minus Laya, as shipped: +0.026 [+0.011, +0.041]
all 7, tuned, Jev minus Always says fine: -0.004 [-0.019, +0.012]

### Second wording (majority.py --w2)

| model | toxicity | severe_toxicity | obscene | threat | insult | identity_attack | sexual_explicit | all 7 | all 7, tuned |
|---|---|---|---|---|---|---|---|---|---|
| Always says fine | 71.7% | 100.0% | 97.8% | 99.2% | 77.7% | 98.0% | 99.0% | 71.2% | 71.2% |
| Jev | 73.2% | 85.2% | 94.8% | 98.5% | 53.9% | 91.9% | 98.7% | 37.2% | 69.8% |
| Laya, as shipped | 87.5% | 79.8% | 84.9% | 92.5% | 89.8% | 96.8% | 93.7% | 61.6% | 79.8% |
| First fine-tune (toxicity only) | 87.4% | 100.0% | 98.8% | 99.2% | 90.0% | 98.2% | 99.1% | 83.0% | 82.5% |
all 7, First fine-tune (toxicity only) minus Jev: +0.457 [+0.433, +0.481]
all 7, Laya, as shipped minus Jev: +0.243 [+0.216, +0.270]
all 7, First fine-tune (toxicity only) minus Laya, as shipped: +0.214 [+0.195, +0.233]
all 7, Jev minus Always says fine: -0.339 [-0.365, -0.314]
all 7, tuned, First fine-tune (toxicity only) minus Jev: +0.128 [+0.108, +0.148]
all 7, tuned, Laya, as shipped minus Jev: +0.100 [+0.081, +0.118]
all 7, tuned, First fine-tune (toxicity only) minus Laya, as shipped: +0.028 [+0.014, +0.042]
all 7, tuned, Jev minus Always says fine: -0.014 [-0.031, +0.004]

### Natural mix, rough (majority.py, 2026-10-09)

Always says fine: 90.0% at face value, 90.0% tuned
Jev: 42.9% at face value, 87.1% tuned
Laya, as shipped: 83.0% at face value, 90.9% tuned
First fine-tune (toxicity only): 93.4% at face value, 92.3% tuned
Trial fine-tune (1,000 comments, 1 epoch): 92.4% at face value, 91.6% tuned
Laya, fine-tuned (final): 93.2% at face value, 91.9% tuned
