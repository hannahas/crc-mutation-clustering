# CRC Mutation Clustering — Project Progress

## Project Overview
A clustering pipeline using somatic mutation profiles from colorectal cancer patients 
to recover known molecular subtypes and connect them to clinical outcomes.

**GitHub repo:** https://github.com/hannahas/crc-mutation-clustering

---

## Data Source
- **cBioPortal API** — TCGA Colorectal Adenocarcinoma PanCancer Atlas 2018
- **Study ID:** `coadread_tcga_pan_can_atlas_2018`
- 594 patients, 208,739 somatic mutations
- Clinical data: OS/DFS survival, tumor stage, molecular subtype (CIN, MSI, GS, POLE)
- Binary mutation matrix: 528 patients × top 100 most frequently mutated genes

---

## Files in Repo
- `scripts/fetch_data.py` — fetches clinical data, raw mutations, and builds mutation matrix via cBioPortal API
- `notebooks/analysis.ipynb` — full analysis notebook with visualizations
- `data/clinical.csv` — 594 patients × 42 clinical attributes
- `data/mutations_raw.csv` — 208,739 raw mutation records
- `data/mutation_matrix.csv` — binary 528 × 20,638 gene mutation matrix

---

## What We've Done

### Data exploration
- Mutation burden by subtype (log-scale boxplot + pie chart saved to `data/subtype_overview.png`)
- POLE: 1,708 avg mutations, MSI: 553, GS: 58, CIN: 56
- CIN dominates at 71.5% of patients, MSI 13.7%, GS 12.6%, POLE 2.2%

### Dimensionality reduction
- Filtered to top 100 most frequently mutated genes for clustering
- PCA with 50 components explains 79.5% of variance
- PC1 explains 25.9% — essentially a mutation burden axis
- PCA plot saved to `data/pca_clusters.png`

### Clustering
- K-means with k=4 (matching known number of subtypes)
- Silhouette score: 0.410
- Adjusted Rand Index vs true subtypes: 0.396
- Cluster 1 captured all CIN + GS patients (low mutation burden, indistinguishable)
- Clusters 0 and 3 split MSI patients — suggesting potential MSI subgroups
- Cluster 2 captured all POLE + extreme MSI outliers

### Survival analysis
- Kaplan-Meier style curves by subtype and by cluster
- GS subtype shows best long-term survival
- Survival curves saved to `data/survival_curves.png`

---

## What's Next
1. Stage distribution by cluster — bar charts of AJCC stage per cluster
2. Driver gene heatmap — which genes are most mutated in each cluster
3. README — document the project
4. Narrative notebook writeup — same approach as pubmed-health-insights project

---

## Python Environment
- Python 3.14
- venv located at `~/Desktop/crc-mutation-clustering/venv`
- Key packages: pandas, numpy, scikit-learn, matplotlib, seaborn, requests, jupyter
