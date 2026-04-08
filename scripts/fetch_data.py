import requests
import pandas as pd
import time

BASE_URL = "https://www.cbioportal.org/api"
STUDY_ID = "coadread_tcga_pan_can_atlas_2018"

def get_all_samples():
    """Fetch all sample IDs for the CRC study."""
    url = f"{BASE_URL}/studies/{STUDY_ID}/samples"
    r = requests.get(url, headers={"Accept": "application/json"},
                     params={"pageSize": 10000})
    samples = r.json()
    print(f"Total samples: {len(samples)}")
    return [s["sampleId"] for s in samples]


def get_clinical_data():
    """Fetch clinical data for all patients."""
    url = f"{BASE_URL}/studies/{STUDY_ID}/clinical-data"
    r = requests.get(url, headers={"Accept": "application/json"},
                     params={"clinicalDataType": "PATIENT", "pageSize": 100000})
    data = r.json()
    print(f"Clinical attributes fetched: {len(data)}")

    # Pivot from long to wide format
    records = {}
    for item in data:
        pid = item["patientId"]
        if pid not in records:
            records[pid] = {}
        records[pid][item["clinicalAttributeId"]] = item["value"]

    df = pd.DataFrame.from_dict(records, orient="index")
    df.index.name = "patientId"
    df.reset_index(inplace=True)
    return df


def get_mutation_counts():
    """Fetch mutation counts per gene per sample."""
    # First get all sample IDs
    samples = get_all_samples()
    
    url = f"{BASE_URL}/mutations/fetch"
    payload = {
        "sampleIds": samples,
        "studyId": STUDY_ID
    }
    r = requests.post(
        f"{BASE_URL}/molecular-profiles/{STUDY_ID}_mutations/mutations/fetch",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={"sampleIds": samples},
        params={"pageSize": 500000}
    )
    data = r.json()
    print(f"Total mutations fetched: {len(data)}")
    print(f"First record type: {type(data[0])}")

    records = []
    for m in data:
        # Extract gene symbol from keyword field (e.g. "APC truncating" -> "APC")
        keyword = m.get("keyword", "")
        gene = keyword.split()[0] if keyword and keyword != "." else str(m.get("entrezGeneId", "unknown"))
        
        # Calculate VAF from alt/ref counts
        alt = m.get("tumorAltCount", 0) or 0
        ref = m.get("tumorRefCount", 0) or 0
        vaf = alt / (alt + ref) if (alt + ref) > 0 else None

        records.append({
            "sampleId": m["sampleId"],
            "patientId": m["patientId"],
            "gene": gene,
            "mutationType": m.get("mutationType", ""),
            "variantAlleleFreq": vaf
        })

    return pd.DataFrame(records)


def build_mutation_matrix(mutations_df):
    """Build binary gene x sample mutation matrix."""
    # 1 = mutated, 0 = not mutated
    matrix = mutations_df.groupby(["sampleId", "gene"]).size().unstack(fill_value=0)
    matrix = (matrix > 0).astype(int)
    print(f"Mutation matrix shape: {matrix.shape}")
    return matrix


if __name__ == "__main__":
    print("Fetching clinical data...")
    clinical_df = get_clinical_data()
    clinical_df.to_csv("data/clinical.csv", index=False)
    print(f"Saved clinical data: {clinical_df.shape}")
    print(f"Clinical columns: {clinical_df.columns.tolist()[:15]}")

    print("\nFetching mutation data...")
    mutations_df = get_mutation_counts()
    mutations_df.to_csv("data/mutations_raw.csv", index=False)
    print(f"Saved raw mutations: {mutations_df.shape}")

    print("\nBuilding mutation matrix...")
    matrix = build_mutation_matrix(mutations_df)
    matrix.to_csv("data/mutation_matrix.csv")
    print(f"Saved mutation matrix: {matrix.shape}")

    print("\nDone!")