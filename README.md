# CRC Mutation Clustering

An unsupervised machine learning pipeline that clusters colorectal cancer patients 
by somatic mutation profiles and connects those clusters to known molecular subtypes 
and clinical outcomes.

---

## Motivation

Colorectal cancer is not one disease — it is at least four molecularly distinct 
subtypes with different mutation profiles, clinical behaviors, and responses to 
treatment. The key subtypes are:

- **CIN** (Chromosomal Instability) — most common, APC/TP53-driven, moderate mutation burden
- **MSI** (Microsatellite Instable) — mismatch repair deficiency, hypermutated, responds to immunotherapy
- **GS** (Genomically Stable) — low mutation burden, early stage presentation
- **POLE** (Polymerase epsilon mutated) — ultra-hypermutated, extreme mutation burden

This project asks: **can unsupervised clustering of somatic mutation profiles recover 
these known subtypes — and do the resulting clusters predict clinical outcomes like 
tumor stage and survival?**

---

## Pipeline Overview

    cBioPortal API  →  Mutation matrix  →  PCA  →  K-means clustering
                            +                              ↓
                      Clinical data          Clinical outcome analysis
                                         (survival, stage, driver genes)

**Step 1 — Data ingestion (`scripts/fetch_data.py`)**  
Fetches 594 patients and 208,739 somatic mutations from the TCGA Colorectal 
Adenocarcinoma PanCancer Atlas via the cBioPortal REST API. Builds a binary 
mutation matrix (1 = mutated, 0 = not mutated) per patient per gene.

**Step 2 — Dimensionality reduction**  
Filters to the top 100 most frequently mutated genes, scales with StandardScaler, 
and reduces to 50 PCA components (explaining 79.5% of variance).

**Step 3 — Clustering**  
K-means clustering with k=4 (matching the known number of molecular subtypes). 
Evaluated with silhouette score and Adjusted Rand Index against known labels.

**Step 4 — Clinical outcome analysis**  
Connects clusters to AJCC tumor stage, overall survival, and driver gene mutation 
frequencies to validate biological interpretability.

---

## Key Findings

**Mutation burden separates subtypes by orders of magnitude.**  
PC1 (25.9% of variance) is essentially a mutation burden axis. POLE tumors average 
1,708 mutations, MSI averages 553, while CIN and GS average ~57 — a 30-fold difference.

**Unsupervised clustering recovers known biology.**  
K-means achieved a silhouette score of 0.410 and Adjusted Rand Index of 0.396 against 
known subtypes. Cluster 1 captured all CIN and GS patients; Cluster 2 isolated POLE 
and extreme MSI outliers; Clusters 0 and 3 split MSI patients into two subgroups.

**The driver gene heatmap confirms subtype identity.**  
Cluster 1 (CIN/GS) is defined by APC (78%) and TP53 (63%) — the canonical CRC driver 
pathway. Clusters 0 and 3 (MSI) are defined by large passenger genes (TTN, MUC16, SYNE1) 
that accumulate mutations due to mismatch repair deficiency. Cluster 2 (POLE) shows 
near-universal mutation across all genes.

**MSI tumors present at earlier stages.**  
Consistent with known biology, MSI and GS subtypes skew toward Stage I and IIA, 
while CIN tumors are more evenly distributed across stages including later Stage IIIB.

**GS subtype shows best long-term survival.**  
Survival curves show GS patients have a notably elevated long-term survival tail 
compared to CIN and MSI — consistent with their early-stage presentation and 
lower metastatic potential.

---

## Results

| Metric | Value |
|---|---|
| Patients | 528 |
| Mutations | 208,739 |
| Genes used for clustering | 100 |
| PCA components | 50 (79.5% variance) |
| Silhouette score | 0.410 |
| Adjusted Rand Index | 0.396 |

---

## How to Run

**1. Clone the repo and set up the environment**
```bash
git clone https://github.com/hannahas/crc-mutation-clustering.git
cd crc-mutation-clustering
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Fetch data from cBioPortal**
```bash
python3 scripts/fetch_data.py
```

**3. Open the analysis notebook**
```bash
jupyter notebook notebooks/analysis.ipynb
```

---

## Tech Stack

| Component | Tool |
|---|---|
| Data source | cBioPortal REST API (TCGA COADREAD) |
| Data manipulation | pandas, numpy |
| Dimensionality reduction | scikit-learn PCA |
| Clustering | scikit-learn K-means |
| Evaluation | silhouette score, Adjusted Rand Index |
| Visualization | matplotlib, seaborn |
| Environment | Python 3.14, venv |
| Version control | Git / GitHub |

---

## Next Steps

- [ ] Hierarchical clustering as an alternative to K-means
- [ ] Survival analysis with proper Kaplan-Meier estimator (lifelines library)
- [ ] Extend to other cancer types for comparison
- [ ] Investigate the MSI subgroup split — are Clusters 0 and 3 biologically distinct?

---

## Author

Alexander Hannah, PhD  
Computational biologist and data scientist  
[github.com/hannahas](https://github.com/hannahas)
