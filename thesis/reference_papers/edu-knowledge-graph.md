# EduEmbedd – A Knowledge Graph Embedding for Education

## Metadata

- **Author:** Anurag Mohanty (IIIT Bangalore, Electronics City Phase 1, Bengaluru, Karnataka, India)
- **Year:** 2023
- **Venue:** Workshop on Enterprise Knowledge Graphs using Large Language Models, Oct 22, 2023, Birmingham, UK
- **Proceedings:** CEUR Workshop Proceedings (CEUR-WS.org), Vol-3532/paper1
- **License:** CC BY 4.0
- **DOI/URL:** http://ceur-ws.org (ISSN 1613-0073)

---

## Abstract

The paper proposes EduEmbedd, a framework for constructing Knowledge Graph Embeddings (KGE) specifically for the education domain. The motivation is twofold: the growing strength of knowledge graphs as a means of integrating heterogeneous data, and the increasing use of AI in educational applications. The paper argues that domain-specific KGEs have practical value in the LLM era because they can help address hallucination and improve interpretability.

The core claim is that educational entities (courses, chapters, topics, concepts) are best represented by combining two types of information: pedagogical context (how learning entities relate to each other structurally and hierarchically) and content context (what concepts and topics the learning material actually covers). Prior work has generally addressed only one of these. EduEmbedd integrates both into a single KG and learns embeddings from weighted triples. The paper demonstrates that a weight-aware TransH model outperforms both weight-naive TransH and other KGE models on link prediction metrics and cosine similarity tests on a custom NLP course dataset.

---

## 1. Introduction

The introduction establishes the foundational premise: educational learning data inherently carries multiple kinds of information simultaneously, and any embedding intended to represent an educational entity should reflect all of them.

The paper identifies two principal contexts:

**Pedagogical context** refers to the meta-information describing how learning entities relate to one another. This includes:
- Learning complexity levels (beginner, intermediate, expert)
- Inter-dependencies between courses or chapters (supplementary, complementary, composite, contradicting)
- Inheritance and composition relationships (IS-A, Has-A)
- Prerequisite structures

The pedagogical context is structural and organizational rather than content-driven. It captures where an entity sits within the broader learning ecosystem.

**Content context** refers to the knowledge present in the actual learning material: the topics covered in a course chapter, the instructional concepts introduced, the vocabulary and ideas in the text. This is the semantic substance of the learning entity rather than its position in a curriculum hierarchy.

The paper argues that prior work has typically used one or the other of these contexts, not both. KGE offers a principled way to combine them, because both kinds of information can be modeled as relationships between nodes in a graph. A course chapter is thus defined by all of its relationships simultaneously — to prerequisite chapters, to complexity levels, to the topics LDA finds in its text, and to the instructional concepts it introduces.

Beyond the dual-context integration, the introduction highlights a second design requirement that the paper treats as novel: relationships in an education KG should be **weighted**. Relationships are not binary; the strength or probability of an association matters. For example, one course chapter may supplement another more strongly than a third one does. A topic model assigns probabilistic weights to topics within a document. A complexity level may be assigned with a degree (e.g., 80% intermediate). Standard KGE models ignore such numeric edge attributes, and EduEmbedd is designed to incorporate them.

The two contributions are thus summarized as:
1. Amalgamating knowledge from multiple contexts (pedagogical and content)
2. Incorporating weighted relationships between entities

---

## 2. Related Work

The related work section covers two main areas: prior work on educational knowledge graphs, and the landscape of KGE models (especially those with any form of numeric attribute support).

### Educational Knowledge Graphs

Prior work in constructing education-domain KGs has largely been fragmented and single-purpose:

- Wang et al. [1] extracted concept hierarchies from textbooks.
- Chaplot et al. [2] induced prerequisite structures from course unit data.
- Liang et al. [3] recovered prerequisite relations from university course dependencies.
- Liu et al. [4] at Carnegie Mellon University built directed concept graphs from observed relations between courses, but assumed those relations to be known in advance.
- MOOC providers including Khan Academy [5] have built dedicated KGs for online courses, but these are typically undirected graphs built by domain experts rather than automatically.
- KnowEdu [6] (Chen, Lu et al.) provides a system for automatic KG construction in education, but focuses on a single type of concept relation.

The paper notes that none of these works construct a KGE for a domain-specific educational KG, and none simultaneously integrate both content and pedagogical contexts. Most use either the text/concept content or the hierarchical structure, not both.

### Knowledge Graph Embedding Models

The paper gives a concise survey of KGE model families:

- **Translational models:** TransE [8] is the foundational distance-based model. TransH [9] projects entities and relations onto a hyperplane. TransR [10] introduces separate projection spaces for entities and relations.
- **Bilinear/compositional models:** DistMult [11] uses symmetric bilinear-diagonal scoring. ComplEx [12] and RotatE [13] extend this asymmetrically in complex space. HOLE [14] uses circular correlation for compositional representations.
- **Tensor decomposition models:** RESCAL [15], TuckER [16], SimplE [17].
- **Convolutional models:** ConvE [18], ConvKB [19].
- **Attention-based:** Nathani et al. [20].

None of these standard models incorporate numeric attributes on edges. Some multimodal KGE works handle numeric values on nodes: LiteralE [21] enriches node embeddings with numeric literals; KBLRN [22] combines latent, relational, and numeric node features using a product-of-experts model; TransEA [23] jointly trains a structural model and an attribute model for node attributes.

The paper identifies UKGE [24] as the only prior KGE work designed for numeric values on edges. UKGE uses probabilistic soft logic [25] to predict probability estimates for unseen triples by treating edge weights as confidence scores. The paper notes two limitations of UKGE: it requires out-of-band logical rules as additional input, and its design targets uncertainty representation (weights as confidence that a triple is true), which differs from EduEmbedd's intent (weights as degree-of-association).

The paper also notes that Pai and Costabello [26] and the AmpliGraph library [27] support numeric edge attributes for representation learning, but neither supports TransH as a base model, and EduEmbedd requires additional modifications across multiple components of the KGE pipeline.

---

## 3. EduEmbedd Framework

### 3.1. Preliminaries

The paper introduces standard KGE notation. A knowledge graph G = (s, p, o) ⊆ E × R × E is a set of triples t = (s, p, o), where s is the subject entity, p is the predicate (relation), and o is the object entity. E and R are the sets of all entities and relation types.

For EduEmbedd, triples are extended with a numeric weight attribute w ∈ R, yielding G = t = (s, p, o, w). Weights are assigned to triples (i.e., to edges), not to nodes.

### 3.2. EduEmbedd Framework Details

The framework is presented as a multi-stage pipeline (illustrated in Figure 2):
1. Collect content-based and pedagogical triples from educational data
2. Assign weights to the triples
3. Generate the KGE by modifying a base KGE model to incorporate weights (or post-processing)
4. Tune the KGE model
5. Select the final model based on quantitative and qualitative evaluation

#### 3.2.1. Identification of Entities

Unlike generic KGs whose nodes are real-world entities (people, places, organizations), the education domain requires careful definition of what counts as an entity. For EduEmbedd, entities are:

- **Course learning chapters:** The primary units of educational content.
- **Topics from LDA topic modeling:** Latent Dirichlet Allocation is applied to the text of each course chapter to identify a statistical distribution over topics. Each topic is a cluster of keywords. The paper notes that BERTopic or similar probabilistic topic models could also be used. Topics are treated as more abstract entities that may not be directly interpretable by humans.
- **Instructional concepts (ICs):** The concrete, nameable concepts that a learner is expected to understand after studying a chapter (e.g., "CFG grammar," "Dependency grammar" for an NLP chapter). These are more tangible than LDA topics and often appear in textbook indices. Two extraction strategies are discussed: (a) building a master list from textbook indices and searching for these in chapter text, or (b) using a pre-trained LLM (e.g., GPT) with prompt engineering to extract ICs from chapter text.
- **Complexity levels:** Categorical labels (Beginner, Intermediate, Expert) assigned to each chapter. The paper experimented with LLM-based assignment using few-shot prompt engineering and found mixed results; for consistency, expert manual review was used instead.

#### 3.2.2. Identification of Relationships

EduEmbedd defines four relationships within its current scope:

- **Text_topic** (content type): Links a course chapter (head) to the topic identifiers (tail) produced by LDA. Captures what the chapter is statistically "about."
- **Concept_vocab** (content type): Links a course chapter (head) to instructional concepts (tail) present in that chapter. Captures the explicit learning concepts.
- **Prerequisite** (pedagogical type): Links a course chapter (head) to other chapters (tail) that are considered prerequisite to understanding it. Currently determined by expert review of course mandates and curricula.
- **Level** (pedagogical type): Links a course chapter (head) to its complexity level (tail). Currently determined by expert review of course abstracts and introductions.

The paper notes that many more relationships could theoretically be included, but recommends restricting to those relevant to the target use case. For instance, if all corpus materials come from a single field (e.g., engineering), a subject-domain relationship would add no discriminative signal and should be excluded.

#### 3.2.3. Assigning Weights to Relationship Edges

Weights are assigned differently depending on the relationship type:

- **Text_topic weights:** LDA directly produces probability distributions over topics for each document. These topic probabilities serve as the edge weights for Text_topic triples, capturing how strongly a chapter is associated with each topic.
- **Concept_vocab weights:** TF-IDF scores for the instructional concept terms within a chapter document. Higher TF-IDF weight means the concept is more central to that chapter.
- **Prerequisite weights:** Expert assessment quantifying the degree to which a prerequisite chapter is actually necessary or helpful for understanding the head chapter.
- **Level weights:** Expert assessment quantifying the extent to which the chapter is at a given complexity level (e.g., 80% Intermediate). When a chapter is clearly fully at one level, the weight is 1.

#### 3.2.4. Building the EduEmbedd KGE Model

The paper describes the model selection process. The primary requirement is that the KGE model handle 1-to-1, 1-to-many, and many-to-many relationships, which disqualifies TransE (known to struggle with non-1-to-1 mappings). The paper also prioritizes interpretability of the scoring function so that the model can be audited and modified to incorporate edge weights.

The paper evaluates both compositional and translational model families:

- **TransH** was selected as the primary base model because it supports all three relationship cardinalities and is sufficiently interpretable in terms of its scoring objective. TransR was considered but rejected due to greater computational complexity.
- **Holographic Embedding (HOLE)** was selected as a secondary model to experiment with a different genre and to enable cross-family comparisons.

The paper acknowledges that a more exhaustive search across all available KGE models is out of scope for this version and is designated as future work.

#### 3.2.5. EduEmbedd Support for TransH Edge Weights

This subsection describes the technical contribution at the modeling level. Standard TransH does not use numeric edge attributes. The paper modifies TransH throughout its network components to incorporate edge weights. The components modified are:

- **Scoring function:** Assigns scores to triples using the TransH scoring function, with higher scores for positive triples.
- **Loss function:** Optimizes the embedding by maximizing the margin between positive and negative triples.
- **Optimization algorithm:** Margin-based ranking loss constrains the gap between positive and corrupted triple scores.
- **Regularization mechanism:** Handles initialization and regularization of KGE network tensors.
- **Initializer:** Entity and relation embedding initialization functions.
- **Negatives generation strategy:** Corrupted (synthetic negative) triples are generated following the protocol of Bordes et al. (2013): a corruption of triple t = (s, p, o) is defined as either (s, p, o') or (s', p, o), where the corrupted entity is drawn randomly from E. One side of the triple is corrupted at a time, following the local closed world assumption.

The mathematical formulation is given as follows. The base TransE scoring function is:

    f(t) = -||e_s + r_p - e_o||_n

A softplus non-linearity is applied to ensure non-negative scores:

    g(t) = ln(1 + e^{f(t)}) >= 0

With edge weights incorporated into the scoring, the function becomes:

    h(t) = g(t) * w    [where w is the edge weight]

The loss function is a modified, numerically stable version of the negative log-likelihood of normalized softmax scores:

    L = -(log(e^{h(t+)} / (e^{h(t+)} + e^{h(t-)})))

where t+ denotes positive triples and t- denotes corrupted triples. By modulating the output by the numeric edge weight, the training process is steered to focus on triples with higher weights, and the margin between high-weight positive triples and their corruptions is maximized more aggressively.

#### 3.2.6. Model Fine-tuning and Final Model Selection

Hyperparameters tuned during experiments include:

- **Embedding dimension (k):** Chosen empirically given the amount of training data and the number of entity features.
- **Batch size:** Values between 5 and 20 are tried empirically.
- **Learning rate:** Varied by factors of 10 from a default of 0.1.
- **Number of epochs:** Tuned if early stopping is not configured, to ensure convergence.

---

## 4. Experiments

Evaluation combines technical predictive evaluation (link prediction) and functional evaluation (cosine similarity of similar entities).

### Dataset

A custom dataset built from open-source educational courses in the Natural Language Processing domain, spanning more than 300 lesson chapters in total. Because this is a purpose-built domain dataset, no established prior performance baselines exist for comparison. The evaluation therefore focuses on relative comparisons between models rather than absolute benchmarks.

### Evaluation Metrics (Link Prediction)

Standard KGE link prediction metrics are used:

- **Mean Rank (MR):** Average rank of correct predictions across all positive triples (lower is better).
- **Mean Reciprocal Rank (MRR):** Average of the reciprocal ranks of positive predictions (higher is better).
- **Hits@1, Hits@3, Hits@5, Hits@10:** Fraction of positive triples ranked within the top 1, 3, 5, and 10 positions respectively (higher is better).

### 4.1. Technical Predictive Evaluation

Three objectives guide this phase of evaluation:
1. Compare multiple models to select the best performer.
2. Identify the best hyperparameter configuration for the selected model.
3. Establish a relative baseline for the custom dataset.

Results are reported in Table 1, which covers TransH_with_weights, TransE_with_weights, and HolE_with_weights across varied epoch counts (50 and 100), embedding dimensions (k = 40 and 50), and learning rates (0.1 and 0.01).

Key findings from Table 1:
- **TransH_with_weights** consistently outperforms TransE_with_weights and HolE_with_weights across nearly all configurations and metrics.
- The best single configuration for TransH_with_weights is 50 epochs, k=50, lr=0.1, achieving MRR = 0.207, MR = 47.23, Hits@10 = 0.402, Hits@5 = 0.289, Hits@3 = 0.219, Hits@1 = 0.114.
- HolE_with_weights at lr=0.01 and k=50 produces degenerate results (MRR near 0, MR near 800), suggesting training instability for that configuration.
- TransE_with_weights shows the weakest overall performance, with MR values in the range of 95-155 and Hits@10 around 0.14-0.22.

Table 2 directly compares the best TransH_with_weights configuration against vanilla TransH (without edge weights):
- TransH_with_weights: MRR = 0.206, MR = 46.86, Hits@10 = 0.390, Hits@5 = 0.288, Hits@3 = 0.219, Hits@1 = 0.113
- TransH (no weights): MRR = 0.202, MR = 47.35, Hits@10 = 0.399, Hits@5 = 0.280, Hits@3 = 0.213, Hits@1 = 0.106

The differences are modest but consistently favor the weight-aware model on MRR, Hits@5, Hits@3, and Hits@1. Vanilla TransH has a slightly higher Hits@10 (0.399 vs 0.390), but performs worse on the higher-precision metrics. The paper interprets this as evidence that incorporating weights improves the model's ability to produce fine-grained rankings.

### 4.2. Functional Evaluation of TransH with Weights

Because the technical evaluation lacks external baselines, the paper supplements it with a functional evaluation designed to test semantic coherence. A test set of 22 similar entities is drawn from the base data, and average pairwise cosine similarity is computed for the embeddings produced by each model.

Table 3 (all models with edge weights):
- HolE_with_weights: 0.48
- TransE_with_weights: 0.33
- TransH_with_weights: **0.64**

TransH_with_weights produces embeddings that are substantially more similar for semantically related entities than either of the other two model families. The paper takes this as confirmation that TransH_with_weights has the strongest semantic representation capability among the tested models.

Table 4 (effect of weights for TransH):
- TransH_with_weights: **0.64**
- TransH_without_weights: 0.49

The weight-aware version produces embeddings with noticeably higher cosine similarity for similar entities (0.64 vs 0.49), supporting the paper's core claim that incorporating weighted relationships produces semantically richer embeddings.

---

## 5. References (summary of cited works)

The paper cites 27 works. The most relevant to the paper's contributions:

- [1]-[4]: Prior work on education KG construction (concept hierarchies, prerequisite structures, concept graphs).
- [5]-[6]: Industry KG efforts (Khan Academy, KnowEdu).
- [7]: Survey of KGE and explainable AI.
- [8]-[20]: KGE model landscape (TransE through attention-based models).
- [21]-[23]: Multimodal KGE with numeric node attributes (LiteralE, KBLRN, TransEA).
- [24]-[25]: UKGE (the only prior work on numeric edge attributes in KGE) and probabilistic soft logic.
- [26]-[27]: Pai and Costabello's numeric edge attribute work and the AmpliGraph library.

---

## Summary and Critical Assessment

**Core contribution:** EduEmbedd introduces a framework that (a) integrates pedagogical and content-based information about educational entities into a single KG, (b) assigns numeric weights to KG edges based on probabilistic or expert-derived measures of relationship strength, and (c) modifies the TransH KGE model to exploit those edge weights during training. The modification touches the scoring function, loss, optimization, regularization, initialization, and negative generation components of TransH.

**Empirical results:** Experiments on a modest custom NLP course dataset (300+ chapters) show that TransH_with_weights outperforms TransE_with_weights and HolE_with_weights on most link prediction metrics, and outperforms weight-naive TransH on semantic similarity. The improvements are incremental rather than dramatic, which the paper attributes to the small and domain-specific nature of the dataset and the lack of prior baselines.

**Limitations (from the paper):** Exhaustive model selection is described as future work. The dataset is small and restricted to NLP courses. Complexity level assignment by LLM produced inconsistent results, requiring manual expert fallback. The paper does not evaluate on downstream educational tasks such as course recommendation or curriculum planning.

**Relevance to thesis work:** This paper is relevant as background on embedding-based representations of educational content, especially the argument that educational entities carry heterogeneous relational structure that flat text embeddings may not fully capture. The KGE approach contrasts with the text-embedding approach used in MajorMatch: EduEmbedd explicitly constructs relational structure and learns from it, while text embeddings implicitly encode semantic content from surface form. The paper also demonstrates the use of cosine similarity as a functional evaluation of embedding quality for similar entities, which parallels evaluation approaches in the thesis.
