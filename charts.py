"""Render the blog post's SVG charts and diagrams.

  OUT=charts python charts.py   # default folder: ./charts

Numbers are copied from results.md (score.py / ci.py / forget.py output) so the charts match the post.
"""

import os
from html import escape

OUT = os.path.expanduser(os.environ.get("OUT", "charts"))
os.makedirs(OUT, exist_ok=True)
W, H = 1200, 627
BG, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
OLD, NEW, GREY, JEV = "#eb6834", "#2a78d6", "#8a8984", "#4a3aa7"
FONT = "-apple-system, 'Helvetica Neue', Arial, sans-serif"


def text(x, y, s, size=15, fill=INK, anchor="start", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>'


def bar(x0, y, w, h, fill):
    # rounded data end only, anchored to the baseline
    if w < 5:
        return f'<rect x="{x0}" y="{y}" width="{max(w, 1):.1f}" height="{h}" fill="{fill}"/>'
    return f'<path d="M{x0} {y} H{x0 + w - 4:.1f} a4 4 0 0 1 4 4 V{y + h - 4} a4 4 0 0 1 -4 4 H{x0} Z" fill="{fill}"/>'


def svg(name, title, desc, subtitle, body, notes=()):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" role="img" aria-labelledby="t d">',
        f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        text(40, 52, title, 26, weight=600),
        text(40, 82, subtitle, 16, MUTED),
        *body,
        *[text(40, H - 35 + 22 * i - 22 * (len(notes) - 1), n, 14, MUTED) for i, n in enumerate(notes)],
        "</svg>",
    ]
    with open(os.path.join(OUT, name), "w") as f:
        f.write("\n".join(parts) + "\n")


def legend(items, y=116):
    out, x = [], 40
    for label, color in items:
        out += [f'<rect x="{x}" y="{y}" width="14" height="14" rx="3" fill="{color}"/>', text(x + 22, y + 12, label)]
        x += 30 + len(label) * 8.2
    return out


def hbars(groups, series, vmax, ticks, fmt, x0=400, x1=1100, top=150, bottom=500, ref=None, sublabels=None):
    """groups: [label]; series: [(name, color or [color per group], [values per group])]. Values labelled on every bar."""
    scale = (x1 - x0) / vmax
    out = []
    for t in ticks:
        x = x0 + t * scale
        out += [f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" stroke="{GRID}"/>', text(x, bottom + 24, fmt(t), 14, MUTED, "middle")]
    if ref:
        x = x0 + ref[0] * scale
        out += [f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" stroke="{ref[2]}" stroke-width="2" stroke-dasharray="6 5"/>',
                text(x + 8, top + 14, ref[1], 14, MUTED)]
    band = (bottom - top) / len(groups)
    bh = min(26, (band - 18) / len(series) - 2)
    for gi, g in enumerate(groups):
        gy = top + gi * band + (band - len(series) * (bh + 2)) / 2
        out.append(text(x0 - 16, gy + len(series) * (bh + 2) / 2 + 5 - (8 if sublabels else 0), g, 17, anchor="end", weight=600))
        if sublabels:
            out.append(text(x0 - 16, gy + len(series) * (bh + 2) / 2 + 15, sublabels[gi], 14, MUTED, "end"))
        for si, (_, color, vals) in enumerate(series):
            y, w = gy + si * (bh + 2), vals[gi] * scale
            label = fmt(vals[gi])
            out += [bar(x0, y, w, bh, color[gi] if isinstance(color, list) else color),
                    f'<rect x="{x0 + w + 4:.1f}" y="{y + bh / 2 - 10:.1f}" width="{len(label) * 9 + 8}" height="20" fill="{BG}"/>',
                    text(x0 + w + 8, y + bh / 2 + 5, label, 15)]
    return out


def box(x, y, w, h, lines, fill="#ffffff", stroke=GRID, size=18):
    """h=None sizes the box to its lines. First line is the bold heading."""
    lh = size + 10
    h = h or 24 + lh * len(lines)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>']
    for i, ln in enumerate(lines):
        out.append(text(x + 18, y + 12 + lh * (i + 1) - 4, ln, size + 2 if i == 0 else size, INK if i == 0 else MUTED, weight=600 if i == 0 else 400))
    return out


def arrow(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2 - 10}" y2="{y2}" stroke="{MUTED}" stroke-width="2"/>'
            f'<path d="M{x2} {y2} l-12 -6 v12 Z" fill="{MUTED}"/>')


two = lambda v: f"{v:.2f}"

# 1. Headline: plain-language majority match
pct = lambda v: f"{v:.0%}"
svg("laya-headline.svg",
    "How often each AI made the same call as most people",
    "Share of 2,000 test comments where the model's yes/no answer matched the majority of human raters on all 7 labels, taking each answer at face value: Jev 27%, Laya out of the box 61%, Laya fine-tuned 83%. A judge that always says 'fine' would score 71%.",
    "All 7 labels matched the raters' majority. Answers taken at face value (yes = 50% or more).",
    legend([("Jev 1.13 (API)", JEV), ("Laya, out of the box", OLD), ("Laya, fine-tuned", NEW)]) +
    hbars(["Jev 1.13", "Laya, out of the box", "Laya, fine-tuned"], [("", [JEV, OLD, NEW], [0.266, 0.613, 0.832])], 1.0,
          [0, 0.25, 0.5, 0.75, 1.0], pct, ref=(0.712, "always says \u201cfine\u201d: 71%", GREY),
          sublabels=["closed API", "free, open model", "+ 2 hours on one RTX 4090"]),
    ("2,000 Civil Comments, balanced across clean, borderline and toxic. Fine-tuned on 20k comments + 14k AG News questions.",
     "Fine-tuned minus Jev: +57 points, 95% bootstrap interval +54 to +59."))

# 1b. Tuned cut-offs
def tint(c, a=0.45):
    r, g, b = (int(c[k:k + 2], 16) for k in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(round(v + (255 - v) * a) for v in (r, g, b))

svg("laya-tuned.svg",
    "Even with each model's cut-off tuned",
    "All 7 labels matching the raters' majority, at face value versus with a per-label cut-off tuned on half the comments and scored on the other half: Jev 27% to 68%, Laya out of the box 61% to 79%, Laya fine-tuned 83% to 81%. Always saying 'fine' scores 71%.",
    "All 7 labels matched. Dark = face value (50%). Light = cut-off tuned per label on the other half of the comments.",
    hbars(["Jev 1.13", "Laya, out of the box", "Laya, fine-tuned"],
          [("face value", [JEV, OLD, NEW], [0.266, 0.613, 0.832]),
           ("tuned", [tint(JEV), tint(OLD), tint(NEW)], [0.675, 0.790, 0.810])], 1.0,
          [0, 0.25, 0.5, 0.75, 1.0], pct, top=120, ref=(0.712, "always says \u201cfine\u201d: 71%", GREY)),
    ("Tuning: for each label, pick the cut-off that matches most raters on 1,000 comments, score on the other 1,000, then swap and average.",))

# 2. Per label
labels = ["toxicity", "severe toxicity", "obscene", "threat", "insult", "identity attack", "sexual explicit"]
jev = [0.540, 0.247, 0.636, 0.527, 0.463, 0.505, 0.527]
base = [0.799, 0.315, 0.486, 0.483, 0.770, 0.260, 0.481]
ft = [0.823, 0.437, 0.828, 0.709, 0.836, 0.751, 0.810]
svg("laya-labels.svg",
    "For the stats-minded: correlation, label by label",
    "Pearson correlation with the share of raters per label. Jev / Laya out of the box / Laya fine-tuned: toxicity 0.54/0.80/0.82, severe toxicity 0.25/0.32/0.44, obscene 0.64/0.49/0.83, threat 0.53/0.48/0.71, insult 0.46/0.77/0.84, identity attack 0.51/0.26/0.75, sexual explicit 0.53/0.48/0.81.",
    "Correlation with the share of raters who said yes. 0 = no agreement, 1 = perfect. 2,000 test comments.",
    legend([("Jev 1.13", JEV), ("Laya, out of the box", OLD), ("Laya, fine-tuned", NEW)]) +
    hbars(labels, [("Jev", JEV, jev), ("base", OLD, base), ("ft", NEW, ft)], 1.0, [0, 0.25, 0.5, 0.75, 1.0], two,
          x0=230, top=150, bottom=530),
    ("Laya out of the box leads Jev on toxicity, severe toxicity and insult; Jev leads on the other four until Laya is fine-tuned.",))

# 3. Split votes: who over-flags
svg("laya-split.svg",
    "Comments people disagreed about",
    "On 594 test comments where 30 to 70% of raters said toxic, the share each model called toxic: Jev 71%, Laya out of the box 30%, Laya fine-tuned 44%. On 61% of these comments most raters said toxic.",
    "Share of 594 split comments each model called toxic. Dashed line: share where most raters said toxic.",
    legend([("Jev 1.13", JEV), ("Laya, out of the box", OLD), ("Laya, fine-tuned", NEW)]) +
    hbars(["Jev 1.13", "Laya, out of the box", "Laya, fine-tuned"], [("", [JEV, OLD, NEW], [0.709, 0.305, 0.444])], 1.0,
          [0, 0.25, 0.5, 0.75, 1.0], pct, ref=(0.614, "most raters said toxic: 61%", MUTED),
          sublabels=["flags too many", "flags too few", "closer, still too few"]),
    ("Split comments: 30\u201370% of the comment's raters said toxic.",))

# 4. Latency
svg("laya-latency.svg",
    "Time to answer all 7 questions about one comment",
    "Median time per comment for 7 yes/no questions: Laya 30 ms on a local RTX 4090, Jev 274 ms through the OpenRouter API, one request at a time, 100 requests.",
    "Median per comment, 7 questions per request. Not the same conditions: local GPU vs a network API.",
    hbars(["Laya, RTX 4090", "Jev via OpenRouter"], [("", [NEW, JEV], [30, 274])], 300, [0, 100, 200, 300],
          lambda v: f"{v:.0f} ms", top=130, bottom=500, sublabels=["local, 2,000 comments", "network round trip, 100 requests"]),
    ("Jev's time includes the network round trip from my home connection; Laya's includes no network. Neither was tuned for speed.",))

# 5. Forgetting
svg("laya-forgetting.svg",
    "The first fine-tune forgot how to do multiple choice",
    "Accuracy on 600 AG News and 600 DAIR Emotion test items. Laya out of the box: 0.95 and 0.57. Fine-tuned on yes/no questions only: 0.04 and 0.07. Fine-tuned with AG News mixed in: 0.94 and 0.37. Random guessing: 0.25 and 0.17.",
    "Share answered correctly, 600 questions each. Grey = first try (replaced). Guessing: AG News 25%, Emotion 17%.",
    legend([("Laya, out of the box", OLD), ("First try: yes/no only", GREY), ("Second try: + AG News", NEW)]) +
    hbars(["AG News topics", "Emotion"], [("base", OLD, [0.948, 0.573]), ("noul", GREY, [0.037, 0.070]), ("replay", NEW, [0.937, 0.368])],
          1.0, [0, 0.25, 0.5, 0.75, 1.0], pct, x0=300, top=160, bottom=500,
          sublabels=["news topics, 4 choices", "6 emotions, never practised"]),
    ("Grey: trained on yes/no questions only. Blue: the same plus 14k AG News multiple-choice items. Typed-decisions: 0.36 / 0.36 / 0.34 (random 0.32).",))

# 6. How the test works
svg("laya-how.svg",
    "One comment, seven questions, one pass",
    "Diagram: a comment and seven yes/no questions go to the model in one request; it returns seven probabilities, each turned into yes or no and compared with what most raters said. During fine-tuning the raters' share itself is the training target.",
    "Illustration. The same request body goes to Laya and to Jev.",
    [*box(40, 120, 330, None, ["A comment", "“You are an absolute idiot", "and everyone here knows it.”"]),
     *box(40, 290, 330, None, ["7 yes/no questions", "toxicity · severe toxicity", "obscene · threat · insult", "identity attack", "sexual explicit"]),
     arrow(380, 300, 450, 300),
     *box(460, 245, 270, None, ["Laya or Jev", "one request", "(Laya: one pass, 30 ms)"]),
     arrow(740, 300, 810, 300),
     *box(820, 120, 340, None, ["7 probabilities", "toxicity 0.97", "insult 0.95", "threat 0.03 …"]),
     *box(820, 300, 340, None, ["Compared with most raters", "toxic: 9 of 10 said yes \u2192 yes", "threat: 0 of 10 said yes \u2192 no", "fine-tuning practises on the", "share itself (0.9, 0.0)"], fill="#f4f8fd", stroke=NEW)],
    ("Civil Comments records, for each comment and label, the share of its human raters who said yes. Numbers here are illustrative.",))

# 7. The catch
svg("laya-catch.svg",
    "Why it forgot: our best guess",
    "Diagram, labelled hypothesis: Laya scores every answer option with one shared component. Yes/no questions always offer the same two options in the same order, so two epochs over 140,000 yes/no items never forced 'the option that matches the text wins'. On multiple choice the yes/no-only checkpoint picked a wrong option; in 200 AG News articles, sports was most often answered as world and world as sports.",
    "Illustration of a hypothesis, not a measured mechanism.",
    [*box(40, 120, 350, None, ["One shared scorer", "rates every answer option", "for every question type:", "choice, score and yes/no"]),
     *box(425, 120, 350, None, ["Yes/no questions", "always the same two options", "in the same order, so either", "convention fits them"], fill="#fdf6f2", stroke=OLD),
     *box(810, 120, 350, None, ["Multiple choice", "needs “the option that", "matches the text wins”.", "Nothing held that in place."]),
     *box(40, 330, 540, None, ["Before: AG News 95%", "“Giants win the pennant” → sports", "picks the option that matches best"], fill="#fdf6f2", stroke=OLD),
     *box(620, 330, 540, None, ["After 2 epochs of yes/no only: 4%", "“Giants win the pennant” → world", "picks a wrong option,", "whatever order the options are in"], fill="#f4f6f8", stroke=GREY)],
    ("Example headline is illustrative; sports articles were most often answered as world. Reversed option order: still 3.5% of 200.",))

# 8. Decision
svg("laya-decision.svg",
    "Should you fine-tune Laya instead of calling Jev?",
    "Checklist. Use it when: you have labelled examples of your own decisions, you can run a GPU, you mostly ask one kind of question, and you will re-test your other questions after every fine-tune. Skip it when: you need many unrelated question types from one checkpoint, you have no labels, or you need more than about 20 options in one question.",
    "Checklist, from 2,000 test comments and three forgetting tests.",
    [*box(40, 120, 540, None, ["Use it when", "✓ you have labelled examples of your decisions", "   (rater shares work as training targets)", "✓ you can run a GPU for a few hours", "✓ one checkpoint serves one kind of question", "✓ you re-test your other questions after", "   every fine-tune, before you ship", "✓ you want 30 ms answers and no per-call bill"], fill="#f4f8fd", stroke=NEW, size=22),
     *box(620, 120, 540, None, ["Skip it when", "✗ one checkpoint must answer many unrelated", "   question types (mix varied data back in,", "   or keep the shipped checkpoint for those)", "✗ you have no labelled examples", "✗ a question needs more than ~20 options", "   (Laya's documented limit)", "✗ you can't host a GPU model"], fill="#fdf6f2", stroke=OLD, size=22)],
    ("Based on one run per arm: 2,000 Civil Comments test comments; 600-item AG News and Emotion tests; 2,000 typed-decisions.",))

print("wrote", sorted(f for f in os.listdir(OUT) if f.startswith("laya-")))
