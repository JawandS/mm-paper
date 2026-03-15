# Using Embeddings to Uncover the Similarity Between Engineering Education Doctoral Programs and Academic Workforce Opportunities

## Metadata

- **Authors:** Malini Josiam (Virginia Tech, Department of Engineering Education), Olivia Ryan (Virginia Polytechnic Institute and State University), Varun Sridhar (Independent Researcher)
- **Year:** 2025
- **Venue:** 2025 ASEE Annual Conference & Exposition, Palais des congrès de Montréal, Montréal, QC, June 22–25, 2025
- **Paper ID:** #45520
- **DOI:** Not explicitly provided in the paper
- **Paper type:** Full methods paper

---

## Introduction and Background

The paper opens by situating the work in the context of AI's growing role in education research. The authors note calls in the literature for novel research demonstrating the efficacy of generative AI, and for scholars to document best practices and present case studies of its application in engineering education specifically.

The introduction provides a working explanation of embeddings and cosine similarity. Embedding models take raw objects (text, images, etc.) as input and produce dense vector representations in a high-dimensional space, such that similar objects land near one another in that space. Sentence embedding models take a sentence or paragraph as input and produce a single embedding as output. Cosine similarity measures the angular similarity between two vectors, yielding a score bounded between -1 and 1; it is scale-invariant, interpretable, and well-suited to high-dimensional spaces. The key claim is that quantifying otherwise qualitative similarity judgments via these techniques enables faster and more automated analysis.

The domain context is Engineering Education (EngE) as an academic field. EngE emerged as a distinct research discipline in the early 2000s, shifting away from a purely pedagogical orientation. Around the same time, newly formed EngE academic units began offering doctoral degrees designed to prepare students for faculty careers, emphasizing candidates who combined engineering disciplinary knowledge with expertise in pedagogy and assessment. Scholars subsequently worked to define the boundaries of the field, but a persistent tension has remained between those who prioritize engineering teaching practice and those who prioritize EngE as a research enterprise.

Despite this ongoing tension, EngE doctoral programs have proliferated. As of 2022, 15 programs in the U.S. offered PhDs in EngE or closely related disciplines, and the field has grown substantially over the preceding decade. As more students earn terminal degrees in EngE, the demand for relevant academic jobs grows. Yet, the authors observe, relatively little is known about how program outcomes (POs) — the explicit competency goals doctoral programs publish — align with what the academic job market actually requires.

Prior work in the area includes word embeddings applied to EngE classroom contexts, sentence embeddings used to train course syllabi and analyze instructional material, sentence embeddings for thematic analysis of open-ended student responses, and sentence embeddings applied to job posting qualifications in other education technology contexts. The current paper contributes to this body by integrating traditional qualitative coding with sentence embeddings and cosine similarity to compare two textual data sources: EngE doctoral POs and EngE academic job postings.

The authors identify their positionality explicitly: two of the three authors are doctoral candidates in EngE who have personal stakes in understanding how their training maps onto the academic job market. They partnered with an industry machine learning engineer who provided technical AI expertise but had no prior EngE-specific experience.

---

## Purpose and Research Questions

The stated purpose is to demonstrate the utility of integrating qualitative coding, sentence embeddings, and cosine similarity for illuminating similarities and differences among EngE doctoral programs in terms of their alignment with the EngE academic job market.

The study addresses three research questions:

1. What are current EngE PhD graduates prepared to do?
2. What academic job opportunities are available in the field of EngE?
3. How do the program outcomes (POs) and the required qualifications of academic job opportunities compare?

---

## Methods

### Overview

The study is an exploratory qualitative study using publicly available data. Traditional qualitative data analysis addresses RQ1 and RQ2. NLP-assisted qualitative data analysis addresses RQ3. The two primary datasets are program information and job postings, both sourced initially from the Engineering Education List wiki (the "EngE wiki"), a community-maintained resource.

### Program Information

The authors selected programs that were: active, listed in the EngE Departments and Programs (Graduate) section of the EngE wiki, based in the U.S., and offering a doctoral degree in EngE or a closely related discipline (e.g., Engineering and Science Education) as of April 2024. Programs offering only STEM education degrees were excluded. This yielded 13 programs. Programs without publicly available POs were then excluded, reducing the dataset to 12 programs across 12 institutions.

The 12 programs (listed in Appendix I of the paper) are:
- Clemson (Ph.D. Engineering and Science Education, enrollment 25)
- Florida International University (Ph.D. Engineering and Computing Education, enrollment 19)
- Mississippi State University (Ph.D. Engineering Education, enrollment unknown)
- Purdue University (Ph.D. Engineering Education, enrollment 75)
- The Ohio State University (Ph.D. Engineering Education, enrollment 24)
- University at Buffalo (Ph.D. Engineering Education, enrollment unknown)
- University of Colorado Boulder (Ph.D. Engineering Education, enrollment unknown)
- University of Florida (Ph.D. Engineering Education, enrollment 11)
- University of Michigan (Ph.D. Engineering Education Research, enrollment 13)
- University of Nebraska Lincoln (Ph.D. Engineering Education Research, enrollment 11)
- Utah State University (Ph.D. Engineering Education, enrollment 23)
- Virginia Tech (Ph.D. Engineering Education, enrollment 54)

Preliminary data collected for each program included its name, degree name, enrollment size, and POs.

### Job Postings

Job postings were downloaded from the EngE wiki on April 8, 2024. The wiki's job board includes both current and historical postings, covering positions between January 2023 and April 2024. For each posting, the authors recorded institution, department, location (zip code), and position title. Required and desired qualifications were retrieved via links in the wiki. Postings for which the original post or qualifications could not be found were excluded. The final job dataset comprised 95 postings.

### Qualitative Coding

The first and second authors independently coded each PO using emergent codes following Saldaña's coding manual. A second round of coding consolidated codes into nine categories: career, DEI, discrepancy, engineering expertise, engineering education issues, professional development, research, teaching, and other. The "discrepancy" category captured cases where the two coders disagreed.

Job postings were also independently coded to categorize position titles into: open rank, assistant professor, associate professor, post doc, director/assistant director, unranked teaching faculty, admin (department head/chair), and other.

### Embedding and Cosine Similarity Analysis (RQ3)

The third author conducted the NLP-assisted analysis. The chosen embedding model was **all-MiniLM-L6-v2**, a sentence embedding model trained on diverse English Internet text (Reddit, Stack Exchange, Yahoo Answers). The authors considered all-MiniLM-L12-v2 and all-mpnet-base-v2 but selected all-MiniLM-L6-v2 for its best balance of performance, runtime, and computational cost.

The procedure was:
1. Concatenate all POs for a given program into one input and generate one sentence embedding per program (12 embeddings total).
2. Concatenate required and desired qualifications for each job posting and generate one sentence embedding per job posting (95 embeddings total).
3. Compute cosine similarity between each program embedding and each job posting embedding, producing a 12 × 95 matrix of similarity scores.

The authors focused interpretation on scores at or above 0.5, treating lower scores as too noisy to draw reliable conclusions from, citing limitations in embedding representations and noise in input text.

### Human-in-the-Loop Validation

To verify the AI method's validity, the authors used qualitative human-in-the-loop evaluation. They noted that University of Colorado Boulder and Mississippi State University had nearly identical POs and confirmed that the cosine similarity between those two programs' embeddings was 0.95 — consistent with expected near-identity. They also verified that both programs received very similar similarity scores against each job posting, with minor variation (0.05–0.1) attributable to verbiage differences that did not materially affect conclusions about strong versus weak alignment.

### Visualization Tools

Geographic visualizations were produced in Python using the Folium library (program locations) and Plotly (job posting heatmap by county). Zip codes were converted to FIPS codes using the zip2fips GitHub repository.

The full pipeline (data gathering → qualitative coding → sentence embeddings → cosine similarity) is summarized in Figure 1 of the paper.

---

## Positionality

The two doctoral candidate authors are embedded in EngE and have direct interest in entering the academic job market; their motivation was partly practical (they read *The Professor Is In* and took a graduate course in education assessment). The industry MLE co-author provided technical expertise without EngE domain knowledge. The authors disclose these positions to acknowledge how their perspectives shaped the research design and interpretation.

---

## Limitations

The authors identify three categories of limitation.

**Limitations from using POs as a proxy for program preparation.** POs are only partial indicators of how programs train students. Doctoral education is highly individualized; the same program can produce students with very different teaching and research experiences depending on advisor, department climate, and research group. Students also pursue individual experiences outside the program. POs represent stated priorities, not guaranteed training. At the same time, the authors affirm that POs remain valuable because they should drive outcome-based program assessment and alignment of coursework, milestones, and assistantships.

**Limitations from the job posting data.** The authors used a single source (the EngE wiki job board), which compiled academic opportunities but not positions in industry, government, or other sectors that EngE graduates pursue. The required and desired qualifications used in the analysis do not capture the full scope of a position. Data collection in April 2024 meant that fall 2023 postings may have been removed, so the dataset likely underrepresents a full academic hiring cycle. Results reflect the market in early 2024 and should not be generalized to any other year.

**Limitations from the embedding approach.** Cosine similarity below 0.5 is too noisy to interpret meaningfully, leaving approximately one-third of the job-posting similarity scores uninterpreted. The method is well-suited for identifying high similarity but cannot unpack the reasons for low similarity. The authors note that direct comparison of two close scores (e.g., 0.95 vs. 0.93) cannot reliably indicate which program is more aligned with a given posting; only aggregate patterns are robust enough to support conclusions.

Despite these limitations, the authors argue their study demonstrates the viability of integrating qualitative coding with embedding similarity for large-scale qualitative data analysis.

---

## Findings

### Finding 1: Program Outcomes Are Overwhelmingly Research and Teaching Focused

Across 67 total POs from 12 programs, research (18 POs) and teaching (16 POs) were by far the most common categories, together accounting for 50% of all POs. The remaining categories and their counts were:

| Category | Count |
|---|---|
| research | 18 |
| teaching | 16 |
| professional development | 6 |
| discrepancy | 6 |
| other | 7 |
| career | 4 |
| DEI | 4 |
| engineering education issues | 4 |
| engineering expertise | 3 |

The 21 POs (31%) in the categories of career, DEI, engineering expertise, engineering education issues, and professional development represent a secondary but meaningful cluster. The remaining 13 POs (19%) were either contested between coders (6) or did not fit any established category (7).

All 12 programs had at least one research-related PO, but not all had a teaching-focused PO; 10 of the 12 did. Most programs (83%) had POs spanning four or fewer categories.

The distribution of PO categories was uneven across programs. Programs like Purdue University had 15 POs spanning 7 categories — the most expansive in the dataset — while programs like University of Michigan had only 3 POs in 3 categories, all narrowly focused on research output (publishing, grant competition) and career entry.

### Finding 2: Academic Job Postings Are Largely for Entry-Level Doctoral Opportunities

Of the 95 job postings, approximately 70% were entry-level positions accessible to a recent PhD graduate. The breakdown by category was:

- Open rank: 29% (most common, approximately 28 postings)
- Assistant professor: 16% (approximately 15 postings)
- Other: 15%
- Postdoc: 15%
- Director/assistant director: smaller proportion
- Unranked teaching faculty: smaller proportion
- Admin (department head/chair): small
- Associate professor: small (fewest)

Geographically, states with the highest concentration of job postings included California, Arizona, Texas, and Virginia.

### Finding 3: Alignment Between Program Outcomes and Job Posting Qualifications Varies Significantly by Program

The embedding similarity analysis identified substantial variation in how well different programs' POs aligned with the job market. Programs were ranked by the number of times their POs scored highest in cosine similarity against a given job posting. The results, shown in Figure 5 of the paper, included only the seven programs that were ranked first at least once.

University of Nebraska Lincoln was the top-ranked program most frequently, having the highest similarity score for 25 of the 95 job postings and aligning with all eight position title categories. Five programs never held the top rank for any posting.

For a more comprehensive measure of alignment, the authors counted the number of job postings for which each program achieved a cosine similarity of 0.5 or above. Results from Appendix IV:

| Program | # POs | # PO Categories | # Similarity Scores ≥ 0.5 |
|---|---|---|---|
| University of Nebraska Lincoln | 5 | 4 | 44 |
| University at Buffalo | 6 | 5 | 40 |
| Clemson | 7 | 4 | 37 |
| Utah State University | 4 | 3 | 36 |
| Florida International University | 4 | 4 | 35 |
| The Ohio State University | 4 | 3 | 33 |
| University of Colorado Boulder | 5 | 3 | 30 |
| Virginia Tech | 7 | 4 | 26 |
| University of Michigan | 3 | 3 | 24 |
| Mississippi State University | 6 | 3 | 22 |
| University of Florida | 3 | 3 | 22 |
| Purdue University | 15 | 7 | 7 |

Every program had some alignment (≥ 0.5) with at least 7 job postings. Eleven of the 12 programs had alignment with at least 22 postings (23% of the dataset). Purdue University was a notable outlier: despite having the most POs (15) across the most categories (7), it had the fewest high-similarity matches (7). This directly illustrates a key finding — the volume or breadth of POs does not predict job market alignment.

---

## Discussion and Implications

The discussion integrates all three findings and draws out practical and methodological implications.

**On the substantive findings.** The predominance of research and teaching POs across programs reflects the longstanding dual mandate of EngE doctoral education. Given that approximately 70% of available academic jobs are entry-level positions a new PhD could fill (postdoc, assistant professor, unranked teaching faculty), the general focus of POs on research and teaching is directionally sensible. However, the wide variation in alignment scores suggests that some programs' POs are better calibrated to the job market than others, and that this cannot be fixed simply by adding more POs or broadening categories. Purdue's low alignment score despite its breadth illustrates that more is not always better.

The authors recommend that EngE programs, department chairs, and program heads use AI-driven techniques like this one to regularly review and update their POs against current job market demands. This complements prior research showing that early-career EngE researcher positions exist across a variety of institutional types and roles, underlining the need for broad but targeted preparation.

**On the methodological contribution.** The authors argue that embeddings and cosine similarity are valuable additions to qualitative data analysis, with an important caveat: they must be used in aggregate and interpreted with human judgment. A difference of 0.02 between two scores (e.g., 0.95 vs. 0.93) should not be taken as evidence that one program is more aligned than another given noise and limitations of cosine similarity. Aggregate measures — such as counting the number of postings above a threshold — produce interpretable and meaningful patterns.

The authors characterize this approach as best suited for "decontextualized" structured text data, contrasting it with highly contextualized data such as interview or focus group transcripts, which require reflexivity and interpretive depth that AI cannot replicate. They explicitly caution that AI-assisted analysis can reinforce existing biases, citing the "stochastic parrots" literature.

**On broader applicability.** The authors suggest the embedding similarity method could be applied to other large-scale EngE research questions, including evaluating alignment between course learning outcomes and ABET accreditation criteria, evaluating course syllabi, or analyzing structured student reflections. They note that embeddings are gaining traction in the EngE research community, citing a 2024 survey of embedding applications in engineering education research.

---

## Conclusion

The authors conclude that integrating qualitative coding, sentence embeddings, and cosine similarity is a feasible and promising approach for evaluating large qualitative datasets in EngE research. The specific findings — that EngE doctoral POs are predominantly research and teaching focused, that the EngE academic job market is dominated by entry-level positions, and that PO-to-job-market alignment varies substantially across programs — are presented as actionable for program administrators. The overarching methodological lesson is that AI results in this domain are meaningful when contextualized by human judgment and interpreted through aggregation rather than raw score comparison.

---

## Appendices (Summary)

**Appendix I** lists the 12 programs, their zip codes, the specific degree offered, and 2024 enrollment sizes where known. Enrollments ranged from 11 (University of Florida; University of Nebraska Lincoln) to 75 (Purdue University); Virginia Tech was second largest at 54.

**Appendix II** provides a map showing the geographic distribution of the 12 programs across the continental U.S., concentrated in the Midwest, South, and East.

**Appendix III** provides the full text of each program's POs and their assigned categories, covering all 12 programs. The table reveals significant variation in the specificity and language of POs: some programs state concrete outcomes (e.g., University of Michigan: "publish in top tier engineering education and education journals; compete for federal grants and contracts"), while others use broader competency language. University of Colorado Boulder and Mississippi State University have nearly identical PO text, which the authors used as the basis for their human-in-the-loop validation of the embedding method (confirmed cosine similarity of 0.95 between the two programs).

**Appendix IV** presents the per-program table of number of POs, number of PO categories, and number of similarity scores ≥ 0.5 with job postings, along with a dot plot visualizing all three variables simultaneously for each program. The visualization makes the lack of correlation between PO breadth and job alignment scores visually apparent, particularly in the case of Purdue University.
