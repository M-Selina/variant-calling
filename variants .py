import pandas as pd
import requests
import time

# Your variants list (you can also read from a CSV or Excel file)
variants = [
    "chr1:g.1014090G>T",
    "chr1:g.1014138C>G",
    "chr1:g.1014188A>G",
    "chr1:g.1014204T>A",
    "chr1:g.1014287A>C",
    "chr1:g.1014290G>A",
    "chr1:g.1014297A>C",
    "chr1:g.1014339A>C",
    "chr1:g.1014396A>G"
]

def fetch_annotations(variant_list):
    """Fetches variant annotations from MyVariant.info API in batches."""
    url = "https://myvariant.info/v1/variant"
    annotations = []
    
    for i in range(0, len(variant_list), 5):
        batch = variant_list[i:i+5]
        response = requests.post(f"{url}/batch", json={"ids": batch})
        if response.ok:
            annotations.extend(response.json())
        else:
            print("Error fetching:", response.text)
        time.sleep(1)  # prevent throttling

    return annotations

# Run the query
results = fetch_annotations(variants)

# Process the results
records = []
for res in results:
    record = {
        "query": res.get("query"),
        "variant_id": res.get("_id"),
        "gene": res.get("gene", {}).get("symbol"),
        "clinvar_clinsig": res.get("clinvar", {}).get("clinical_significance"),
        "clinvar_trait": res.get("clinvar", {}).get("trait"),
        "rsid": res.get("dbsnp", {}).get("rsid"),
        "cadd_phred": res.get("cadd", {}).get("phred"),
        "polyphen_pred": res.get("snpeff", {}).get("ann", [{}])[0].get("polyphen_prediction"),
        "sift_pred": res.get("snpeff", {}).get("ann", [{}])[0].get("sift_prediction"),
    }
    records.append(record)

# Convert to DataFrame
df = pd.DataFrame(records)
print(df)

# Optional: save to Excel
df.to_excel("isg15_variant_annotations.xlsx", index=False)
