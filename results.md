
## preds_constant.jsonl  answered 2000/2000, errors 0
| attribute | brier | mae | pearson | spearman | calib_err | auroc | f1@0.5 |
|---|---|---|---|---|---|---|---|
| toxicity | 0.076 | 0.235 | 0.000 | nan | 0.001 | 0.500 | 0.000 |
| severe_toxicity | 0.001 | 0.022 | 0.000 | nan | 0.001 | nan | 0.000 |
| obscene | 0.015 | 0.071 | -0.000 | nan | 0.000 | 0.500 | 0.000 |
| threat | 0.006 | 0.040 | 0.000 | nan | 0.001 | 0.500 | 0.000 |
| insult | 0.072 | 0.221 | -0.000 | nan | 0.001 | 0.500 | 0.000 |
| identity_attack | 0.013 | 0.079 | -0.000 | nan | 0.007 | 0.500 | 0.000 |
| sexual_explicit | 0.006 | 0.031 | nan | nan | 0.002 | 0.500 | 0.000 |
| **macro** | 0.027 | 0.100 | 0.000 | nan | 0.002 | 0.500 | 0.000 |

split-vote toxicity slice (n=594): mae 0.211, brier 0.063, mean p 0.296 vs mean votes 0.507
latency per comment (7 questions): p50 0 ms, p95 0 ms

## preds_laya_base.jsonl  answered 2000/2000, errors 0
| attribute | brier | mae | pearson | spearman | calib_err | auroc | f1@0.5 |
|---|---|---|---|---|---|---|---|
| toxicity | 0.032 | 0.148 | 0.799 | 0.785 | 0.076 | 0.939 | 0.688 |
| severe_toxicity | 0.122 | 0.308 | 0.315 | 0.465 | 0.307 | nan | 0.000 |
| obscene | 0.051 | 0.174 | 0.486 | 0.515 | 0.160 | 0.902 | 0.240 |
| threat | 0.047 | 0.162 | 0.483 | 0.360 | 0.157 | 0.950 | 0.161 |
| insult | 0.049 | 0.179 | 0.770 | 0.761 | 0.140 | 0.927 | 0.735 |
| identity_attack | 0.040 | 0.161 | 0.260 | 0.344 | 0.135 | 0.798 | 0.108 |
| sexual_explicit | 0.037 | 0.144 | 0.481 | 0.262 | 0.140 | 0.922 | 0.215 |
| **macro** | 0.054 | 0.182 | 0.513 | 0.499 | 0.159 | 0.906 | 0.307 |

split-vote toxicity slice (n=594): mae 0.108, brier 0.019, mean p 0.445 vs mean votes 0.507
latency per comment (7 questions): p50 30 ms, p95 32 ms

## preds_laya_ft.jsonl  answered 2000/2000, errors 0
| attribute | brier | mae | pearson | spearman | calib_err | auroc | f1@0.5 |
|---|---|---|---|---|---|---|---|
| toxicity | 0.024 | 0.112 | 0.829 | 0.793 | 0.020 | 0.942 | 0.764 |
| severe_toxicity | 0.001 | 0.014 | 0.422 | 0.466 | 0.001 | nan | 0.000 |
| obscene | 0.005 | 0.030 | 0.820 | 0.572 | 0.009 | 0.983 | 0.629 |
| threat | 0.003 | 0.021 | 0.709 | 0.412 | 0.007 | 0.946 | 0.417 |
| insult | 0.021 | 0.100 | 0.840 | 0.787 | 0.023 | 0.944 | 0.752 |
| identity_attack | 0.006 | 0.041 | 0.750 | 0.558 | 0.011 | 0.973 | 0.302 |
| sexual_explicit | 0.002 | 0.013 | 0.782 | 0.365 | 0.004 | 0.992 | 0.385 |
| **macro** | 0.009 | 0.047 | 0.736 | 0.565 | 0.011 | 0.963 | 0.464 |

split-vote toxicity slice (n=594): mae 0.128, brier 0.027, mean p 0.440 vs mean votes 0.507
latency per comment (7 questions): p50 31 ms, p95 33 ms

## preds_laya_replay.jsonl  answered 2000/2000, errors 0
| attribute | brier | mae | pearson | spearman | calib_err | auroc | f1@0.5 |
|---|---|---|---|---|---|---|---|
| toxicity | 0.025 | 0.115 | 0.823 | 0.791 | 0.024 | 0.941 | 0.750 |
| severe_toxicity | 0.001 | 0.015 | 0.437 | 0.469 | 0.000 | nan | 0.000 |
| obscene | 0.005 | 0.031 | 0.828 | 0.573 | 0.011 | 0.988 | 0.641 |
| threat | 0.003 | 0.021 | 0.709 | 0.415 | 0.005 | 0.963 | 0.364 |
| insult | 0.022 | 0.103 | 0.836 | 0.788 | 0.028 | 0.944 | 0.748 |
| identity_attack | 0.006 | 0.041 | 0.751 | 0.549 | 0.011 | 0.982 | 0.533 |
| sexual_explicit | 0.002 | 0.013 | 0.810 | 0.368 | 0.001 | 0.994 | 0.400 |
| **macro** | 0.009 | 0.049 | 0.742 | 0.565 | 0.012 | 0.969 | 0.491 |

split-vote toxicity slice (n=594): mae 0.127, brier 0.027, mean p 0.446 vs mean votes 0.507
latency per comment (7 questions): p50 30 ms, p95 31 ms

## preds_jev.jsonl  answered 2000/2000, errors 0
| attribute | brier | mae | pearson | spearman | calib_err | auroc | f1@0.5 |
|---|---|---|---|---|---|---|---|
| toxicity | 0.107 | 0.259 | 0.540 | 0.554 | 0.192 | 0.797 | 0.582 |
| severe_toxicity | 0.188 | 0.340 | 0.247 | 0.346 | 0.338 | nan | 0.000 |
| obscene | 0.031 | 0.096 | 0.636 | 0.474 | 0.078 | 0.966 | 0.411 |
| threat | 0.020 | 0.081 | 0.527 | 0.358 | 0.069 | 0.963 | 0.259 |
| insult | 0.295 | 0.466 | 0.463 | 0.570 | 0.452 | 0.802 | 0.440 |
| identity_attack | 0.032 | 0.108 | 0.505 | 0.401 | 0.080 | 0.930 | 0.257 |
| sexual_explicit | 0.027 | 0.075 | 0.527 | 0.305 | 0.067 | 0.956 | 0.230 |
| **macro** | 0.100 | 0.203 | 0.492 | 0.429 | 0.182 | 0.902 | 0.311 |

split-vote toxicity slice (n=594): mae 0.223, brier 0.071, mean p 0.629 vs mean votes 0.507
latency per comment (7 questions): p50 355 ms, p95 732 ms

## Forgetting check (accuracy)

| model | AG News | DAIR Emotion (held out) | typed-decisions |
|---|---|---|---|
| base | 0.948 | 0.573 | 0.360 |
| smoke (1k comments, 1 epoch) | 0.945 | 0.582 | 0.356 |
| noul-only (20k, 2 epochs) | 0.037 | 0.070 | 0.357 |
| + AG News replay | 0.937 | 0.368 | 0.336 |
