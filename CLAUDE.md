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
| `thesis/Content/04_MajorMatch.tex` | Dimensionality Analysis | Variance explained by elicited dimensions; LLM-assigned scores as third benchmark |
| `thesis/Content/05_Conclusion.tex` | Conclusion | Summary of findings, limitations, practical implications, future work |

**Abstract:** `thesis/abstract.tex` — write last, after all chapter content is finalized.

**Sections 03 and 04 internal structure:** Challenge/Gap → Implementation → Benefits

**A figure showing how MajorMatch works should appear somewhere in the thesis.**

---

## Audience

An undergraduate honors committee in computer science. Assume technical literacy but not specialist familiarity with NLP or recommender systems. All non-obvious concepts should be explained on first use.

---

## Hard Constraints

- No IRB-collected user data is available; do not imply otherwise
- Avoid em-dashes entirely
- Do not reproduce the core matching algorithm in detail

---

## Writing Style

**Voice and person:** First person, used freely. Write as the author of a technical undergraduate report, not as a journal submission. Sound like a student describing their own work.

**Tone:** Exploratory and discursive. Build arguments methodically rather than announcing conclusions upfront. Analytical sections should read: context, method, result, implication.

**Sentence length:** Prefer simple, direct sentences. Break compound-complex constructions into separate sentences. A sequence of short, clear sentences reads better than one long clause-heavy sentence. Vary rhythm but default to simple.

**Concision:** Include only the context that's directly necessary. Establish the minimum background needed to make a point, then move on. Do not elaborate institutional implications or enumerate adjacent problems beyond what the thesis directly needs.

**Perspective:** Frame the problem from the student's point of view when both student and institutional perspectives are available. Institutional consequences (administrative costs, transfer rates) are secondary context.

**Technical concepts:** Explain everything a non-specialist reader would need. Use concrete analogies before formal definitions. Inline figure and table references are preferred over forward references.

**Transitions:** Simple connectives ("However," "Therefore,") work fine as sentence starters when they move the argument forward. Analytical sections build step by step; the introduction and conclusion can move more freely.

**Limitations:** Address proportionally to their significance. Do not bury or over-hedge.

**Implications:** Frame practically. Connect findings to what they mean for the research question and for applications like MajorMatch.

**Formatting:**
- No em-dashes (use commas, parentheses, or restructure the sentence)
- Avoid typical AI writing patterns: do not open sentences with "Notably," "Importantly," "It is worth noting," or similar throat-clearing phrases
- Prefer active constructions
- Avoid filler qualifiers ("quite," "rather," "somewhat")

---

## Key Terminology

| Term | Meaning in this project |
|---|---|
| CIP codes | Classification of Instructional Programs — a federal taxonomy of academic programs maintained by NCES |
| Embedding | A dense vector representation of a text string produced by a language model |
| Cosine similarity | A distance metric used to compare embedding vectors; the basis of MajorMatch's matching logic |
| ARI / NMI / Purity | Clustering quality metrics comparing recovered clusters to ground-truth CIP groupings |
| Spherical k-means | K-means variant that uses cosine similarity rather than Euclidean distance |
| LLM dimension scores | Scores assigned by a large language model on author-defined dimensions (e.g., quantitative intensity, social orientation); used as a third benchmark in Section 04 |

---

## What to Avoid

- Reproducing core matching algorithm details (IP concern)
- Claiming user study results without IRB data
- Presenting MajorMatch as the thesis subject rather than the motivating application
- Em-dashes
- Generic AI preamble phrases
