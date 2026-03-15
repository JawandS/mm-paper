# Thesis Direction (Concise)

## Working Title
**Do Embedding-Based Clusters Recover CIP Academic Areas?**

## Core Question
How well do embedding-based clusters of majors align with **human labeling by CIP areas**?

## Goal
- If we can recover meaningful latent groupings from program text, this approach can support institutions whose local programs do not map cleanly to baseline CIP categories.
- A strong result would show not only CIP alignment, but also potentially more meaningful cross-cutting clusters than CIP alone.

## Motivation
- CIP codes are often treated as ground truth in education/program research.
- We want a more data-driven view of program content from text representations.
- This thesis tests whether embedding-based structure recovers, refines, or departs from CIP structure.

## Literature Gap
- Existing work uses topic models, behavioral predictors, or domain-specific matching.
- To our knowledge, no prior study directly compares modern embedding-based program representations against CIP as the main benchmark.

## Closest Work / Competition
- Haas, Graf & Arslan (2025): topic modeling on course descriptions for program recommendation; comparable goal, but LDA-style topics and no CIP comparison.
- Josiam, Ryan & Sridhar (2025): sentence embeddings + cosine similarity for Engineering Education PhD programs vs job postings; methodologically close, but domain-specific alignment and not CIP-based.
- Stein et al. (2020): nearest-neighbor major recommendation from historical enrollment behavior; supervised behavioral method, no text embeddings.
- Zayed et al. (2022): random-forest major prediction from grades/demographics; high accuracy but dependent on student performance data, not text-based preference structure.
- Mohanty / EduEmbedd (2023): knowledge-graph embeddings for courses; relevant precedent, but course-level and not directly comparable at program+CIP level.

## Data
- Raw CIP taxonomy (`CIPCode2020.csv`): `CIPTitle` and `CIPDefinition` as input text.
- 2-digit CIP area as the ground truth label.
- Top 12 CIP areas by program count (~1,100 programs after filtering stubs, residencies, and apprenticeships).

## Method (Simple)
1. Generate embeddings for all majors.
2. Run unsupervised clustering (e.g., k-means / spherical k-means).
3. Compare cluster assignments to CIP-area labels.
4. Repeat across seeds (and optionally multiple embedding models).

## Metrics
- Adjusted Rand Index (ARI)
- Normalized Mutual Information (NMI)
- Cluster purity / majority-label accuracy
- Silhouette score (internal validity — identifies geometrically natural k independently of labels)
- Stability across random seeds

## Expected Contribution
- Show where embedding geometry matches CIP structure well (coarse academic structure).
- Show where it diverges (cross-disciplinary majors, subjective boundaries).
- Provide evidence for a portable, data-driven grouping method that can complement or improve on CIP-only organization.

## Scope Guardrails
- Primary ground truth: CIP areas (2-digit family).
- Input text: raw CIP descriptions only — no LLM enrichment, no external data sources.
- MajorMatch application context: motivational background only, not part of the research evaluation.
