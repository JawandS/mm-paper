# CLAUDE.md

This file provides guidance to Claude Code when working in this repository. The Python pipeline is complete and static. The active work is writing the thesis.

---

## Where Things Live

```
thesis/             # LaTeX write-up (compiled via Overleaf)
  Content/                  # Chapter .tex files
  Reference/thesis.bib      # All cited references
  reference_papers/         # PDF and .md versions of cited papers
data/               # Pipeline outputs — source of truth for all results
  clean_majors.csv          # 1,264 programs across 23 CIP areas
  embeddings.json           # OpenAI text-embedding-3-small vectors, keyed by CIPCode
  results/unsupervised/     # Clustering metrics and summaries
  results/supervised/       # Classification metrics and summaries
```

---

## Research Summary

**Core question:** Does embedding geometry spontaneously recover human-defined conceptual structure in academic programs?

The analysis validates embeddings against three independent benchmarks:

1. **CIP codes** (government administrative taxonomy) — unsupervised clustering recovers area structure. Spherical k-means (k=23, cosine similarity, 100 seeds) with three initialization strategies (random, stratified, cip_mean). Metrics: ARI, NMI, purity. Results in `data/results/unsupervised/`.

2. **Qualitative major clusterings** (author-defined groupings) — embeddings respect author-perceived conceptual groupings.

3. **LLM-assigned dimension scores** — a large language model scores each program on author-defined dimensions (e.g., quantitative intensity, social orientation); variance explained by a small number of elicited dimensions. Results in `data/results/supervised/`.

The supervised benchmark (logistic regression, SVM-RBF, MLP; 5-fold stratified CV; accuracy, balanced accuracy, macro F1) separately establishes how well embeddings support classification. Results in `data/results/supervised/`.

**MajorMatch's role:** MajorMatch (majormatch.me) is the motivating application, not the thesis subject. It provides practical stakes for the research question. Minimize exposure of matching system internals.

---

## Thesis Structure

| File | Section | Content |
|---|---|---|
| `thesis/Content/01_Introduction.tex` | Introduction | Motivation, research questions, section overview, MajorMatch as applied context |
| `thesis/Content/02_RelatedWork.tex` | Related Work | Major/program recommendation systems; embedding-based classification; interpretability in recommender systems |
| `thesis/Content/03_Embeddings.tex` | Embedding Structure | CIP code comparison — establishes embeddings as a valid representation of academic program structure |
| `thesis/Content/04_MajorMatch.tex` | MajorMatch Pipeline | How clustering-derived groupings serve as stage 1 of the MajorMatch matching pipeline; connects Chapter 3's validation to a concrete downstream use |
| `thesis/Content/05_Conclusion.tex` | Conclusion | Summary of findings, limitations, practical implications, future work |

**Abstract:** `thesis/abstract.tex` — write last, after all chapter content is finalized.

**Sections 03 and 04 internal structure:** Problem → Method → Results → Implications

**A figure showing how MajorMatch works should appear somewhere in the thesis.**

---

## Audience

An undergraduate honors committee in computer science. Assume technical literacy but not specialist familiarity with NLP or recommender systems. All non-obvious concepts should be explained on first use.

---

## Hard Constraints

- No IRB-collected user data -- do not imply otherwise
- No em-dashes
- Do not reproduce the core matching algorithm in detail
- Do not present MajorMatch as the thesis subject -- it is the motivating application

---

## Writing Style

**Voice:** First person for methodological actions only ("I compare," "I set," "I use"). Not for background, context, or prior work results.

**Tone:** Direct and confident. State claims without hedging ("might suggest," "appears to," "could potentially indicate" are off-limits). Build arguments step by step; each step is asserted. Frame from the student's perspective.

**Limitations:** State the limitation once, where it arises. Immediately follow with what the result still establishes despite it. Do not save limitations for the conclusion. Do not over-hedge by restating them.

**Section openings:** Open each analytical section with the research question that section answers. Do not describe what the section will do ("This section presents..."). State the problem or question directly, then address it.

**Paragraphs:** One point per paragraph. The opening sentence states the claim. Supporting sentences explain the mechanism or evidence. If removing a sentence does not weaken the argument, remove it.

**Sentences:** Default to simple and direct. Break compound-complex constructions apart. For mechanistic explanations, use one sentence per step.

**Results writing:** Lead with the number, then interpret. "Random initialization achieves ARI=0.424, well above the chance baseline of 0" -- not "The chance baseline is 0, and random initialization achieves ARI=0.424." Interpretation follows assertion; mechanism follows claim.

**Concision:** Include only what's directly necessary. Establish minimum background, then move on. Do not elaborate institutional implications or enumerate adjacent problems beyond what the thesis needs. Do not announce what you are about to analyze ("Two patterns warrant attention," "There are several things to note") -- just analyze it.

**Numbers:** Spell out small counts (one through nine); use numerals for 10 and above ("two programs," "65 participants"). Percent signs with numerals ("98\%").

**Related work:** Each entry: what the paper does → key result with numbers → one sentence naming what it demonstrates for this thesis ("This result demonstrates..., motivating this thesis' work with...").

**Technical explanations:** Concrete analogy or example before the formal definition. Then one sentence per step.

**Verbs:** Active and precise. Prefer "demonstrates," "establishes," "addresses," "motivates," "recovers," "outperforms" over "shows" or "indicates." Passive is acceptable for methodology ("k is set to 23") but not for results or claims.

**Formatting:**
- No throat-clearing openers: "Notably," "Importantly," "It is worth noting"
- No filler qualifiers: "quite," "rather," "somewhat"
- No topic-burying openers: "There are many ways to..." or "It is the case that..."
- No meta-commentary: do not announce what you are about to say or flag that something is interesting before saying it
- Transitions ("However," "Therefore," "Furthermore") are fine as sentence starters when they advance the argument
