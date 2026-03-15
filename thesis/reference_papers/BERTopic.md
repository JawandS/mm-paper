# Recommending the Right Academic Programs: An Interest Mining Approach Using BERTopic

## Metadata

- **Authors:** Alessandro Hill, Kalen Goo, Puneet Agarwal
- **Year:** 2025 (received February 6, 2024; accepted December 28, 2024; published online March 13, 2025)
- **Venue:** *Data Mining and Knowledge Discovery*, vol. 39, article 20
- **DOI:** https://doi.org/10.1007/s10618-024-01087-y
- **Affiliations:** Hill: University of Bologna (DEI) and California Polytechnic State University; Goo and Agarwal: California Polytechnic State University, Department of Industrial and Manufacturing Engineering

---

## Abstract

The paper presents a decision support system called **TopProRec** (Top Program Recommender) that helps prospective and transfer students match their personal interests with suitable academic programs. The system uses BERTopic, a topic modeling algorithm, to mine interest topics from university course descriptions. Students select interest topics presented as word clouds, and the system computes a ranked shortlist of programs via a statistical backtracking method through what the authors call a "knowledge map" — a network representing program-course relationships. A case study at a large US polytechnic university with 84 programs and over 4,200 course descriptions is evaluated through a user experiment with 65 students. Over 98% of users found the recommendations aligned with their interests, and ~94% said they would use the tool in the future. Quantitative analysis shows the system can achieve 98% program coverage while maintaining a personalization score of 0.77.

---

## 1. Introduction

The introduction motivates the problem with statistics on the scale and stakes of higher education program selection. In 2022, 18.6 million US students were enrolled in college programs, choosing from over 1,800 majors at approximately 6,000 institutions. A 2024 survey found 54% of college students doubted their major choice at least occasionally, and more than 50% change their major at least once. A study at Georgia Tech found 35% of students leaving the CS program cited the program being too narrow to accommodate outside interests. Forty-four percent of job-seeking graduates regret their major choice.

The introduction identifies two compounding problems. From the student side: the volume of programs is overwhelming, interdisciplinary content creates confusion, and high-level program descriptions (learning objectives) often do not clearly communicate what a program actually teaches day-to-day. From the institutional side: reducing internal transfers (students who change programs before graduating) lowers administrative costs, and increasing major-fit satisfaction has positive downstream effects on dropout rates and overall student satisfaction.

The authors argue that their approach is distinctive in several ways. It is based entirely on publicly available course catalog data and requires no confidential student records (no entrance exam scores, grades, or demographic information). It operates without labeled training data, using unsupervised machine learning rather than supervised prediction. To the authors' knowledge, no prior automated system has used course description data at the course level to support program selection.

The system also has equity implications: students who lack access to conventional support structures (private college counselors, well-resourced high school advising) can benefit from an automated, freely accessible tool.

The introduction lists four key contributions:
1. A novel, broadly applicable ML-based decision support system for study program recommendations.
2. Practical design and implementation guidelines from real-world deployment.
3. Comprehensive qualitative and quantitative evaluation using real recommendations, student surveys, and computational analysis.
4. A framework for expanding student support services through a real-time, user-centered, data-driven system.

The paper is organized as: related work (Section 2), system description (Section 3), case study and evaluation (Section 4), conclusion (Section 5), appendices.

---

## 2. Related Work

This section surveys prior work on decision support systems (DSS) for university major or program selection. The authors organize prior approaches into a taxonomy: Multiple Criteria Decision Making (MCDM) models, Rule-Based Method of Knowledge Representation (RBMKR), supervised ML, and unsupervised ML. Table 1 in the paper maps nine prior systems to these categories.

### 2.1 MCDM Approaches

Three prior systems use MCDM:

- **Permanasari et al. (2020)** — A hybrid MCDM system for Indonesian high school students, combining Simple Additive Weighting (SAW), TOPSIS, and Gray Relational Analysis (GRA). Uses test scores, academic reports, and declared majors as input.
- **Khasanah et al. (2015)** — A Fuzzy SAW DSS for high school major selection, incorporating academic performance, psychological tests, and interest questionnaires.
- **Conejero et al. (2021)** — Applies TOPSIS to assess vocational and educational training programs on employability outcomes, using a dataset of 28,000 student records.

### 2.2 Rule-Based Approaches

Two prior systems use rule-based or theory-based reasoning:

- **Ayman Al Ahmar (2012)** — A rule-based expert system using an object-oriented database, with majors as objects with attribute and skill values. Selection rules incorporate high school scores and personal preferences.
- **Kumar and Kumar (2013)** — Uses the Theory of Reasoned Action (TRA) framework to model students' business major decisions, factoring in attitudes toward job opportunities, social image, personal aptitude, and subjective norms from family, friends, and teachers.

### 2.3 Supervised ML Approaches

- **Zayed et al. (2022)** — Applies decision trees, SVMs, and random forests to predict optimal majors using academic performance, grades, labor market data, and gender. Random forest achieves 97.7% accuracy.
- **Stein et al. (2020)** — A nearest-neighbor recommender built on nine years of historical student data, comparing a student's first two years of coursework and performance to major averages.

### 2.4 Unsupervised ML Approaches

- **Alghamdi et al. (2019)** — A fuzzy-based system using similarity-based clustering to group majors by content or field similarity, incorporating academic performance and preferences.
- **Obeid et al. (2018)** — An ontology-based system focusing on skills, interests, and preferences rather than grades. Clusters graduate student profiles and recommends majors by profile similarity.

### 2.5 Course-Level and MOOC Recommenders

The section also reviews related systems that recommend courses rather than programs: Al-Badarenah and Alsakran (2016) use k-means clustering for elective course recommendations; Elbadrawy and Karypis (2016) integrate matrix factorization and collaborative filtering; Jing and Tang (2017) recommend MOOCs on XuetangX; Bakhshinategh et al. (2017) incorporate Graduating Attributes in a time-aware course recommender; and Pardos and Jiang (2020) build a serendipity-focused course recommendation system. Hatzakis et al. (2007) used a program management framework to improve curriculum coherence.

### 2.6 Topic Modeling Background

The section provides a conceptual overview of topic modeling, explaining the distinction between probability-based approaches (LDA, NMF) and embedding-based approaches (Top2Vec, BERTopic, CTM). LDA and NMF are noted to have two key drawbacks: the number of topics must be prespecified, and they cannot capture semantic context between words. Embedding-based methods address these limitations by encoding text so that semantically similar documents cluster together in vector space.

Recent work has extended topic modeling with deep learning and BERT-based Neural Topic Models (NTMs), and hybrid LDA-BERT models have appeared. Topic modeling has been applied across bioinformatics, marketing, material science, social media, transportation, and tourism. Föll and Thiesse (2021) applied topic modeling specifically to university IS curricula in Germany, analyzing 90+ programs and 3,700 modules.

### 2.7 Differentiation of This Work

The authors close the section by distinguishing TopProRec from all prior work. Unlike existing systems, it (a) mines course descriptions rather than using student records, (b) requires no labeled data, (c) operates at the course content level rather than at the program metadata level, and (d) is the first automated system to use course description data for program selection. The unsupervised approach avoids the biases inherent in MCDM criteria weighting and the need for labeled training sets, and it is more adaptive to changing preferences.

---

## 3. The Recommender System

This section describes the TopProRec system in detail, covering the overall process architecture, data model, topic modeling pipeline, topic presentation interface, and the backtracking recommendation algorithm.

### 3.1 Overview and Recommendation Process

TopProRec is classified as a **session-based recommender system**: it generates personalized recommendations from a single interaction with a new user, with no prior user history required. The definition used (from Ricci et al. 2022) is "a software tool that provides suggestions for items most likely of interest to a particular user."

The process consists of three sequential phases:

1. **Diagnose** — Automated extraction of program data and course descriptions from the institution's public catalog; topic modeling applied to course descriptions to generate interest topics.
2. **Feedback** — Interest topics are displayed to the student as word clouds; the student selects up to a maximum number of topics (parameter phi) that match their interests.
3. **Prescribe** — The backtracking algorithm computes relevance scores for all programs based on the selected topics and returns a ranked shortlist.

The core representational unit is the **interest topic**: a set of keywords derived from course descriptions that clusters semantically related content. Topics are not labels invented by the system designers but emerge from the data itself.

### 3.2 Program Data Processing

The input data structure comprises three entities:

- **P** — the set of all study programs (n programs total)
- **C** — the set of all courses (m courses total)
- **D** — the set of course descriptions, one per course

Courses and programs are connected by a many-to-many relationship **E**: a course may be mandatory (core) or optional (elective) in multiple programs. This structure forms a **bimodal directed network N** (the "knowledge map") with nodes in C and P and edges in E.

Each course description D_c is a text string, typically short (limited to 50 words in the case study). Course descriptions are not necessarily unique. After topic modeling extracts keywords, the system must be able to backtrack: given a keyword in a topic cluster, trace which course descriptions contain it, and then trace which programs include those courses. This chain — keyword → course → program — is the structural backbone of the scoring algorithm.

The authors note the system can be restricted to a subset of programs or extended to cover multiple universities.

### 3.3 Topic Modeling Method

The section provides a formal treatment of topic modeling terminology and then describes why BERTopic was chosen.

**General Topic Modeling Formalism:**

- A "word" is the fundamental unit of data.
- A "document" is a sequence of L words.
- A "corpus" is a collection of M documents.
- In this application, a course description is a document; the corpus is all course descriptions across all programs.
- A topic **z** is a probability distribution over the vocabulary.
- The per-topic word distribution is phi(z) = P(w|z).
- The per-document topic distribution is theta(d) = P(z|d).
- The goal of topic modeling is to infer these latent distributions from observed text.

**BERTopic Pipeline:**

BERTopic (Grootendorst 2022) operates as a sequential modular pipeline with five stages, each of which admits multiple options:

1. **Embeddings** — Pre-trained language models convert each document into a dense vector. Default: sentence-transformers (all-MiniLM-L6-v2 for English; paraphrase-multilingual-MiniLM-L12-v2 for multilingual settings supporting 50 languages).
2. **Dimensionality Reduction** — Reduces the dimensionality of embeddings to improve clustering efficiency. Default: UMAP (Uniform Manifold Approximation and Projection). Alternatives include PCA and t-SNE.
3. **Clustering** — Groups the reduced embeddings into topics. Default: HDBSCAN (Hierarchical Density-based Spatial Clustering of Applications with Noise). HDBSCAN uses soft clustering that allows noise points to be treated as outliers, producing more robust results than hard-assignment methods.
4. **Tokenization** — Converts clustered documents to token counts. Default: CountVectorizer (from scikit-learn).
5. **Weighting Scheme** — Identifies the most representative keywords for each cluster. Default: **c-TF-IDF** (Class-based Term Frequency-inverse Document Frequency). c-TF-IDF treats all documents in a cluster as a single document and computes TF-IDF relative to the entire corpus. A higher c-TF-IDF score means a word is more representative of its cluster. Optional post-hoc representation refinement can be performed using GPT, T5, KeyBERT, or SpaCy.

**Why BERTopic over LDA/NMF:**

BERTopic leverages contextual embeddings from BERT-style transformers, enabling understanding of word meaning in context rather than treating words as independent tokens. UMAP + HDBSCAN effectively handles complex and noisy data structures. c-TF-IDF improves topic interpretability. The framework integrates seamlessly with Python's Hugging Face Transformers library. BERTopic has shown success across tourism, social media, healthcare, and banking applications.

### 3.4 Topic Presentation and Interest Feedback

After topic modeling runs, the system pre-processes the output to remove technical artifacts from course descriptions: class type (lecture, laboratory), class mode (virtual, face-to-face), and prerequisite course listings. BERTopic assigns importance scores to keywords within each topic cluster based on c-TF-IDF values.

The top gamma keywords per topic are displayed to the user as **word clouds**, with word size and color proportional to each keyword's importance score within the topic. Word clouds are laid out in a space-optimized grid (mixing horizontal and vertical word orientations) and displayed in an arbitrary order to avoid ordering bias.

Students are asked to select up to phi topics (maximum) that match their personal interests. The selection interface is designed for use on both desktop computers and mobile devices.

### 3.5 Program Recommendation

The recommendation step uses a **network backtracking algorithm** (Algorithm 1) that traverses the knowledge map from selected topics back to programs. Three scoring metrics are computed for each program p:

1. **PIS (Program Interest Score)** — A raw count of how many times keywords from the user's selected interest topics appear across all course descriptions eligible within program p. Multiple occurrences in different courses are counted cumulatively.

2. **R-PIS (Relative Program Interest Score)** — PIS normalized by the total number of courses in program p. This correction prevents large programs (which have more courses and thus more keyword opportunities) from being systematically ranked higher simply due to size.

   R-PIS_p = PIS_p / |p|

3. **SCORE** — R-PIS scaled to the interval [0, 100] for display:

   SCORE_p = 100 * R-PIS_p / max_{q in R} R-PIS_q

The algorithm iterates over user-selected topics T, then over keywords w in each topic, then over all courses c, checking whether keyword w appears in the cleaned course description D*_c. If so, the PIS for every program associated with that course is incremented via the edge set E in network N. Programs with zero keyword overlap (R-PIS = 0) are excluded from recommendations. The final ranking returns the top tau programs.

The system parameters are:
- **h** — number of interest topics generated
- **gamma** — number of keywords per topic
- **phi** — maximum number of topics a user may select
- **tau** — number of programs returned in the ranked list

---

## 4. Case Study

The case study implements TopProRec on publicly available data from California Polytechnic State University (Cal Poly San Luis Obispo) for the 2021/22 academic year, then evaluates it with 65 users in an IRB-approved experiment.

### 4.1 Data Collection

The dataset covers:
- **84 programs** across 6 colleges (Agriculture, Food & Environmental Sciences; Engineering; Liberal Arts; Science and Mathematics; Architecture and Environmental Design; Business) plus Interdisciplinary Programs (one program: Liberal Arts and Engineering Studies).
- **4,251 course descriptions**, each capped at 50 words and averaging 42.3 words.
- **19,283 keywords** extracted, averaging 16.8 characters and ~2.0 words each.
- Programs ranged from 11 courses (Accounting) to 224 courses (Environmental Management and Protection), with a mean of 75.1 courses per program.
- Courses were associated with between 1 and 22 programs (mean 2.1 programs per course). Calculus IV, for example, appeared in 22 programs.
- The university's total enrollment was approximately 21,000 students.

The course-program bimodal network (the knowledge map) had 2,565 course nodes, 84 program nodes, and 6,143 edges. The paper illustrates this network visually (Fig. 5) using NetworkX for construction and yEd for layout, with the Louvain modularity method determining the organic clustering layout.

College course counts ranged from 1,768 (Agriculture, Food and Environmental Sciences) to 82 (Interdisciplinary Programs).

### 4.2 System Architecture and Interfaces

TopProRec is implemented as a modular four-component architecture:
1. **Data Management** — Data extraction and cleaning from public catalog sources (using Beautiful Soup for web scraping).
2. **Analytics Engine** — Topic modeling and recommendation computation.
3. **User Interface** — Two-screen interaction: (1) topic selection screen showing word cloud grid, (2) program ranking screen showing ranked shortlist with scores.

The user interface supports desktop and mobile form factors. After viewing recommendations, users can restart with a revised topic selection.

### 4.3 Implementation

The system was implemented in Python 3.10 on a MacOS machine (2.6 GHz 6-core Intel Core i7, 16 GB RAM). Key libraries:
- **Beautiful Soup** — web scraping of catalog data
- **NLTK** — preprocessing: tokenization, stop word removal, stemming, lemmatization
- **BERTopic v0.13.0** — topic modeling
- **scikit-learn CountVectorizer** — tokenization step within BERTopic
- **WordCloud** — word cloud visualization

System parameter values chosen for the case study:
- h = 30 (interest topics)
- gamma = 20 (keywords per topic)
- phi = 8 (maximum user-selected topics)
- tau = 7 (programs in final ranking)

### 4.4 A Real Recommendation Example

The section walks through a complete recommendation example for a fictitious student who selects five topics from the 30 generated: topics related to business/administration/government, networked systems/hardware, engineering/construction, statistical modeling/regression, and printing/packaging/supply chain.

For this selection, the backtracking algorithm returns a top-7 ranking (Table 4):

| Rank | Program | #Courses | PIS | R-PIS | SCORE |
|------|---------|----------|-----|-------|-------|
| 1 | Data Science | 21 | 113 | 5.381 | 100.0 |
| 2 | Bioinformatics | 16 | 86 | 5.375 | 99.9 |
| 3 | Industrial Engineering | 102 | 546 | 5.353 | 99.5 |
| 4 | Management and Human Resources | 14 | 73 | 5.214 | 96.9 |
| 5 | Manufacturing Engineering | 115 | 585 | 5.087 | 94.5 |
| 6 | Industrial Technology | 27 | 135 | 5.000 | 92.9 |
| 7 | Computer Science | 176 | 822 | 4.670 | 86.8 |

The authors note that although PIS scores vary widely (113 for Data Science vs. 822 for Computer Science), the R-PIS scores are consistently high across the top 6, with only Computer Science showing a meaningful drop, largely because its large course count (~176 courses) dilutes the relative score. The remaining 25 unselected word clouds are provided in Appendix A.

### 4.5 System Evaluation

The evaluation has two components: a quantitative analysis of system design properties and a qualitative analysis from a user survey.

#### 4.5.1 User Experiment Setup

64 students were randomly selected from 39 different majors. 50 were enrolled at Cal Poly; 14 were from other local colleges. Participation was voluntary with no incentive. Year distribution: 5 first-year, 22 second-year, 13 third-year, 14 fourth-year, 11 beyond. Each participant completed the full recommendation process (topic selection, then received ranked program list) and completed a survey. System parameters: h=30, gamma=20, phi=8, tau=7. Across all 65 users, 63 distinct programs were recommended at least once. Interdisciplinary Programs was never recommended, attributed to it containing only a single program.

#### 4.5.2 System Design Analysis

The section evaluates TopProRec against seven recommender system quality dimensions.

**Explainability**

The system generates a **topic score matrix** for any given recommendation. For a topic t and program p, the topic score is the normalized relative frequency of topic-t keywords in p's course descriptions. This matrix can be shown to users to explain why a specific program was or was not recommended. For example, in the worked example (Fig. 9), Topic 19 (networked systems) had zero presence in Management and Human Resources courses, while Topic 30 (printing/packaging) was almost entirely responsible for Industrial Technology's appearance in the ranking. The matrix also covers runner-up programs (Statistics, SCORE=0.859) and programs not recommended (Civil Engineering, History) to show the contrast.

**User Controllability**

The current system does not expose parameters to the user. The authors suggest possible extensions: allowing users to set the number of topics, filter by college or entry requirements, or include programs a priori. They note that topic modeling would need to be rerun if the program/course scope changes.

**Fairness**

Fairness is framed as **program reachability** (rho): the fraction of all programs that could theoretically appear in the top-tau ranking for some user-selected topic combination. A sensitivity analysis varies four parameters:
- h in {10, 20, 25, 30}
- phi in {1, ..., 6}
- gamma in {5, 10, 15, 20}
- tau in {3, 5, 7}

Reachability ranged from 16.7% (h=10, phi=6, gamma=15, tau=3) to 100% (h=30, phi=1, gamma=5, tau=7). The dominant factor was h: with h=10, maximum reachability was only 66.7%. The number of selected topics (phi) had an ambiguous effect depending on h. The number of keywords per topic (gamma) had minor and inconsistent effects. The authors recommend a configuration with rho > 90%, achievable with h in {25,...,30}, phi in {3,...,6}, gamma in {5,...,20}, and tau in {5,6,7}. They note these coverage values are high compared to typical collaborative filtering systems.

In the case study configuration (h=30, phi=8, gamma=20, tau=7), 98.8% of programs (83 of 84) were reachable. Only "Plant Sciences" could not appear in any ranking, likely due to course description characteristics.

**Robustness**

Changes in course descriptions could corrupt topic quality and recommendation results. The authors suggest periodic validation of keyword relevance, which could be supplemented by a brief post-recommendation user survey flagging irrelevant keywords.

**Bias and Privacy Protection**

Recommendations for distinct users are computed independently, so popular programs are surfaced only when the user's topic selection directly matches that program's content. User interests and recommendations are not shared with third parties.

**Personalization**

Personalization is quantified via the **cosine dissimilarity of recommendation vectors**. For each user u, a binary vector of length |P| encodes which programs were recommended. The average pairwise cosine similarity between all pairs of user recommendation vectors is computed; the personalization score is 1 minus this average similarity.

In the experiment, personalization score at the program level was **0.77** (high). At the college level, it was 0.48 (lower, attributed to only 7 colleges being available). There were 59 unique program recommendation profiles across 65 users (91%), with only 9 users sharing an identical program-level recommendation. This indicates the system produces meaningfully differentiated outputs.

**Trustworthiness**

The authors argue that coverage (fairness) supports trust by ensuring students see a fair cross-section of the institution, not a biased subset. Survey result in Question 6 (94%+ would use the tool in the future) is cited as evidence of practical trust. The fact that 98.1% of users saw their interests reflected in at least one recommendation (Question 2) reinforces user confidence.

#### 4.5.3 User Feedback

**Topic Usage Patterns:**
- Most popular topics: selected by 25 participants (39%).
- Least popular topic (Topic 30): never selected in the experiment, though it appeared in the example recommendation.
- Average topics selected per user: 4.9 (out of the maximum of 8).

**Binary Survey Questions (Table 5):**
- Q1 "My current program was recommended": 46.3% yes, 53.7% no. (Many participants' current programs were not recommended, which the authors attribute partly to students not having chosen their program based on interests.)
- Q2 "One or more recommended programs matched my interests": 98.1% yes, 1.9% no. (High validity indicator.)
- Q3 "There is an unexpected program I did not consider": 74.5% yes, 25.5% no. (Demonstrates serendipity.)
- Q4 "A program I would consider is not recommended": 57.4% yes, 42.6% no. (Indicates recall is imperfect, as expected for a top-7 shortlist.)

**Likert-Scale Questions (Table 6):**
- Q5 "I think this tool can be useful to select a major": 96.3% agree or strongly agree.
- Q6 "I would consider using this tool in addition to existing resources": 94.4% agree or strongly agree; one user strongly disagreed.
- Q7 "Interest word clouds were mostly meaningful": 92.6% agree or strongly agree.
- Q8 "It was easy to select interesting word clouds": 85.2% agree or strongly agree; 13% neutral.
- Q9 "Overall it was easy to use this tool": 100% agree or strongly agree.

**Qualitative User Comments (Table 7):**
Users found the concept innovative and the mapping of interests to specific programs particularly engaging. Common positive themes: the tool is especially valuable for undecided students, it surfaces unexpected programs, and some users wished they had had access to it when first applying to the university. Suggestions for improvement included: conducting a blind study to remove awareness-of-test bias; removing major names from word clouds to reduce anchoring; refining word cloud legibility (font choice, spacing); incorporating images in the clouds; weighting word importance more visibly; providing more explanation of how clusters were derived; allowing multiple recommendation rounds to progressively narrow options; and extending the system to recommend jobs and internships.

---

## 5. Conclusion

The conclusion summarizes the system's contributions and outlines directions for future work.

TopProRec is characterized as a novel information system for program selection that:
- Uses only publicly available course description data (no student records required).
- Operates in real time.
- Achieves both serendipity (surprising but relevant program discovery) and confirmation (validating programs already under consideration).
- Relies on the quality of course descriptions — a limitation explicitly acknowledged.

The case study findings are summarized: 98% program coverage (fairness), personalization score of 0.77, and strong user satisfaction in qualitative evaluation.

Directions identified for future research:
1. Extending to vocational and professional training settings.
2. Integrating course catalogs from multiple universities, as well as minors, certificates, and study abroad programs.
3. Providing recommendations at the individual course level.
4. Increasing user control (e.g., excluding topics or filtering by admission requirements).
5. Improving accuracy by using richer course data, including syllabi, class activities, and course materials.

---

## Appendices

**Appendix A** — All 30 interest topic word clouds from the case study (Fig. 12). Topics cover broad areas including: gender/history/culture; business/administration/government; healthcare/investigation; literature/writing; biology/teaching; music/performance; construction/architecture; environmental science; language/communication; media/journalism; financial/accounting; health/nutrition; dairy/food; electronics/signal processing; agribusiness; molecular chemistry; statistics/regression; plant science/horticulture; geoscience/water; mathematics; leadership/military; personnel/education; aerospace/aviation; printing/packaging. The diversity of topics reflects the full breadth of a polytechnic university's course offerings.

**Appendix B** — Complete binary recommendation matrices for the 65-user experiment. Includes:
- **M^{R,P}** (Fig. 13): 65-user by 84-program binary recommendation matrix showing which programs were recommended to which users.
- **M^{R,C}** (Fig. 14): 65-user by 7-college binary recommendation matrix, plus a full rank-level breakdown of how often each program appeared at ranks 1 through 7 across all users.

The college-level summary shows Liberal Arts (CLA) received the most total recommendations (195 program-level appearances across 7 ranks), followed by Business (91), Engineering (39), and Agriculture/Food/Environmental Sciences (53). Interdisciplinary Programs received zero recommendations. At the program level, Health and Society led with 39 appearances (Sigma), followed by Science, Technology and Society (38) and Global Citizenship and Social Sustainability (26).

**Appendix C** — Complete Program Interest Score (PIS) data (Table 8): a 84-program × 30-topic matrix reporting the raw keyword-match counts for every program across every interest topic, along with the total course count |p| for each program. This data enables full reproducibility of the scoring algorithm for any possible topic selection combination.

---

## Key Technical Details for Reference

- **BERTopic version used:** v0.13.0
- **Embedding model:** sentence-transformers (all-MiniLM-L6-v2 for English)
- **Dimensionality reduction:** UMAP
- **Clustering:** HDBSCAN
- **Tokenization:** CountVectorizer (scikit-learn)
- **Weighting:** c-TF-IDF
- **Case study system parameters:** h=30 topics, gamma=20 keywords/topic, phi=8 max selected topics, tau=7 recommended programs
- **Dataset:** Cal Poly SLO 2021/22; 84 programs, 4,251 course descriptions, 19,283 extracted keywords
- **Personalization score:** 0.77 (program level), 0.48 (college level)
- **Program reachability in case study configuration:** 98.8%
- **User experiment:** 65 students, 39 different majors, IRB-approved, voluntary participation
