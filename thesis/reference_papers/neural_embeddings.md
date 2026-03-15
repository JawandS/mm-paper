# Neural Embeddings of Scholarly Periodicals Reveal Complex Disciplinary Organizations

## Metadata

- **Authors:** Hao Peng, Qing Ke, Ceren Budak, Daniel M. Romero, Yong-Yeol Ahn
- **Year:** 2021
- **Venue:** *Science Advances*, Vol. 7, No. 17
- **DOI:** 10.1126/sciadv.abb9004
- **License:** CC BY-NC 4.0

---

## Abstract (Summary)

The paper proposes a neural embedding method for representing scholarly periodicals (academic journals and conference proceedings) as dense continuous vectors, derived from the citation network between individual papers. The resulting embeddings encode nuanced disciplinary and interdisciplinary relationships between periodicals, support cross-disciplinary vector analogies, and allow quantitative grounding of periodicals along conceptual axes such as the "soft-to-hard sciences" spectrum and the "social-to-biological sciences" spectrum. The authors argue this framework offers a new set of quantitative tools for the science of science.

---

## Introduction

### Background and Motivation

Scholarly periodicals have historically served as the primary organizational units for scientific communication and knowledge production. Beyond being conduits for scientific exchange, they act as repositories organized around topical niches and disciplines. For this reason, they have long been treated as fundamental units in studying the structure and evolution of science.

Previous work moved beyond manual classification by using citation data and metadata to construct similarity matrices or networks, producing algorithmically-derived "maps of science." However, these approaches rely on vector-space representations built from explicit citation connections, which suffer from severe sparsity: using inter-citation or co-citation counts as similarity measures produces matrices where most entries are zero, making meaningful similarity comparisons difficult across many journal pairs. Incorporating indirect relationships requires choosing among many distance metrics and managing very large, dense matrices.

### The Neural Embedding Solution

The authors argue that neural embedding techniques address these problems directly. Neural embeddings produce compact, dense, and continuous vector representations that encode both explicit and implicit relationships between entities. While the underlying vector-space model is decades old, neural network implementations provide flexibility, efficiency, and robustness that have recently produced breakthroughs in natural language processing and beyond. Word embedding models (e.g., word2vec) demonstrated that rich semantic relationships between words appear as geometric relationships in low-dimensional vector spaces, enabling surprising applications such as bias detection in language, studying cultural change, and predicting material properties. The embedding idea has since generalized to sentences, documents, images, and network nodes.

### Proposed Approach

The authors propose a method to learn dense vector representations of periodicals from the paper-level citation network. The intuition is framed as a citation-following thought experiment: when reading an unfamiliar paper, a reader follows the reference list into earlier papers, creating a citation trail. Each paper in the trail was published in some periodical; treating each periodical as a "word" and each citation trail as a "sentence," one can apply the word2vec skip-gram model to learn periodical embeddings. Periodicals appearing in similar citation contexts will have similar vector representations. Crucially, this approach uses lower-level paper-to-paper citations rather than the coarser periodical-to-periodical citation network, extracting richer and higher-order trajectory information.

The method builds on DeepWalk and node2vec, which are network adaptations of word2vec. The paper states four main contributions: (i) better similarity capture between periodicals than sparse baselines, (ii) a high-resolution map of disciplinary organization with insights into interdisciplinarity, (iii) meaningful cross-disciplinary analogies between periodicals, and (iv) identification of robust conceptual spectra such as the soft-hard science axis.

---

## Results

### Dataset Overview

The method was applied to the Microsoft Academic Graph (MAG), the largest open-access bibliometric dataset at the time. The snapshot contained 126.9 million papers published in 23,404 journals and 1,283 conference proceedings between 1800 and 2016, with 528.2 million citations. After filtering to papers with periodical information, the study used 53.4 million papers and 402.4 million citations across 24,020 scholarly periodicals. The training produced 100-dimensional unit vectors for 20,835 periodicals (3,185 were dropped for low frequency). Discipline labels were obtained by matching MAG periodicals to the UCSD Map of Science catalog, which classifies approximately 25,000 journals into 13 academic disciplines; 12,780 matched journals were used in evaluation tasks.

The basic utility of the embeddings is illustrated by nearest-neighbor examples: the two closest periodicals to *Proceedings of the National Academy of Sciences* are *Nature* and *Science*; the two closest to *American Sociological Review* are *Social Forces* and *American Journal of Sociology*.

---

### Validating the Embedding Space

The authors compared their dense periodical embeddings (referred to as "p2v") against two citation-based sparse baselines:

- **Citation vector (cv):** Each periodical is represented by a 48,020-dimensional vector concatenating normalized in-degree and out-degree citation counts with respect to all other periodicals.
- **Jaccard similarity matrix (jac):** A sparse similarity matrix where each entry represents citation counts between two periodicals normalized by their total citations; this was the best-performing baseline in prior literature.

Three evaluation tasks were used.

#### Task 1: Capturing Similarity Distributions Across Disciplines

100,000 journal pairs were sampled for each of four groups: random pairs, cross-discipline pairs, within-discipline pairs, and within-subdiscipline pairs. The cosine similarity distribution was computed for each group under all three models.

Under cv and jac, most same-discipline and even same-subdiscipline journal pairs receive a similarity score of 0 or near 0, because both methods produce non-negative sparse vectors. This represents the core failure of sparse encodings: they cannot meaningfully differentiate similarity among most pairs. Under p2v, similarity scores range from -0.5 to 1.0, with the distributions for same-discipline and same-subdiscipline pairs clearly shifted relative to random pairs.

Quantitatively, mean cosine similarity values for the four groups (random, cross-discipline, within-discipline, within-subdiscipline) are:
- cv: 0.02, 0.03, 0.10, 0.28
- jac: 0.008, 0.009, 0.046, 0.175
- p2v: 0.07, 0.03, 0.25, 0.54

KL divergence between the within-discipline and random distributions is 0.34 (p2v) versus 0.25 (cv) and 0.11 (jac); for within-subdiscipline pairs, 2.06 versus 1.57 and 1.07. p2v separates the distributions more cleanly at every level of granularity.

#### Task 2: Expert-Ranked Topical Similarity

An expert survey was conducted at the University of Michigan and Indiana University. 247 participants (119 qualified) ranked candidate journals by topical similarity to a target journal. Rankings produced by p2v, cv, jac, and a PageRank-based discipline baseline ("disc.") were compared to expert rankings using Kendall's rank correlation coefficient.

All three vector-space models performed similarly and better than the PageRank baseline. Absolute correlations with experts are low, primarily because experts themselves disagree substantially (average pairwise rank correlation of 0.14 across target journals, and 41.5% of candidate journals placed in an "Unfamiliar Journals" bucket). The practical advantage of p2v over cv and jac in this task is computational: because p2v operates in 100 dimensions rather than 48,040 (cv) or 24,020 (jac), it is orders of magnitude more efficient in time and space for downstream similarity lookups.

#### Task 3: Discipline Category Prediction

Using k-nearest neighbors on vector similarity, the models were tested on predicting the discipline label of a journal from its neighbors. A fourth baseline ("citation weight") assigned a journal the discipline of its highest-weight neighbor in the undirected citation network.

p2v outperforms all baselines in F1 score across all values of k (number of nearest neighbors). This means the embedding space organizes journals such that same-discipline journals cluster more tightly together than under any alternative representation.

Taken together, these three tasks establish that p2v produces a more informative representation of periodical relationships than sparse citation-based alternatives, at lower computational cost.

---

### Disciplinary Structure Revealed by the Periodical Embedding

The embeddings were projected into 2D using t-SNE for visual inspection across 12,780 journals colored by their UCSD discipline assignment. The 13 major disciplines appear as visually coherent regions, broadly confirming that the embedding space recovers established disciplinary organization without being directly trained on discipline labels.

More importantly, the projection exposes structure that disjoint classification systems cannot represent. Several specific examples are described:

- **Archaeology and anthropology journals** classified by UCSD as "Earth Sciences" form a distinct cluster positioned geometrically closer to "Social Sciences" than to the main Earth Sciences cluster, as verified by cosine distances.
- **Medical imaging journals** span "Brain Research," "Medical Specialties," and "EE & CS," reflecting the genuine cross-disciplinary character of neuroimaging research.
- **Parasite-focused journals** span "Social Sciences" (*Ecohealth*), "Biology" (*Parasites*), "Infectious Diseases" (*Malaria Journal*), and "Chemistry" (*Journal of Natural Toxins*), revealing the multifaceted nature of parasite research.

The authors then quantify disagreement between the embedding-based clustering and the UCSD classification. K-means with k=13 was applied to the embedding vectors (excluding 29 multidisciplinary journals), and the resulting clusters were compared to UCSD categories using the element-centric similarity measure, which produces a per-journal agreement score.

The map of agreement shows that interdisciplinary microclusters identified visually correspond to areas of high disagreement between the two clusterings. The distribution of agreement scores within each discipline is multimodal: most journals are assigned consistently, but a significant minority show strong disagreement.

A manual evaluation confirmed the interpretation: for journals with high agreement between p2v clustering and UCSD labels, human evaluators consistently confirmed that the journals clearly belong to their designated discipline. For journals with low agreement (about 40%), evaluators found the UCSD designation disputable, with many journals spanning multiple fields (e.g., *Biostatistics*, *Aggressive Behavior*, and *Cell Biology Education* are all classified as "Social Sciences" in UCSD). This supports the hypothesis that disagreement between an embedding-based clustering and a traditional classification system is a meaningful signal of genuine interdisciplinarity or misclassification, not noise.

The authors propose that this framework can operationalize interdisciplinarity quantitatively: for example, a paper's interdisciplinarity could be measured as the average cosine distance among its cited periodicals.

---

### Cross-Disciplinary Analogies Between Scholarly Periodicals

A central demonstration of word embeddings is the arithmetic analogy: v(king) - v(man) + v(woman) ≈ v(queen). The same operation generalizes to periodical embeddings. Given a "disciplinary axis" defined by two pole periodicals A and B (one from field X, one from field Y), the vector [v(B) - v(A)] points from X toward Y. Applying this to a seed periodical C produces a new periodical D that is analogically related to C as B is to A.

The authors construct "analogy graphs" by iteratively applying this operation. Starting from a seed, each step finds the best candidate periodical by moving along the axis. The results form a directed network of periodicals.

Several examples are presented:

- Using *JMLR* (Machine Learning) and *ASR* (Sociology) as poles, applied to *KDD* and *ICWSM* as seeds, the analogy graph traces a meaningful spectrum from disciplinary sociology (*Social Forces*) through computational social science conferences (*EMNLP*, *IEEE ICDM*) to core machine learning conferences (*ICML*, *NeurIPS*).
- Using *Cell* (Biology) and *Physical Review Letters* (Physics) as poles applied to *ASR*, the graph identifies journals with increasing biological flavor (*NEJM*) or physical flavor (*Social Forces*).
- More exotic combinations, such as applying (*ASR*, *PRL*) to *Blood*, discover a more "physical" journal (*Cell*) and a more "sociological" journal (*NEJM*) from the medical domain.

To validate analogy quality systematically, the authors used author overlap between periodicals as an external signal. The logic: for a valid analogy "A : B ~ C : D," moving from C to D should mean that the ratio of shared authors between C and A versus C and B should be larger than the corresponding ratio for D. That is, D should be comparatively more connected to B's community than C was.

For all 78 discipline pairs (13 disciplines taken two at a time), 1,800 analogy graphs were generated by selecting poles and seeds from the top 10 PageRank-ranked journals in each discipline. The fraction of analogy edges satisfying the author overlap criterion was computed for p2v and cv. p2v outperforms cv for all 78 discipline pairs, and the differences are statistically significant at p < 0.001. This provides systematic, externally-grounded evidence that the periodical analogies produced by the neural embeddings are semantically valid.

---

### Extracting Conceptual Dimensions in Disciplinary Organizations

The analogy operation generalizes from individual periodical pairs to sets of periodicals. By computing the centroid of all periodical vectors in one disciplinary group and subtracting the centroid of another group, a "conceptual axis vector" is obtained. The projection of any periodical onto this axis (measured as cosine similarity to the axis vector) gives a score quantifying where the periodical sits along that dimension.

Two conceptual axes are examined.

#### The Soft-to-Hard Sciences Axis

This axis is motivated by the long-standing "hierarchy of the sciences" concept, which holds that disciplines can be ordered by subject complexity and degree of codification, with mathematics and physics as "hardest" and social sciences as "softest."

Operationally: the hard pole is defined by the centroid of all journals in "Math & Physics"; the soft pole by the centroid of journals in "Social Sciences" and "Humanities." Every periodical is projected onto the resulting axis vector.

The resulting spectrum is continuous and internally coherent. Among the hardest-projecting journals: *Biophysical Journal*, *Journal of Theoretical Biology*, *Fractals*, *Physics Reports*, *Physical Review E*. Among the softest: *Applied Psychology*, *Anthropological Quarterly*, *Law & Society Review*, *Sociological Forum*, *Politics & Society*. When the 13 disciplines are ranked by their mean projection values, the ordering is: Social Sciences, Humanities, Health Professionals, Brain Research, Medical Specialties, Biology, Earth Sciences, Chemistry, Engineering, Infectious Diseases, EE & CS, Biotechnology, Math & Physics. This broadly confirms the intuitive hierarchy, with hardness increasing through Sociology, Psychology, Biology, Chemistry, Physics, and Mathematics.

#### The Social-to-Biological Sciences Axis

The second axis runs from social sciences and humanities to life sciences (Biology, Biotechnology, Infectious Diseases, Health Professionals, Medical Specialties). This axis is orthogonal in interpretation to the soft-hard axis, and the disciplinary ordering changes substantially along it.

Biomedical disciplines cluster near the biological end. Most physical sciences (Chemistry, Earth Sciences, Math & Physics) fall in the middle. Computer science, which was far from Social Sciences on the soft-hard axis, is nearest to Social Sciences on the social-biological axis. This reflects the different senses in which fields are "close" or "distant": methodology (soft-hard) versus subject matter (social-biological). The comparison of the two spectra for the same set of annotated journals illustrates the multidimensional nature of disciplinary organization that a single classification system cannot capture.

#### Robustness Validation

The two axes were validated in two ways. First, the axis was rebuilt from random subsets of journals in the pole disciplines and the resulting ordering of all periodicals was correlated with the original. Spearman rank correlation remains above 0.9 even when fewer than 1% of journals from each pole discipline are used to construct the axis. Both the soft-hard and social-bio axes are therefore stable and not artifacts of the specific journal selection.

Second, the authors tested whether the global axis is consistent with axes constructed entirely within one of the pole disciplines, using subdisciplines as poles. For the soft-hard axis within Social Sciences and Humanities, using Sociology (soft) and Finance (hard, given its connections to math and physics) as internal poles, the Spearman rank correlation between the internal-axis ordering and the global ordering is 0.73. Across nine subfield pair combinations (three soft subdisciplines crossed with three hard subdisciplines), the average rank correlation is 0.73 (95% CI: [0.69, 0.77]). The same robustness test for the social-bio axis, using Sociology as social and BioStatistics as bio, yields a rank correlation of 0.82 with the global axis, with an average of 0.71 (95% CI: [0.63, 0.78]) across nine subfield pairs. These results confirm that the global conceptual axes are not artifacts of the broad category definitions used to construct them, but reflect structure that is present at finer granularities within the data.

---

## Discussion

The discussion synthesizes the findings and situates the contribution within the field.

The authors argue that the continuous embedding framework represents a significant advance over sparse citation-based approaches: it produces representations that are simultaneously more informative, more compact, and better aligned with external signals of disciplinary similarity. Beyond replicating existing classifications, the embeddings surface structure that categorical systems obscure, particularly for genuinely interdisciplinary periodicals.

Two novel measurement capacities are highlighted: (1) cross-disciplinary navigation via vector analogies, which provides a principled way to explore the landscape between disciplines; (2) quantitative grounding along conceptual dimensions, which allows continuous rather than categorical placement of periodicals on axes like soft-to-hard or social-to-biological.

The authors acknowledge that better embedding methods likely exist given the rapid pace of development in machine learning, and they position their contribution as an early application of the embedding paradigm to the science of science, with extensive validation rather than novel architecture.

Six limitations are enumerated:

1. **Data quality dependence.** Embedding quality reflects the quality and coverage of the underlying MAG dataset; fields underrepresented in MAG will have weaker embeddings.
2. **Sparse data for small periodicals.** Periodicals with few papers and citations will have less stable embeddings, though still better than methods using only direct links.
3. **Frequency filtering.** Periodicals appearing fewer than 50 times are excluded, which may underrepresent smaller fields, though coverage is shown to be reasonable across all 13 UCSD disciplines.
4. **Sufficiency of single vectors.** The assumption that one vector per periodical captures all relevant relationships may fail for highly multidisciplinary journals, which may be pulled toward their primary discipline and fail to represent all their topical connections. The method may also be inappropriate when explicit direct citation connections are specifically required. Furthermore, simpler methods can outperform embedding-based ones for certain tasks (e.g., majority voting beats p2v for predicting publication venue from references).
5. **No temporal dimension.** The present study treats all citations as contemporaneous, producing a static picture. It cannot capture how disciplines emerge, merge, or drift over time.
6. **Incomplete theoretical understanding.** The mechanisms and potential biases of neural embedding methods are not fully understood, and unknown biases may be present in the resulting representations.

Future directions suggested include developing improved embedding methods for scholarly periodicals, using the embedding capacity to investigate substantive science-of-science questions, and incorporating temporal citation information to model the evolution of disciplines.

---

## Materials and Methods

### Dataset

The Microsoft Academic Graph (MAG) snapshot accessed on 5 February 2016 was used. It contains 126,909,021 papers in 23,404 journals and 1,283 conference proceedings from 1800 to 2016, with 528,245,433 citations. After restricting to papers with periodical information, the working dataset is 53,410,055 papers and 402,395,790 citations across 24,020 periodicals. Discipline labels for 12,780 journals were obtained by matching to the UCSD Map of Science catalog on journal name.

### Model

The citation network is treated as a directed graph where nodes are papers and edges run from citing to cited paper. Random walks on this graph generate citation trails: starting from a randomly chosen paper, the walk follows citations randomly until reaching a paper with no outgoing edges (no further citations). Trails of length 1 are discarded. Each trail is a sequence of papers; the corresponding sequence of periodicals in which those papers were published forms a "periodical trail."

Two vector representations per periodical are learned (input and output vectors) using skip-gram with negative sampling (SGNS), the same objective as word2vec. For a given periodical trail, the objective is to maximize the log probability of each periodical's context periodicals within a window of size w. This is approximated using the SGNS objective: for each (input, output) pair, k=5 negative samples are drawn from a smoothed unigram distribution over periodicals. After training, input vectors are used as the final embeddings. Training used N=100,000,000 periodical trails. The Gensim package was used for implementation. Training took approximately 3 hours on a standard computing server.

### Hyperparameter Tuning

Context window size W was evaluated at {2, 5, 10} and embedding dimensionality D at {50, 100, 200, 300}. Models were compared by cosine similarity discrimination among same-discipline, same-subdiscipline, and random journal pairs. The best model used W=10 and D=100, yielding 20,835 periodicals. A minimum frequency threshold of 50 occurrences was applied to exclude very rare periodicals.

### Journal Recommendation Survey

The expert survey recruited 367 participants (247 completed; 119 qualified) from the University of Michigan and Indiana University, following IRB guidelines. Participants selected a discipline, confirmed familiarity with at least three of the top 20 journals (by PageRank) in that discipline, then ranked candidate journals by topical similarity to each familiar target journal. Candidate sets were formed from the union of the top four most similar journals according to each algorithm (4 to 12 candidates depending on overlap). Rankings were compared using Kendall's rank correlation, focusing on target journals with average pairwise expert agreement at or above 0.2.

### Evaluation with UCSD Categorization

To test whether disagreement between p2v clustering and UCSD labels signals genuine interdisciplinarity, 20 journals each from the top and bottom 100 by agreement score were selected from three disciplines (EE & CS, Engineering, Social Sciences) and evaluated by three of the paper's authors. Evaluators assessed whether each journal clearly belongs to its UCSD-designated discipline, using labels: yes, no, interdiscipline, or unsure. Pre-test inter-rater Cohen's kappa was 0.59 (moderately high). Results from pretest (majority voting) and posttest were combined; journals labeled "unsure" were excluded.

### Validating the Two Spectra of Science

Robustness of the soft-hard and social-bio axes was tested by: (1) rebuilding each axis from random subsets of journals in the pole disciplines and correlating the resulting orderings with the original, repeated 100 times; (2) rebuilding axes using subdiscipline pairs within the anchor disciplines and correlating with the global ordering. Both approaches yield high and stable rank correlations, confirming that the identified spectra are genuine features of the embedding space.
