import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt

# === Step 1: Set your VCF file path ===
vcf_path = "/Users/selina/Downloads/annotated_subject_2.vcf"  # <-- change if needed

# === Step 2: Initialize counters ===
chrom_counter = Counter()
gene_counter = Counter()
variant_type_counter = Counter()

# Regex to extract annotation (VEP-style ANN field)
ann_pattern = re.compile(r'ANN=([^;]+)')

# === Step 3: Parse the file line-by-line ===
with open(vcf_path, 'r') as file:
    for line in file:
        if line.startswith('#'):
            continue
        fields = line.strip().split('\t')
        chrom = fields[0]
        info = fields[7]

        # Count chromosome
        chrom_counter[chrom] += 1

        # Parse annotation (assuming VEP-style ANN field)
        match = ann_pattern.search(info)
        if match:
            annotations = match.group(1).split(',')
            for ann in annotations:
                parts = ann.split('|')
                if len(parts) > 3:
                    effect = parts[1]
                    gene_name = parts[3]
                    variant_type_counter[effect] += 1
                    gene_counter[gene_name] += 1

# === Step 4: Convert to DataFrames ===
variant_df = pd.DataFrame(variant_type_counter.items(), columns=['Variant_Type', 'Count']).sort_values(by='Count', ascending=False)
chrom_df = pd.DataFrame(chrom_counter.items(), columns=['Chromosome', 'Variant_Count']).sort_values(by='Variant_Count', ascending=False)
gene_df = pd.DataFrame(gene_counter.items(), columns=['Gene', 'Variant_Count']).sort_values(by='Variant_Count', ascending=False)

# === Step 5: Print results ===
print("\nTop 10 Variant Types:")
print(variant_df.head(10))

print("\nTop 10 Chromosomes with Most Variants:")
print(chrom_df.head(10))

print("\nTop 10 Genes with Most Variants:")
print(gene_df.head(10))

# === Optional: Export as CSV ===
variant_df.to_csv("variant_types_summary.csv", index=False)
chrom_df.to_csv("chromosome_variant_counts.csv", index=False)
gene_df.to_csv("top_genes_with_variants.csv", index=False)

# === Optional: Plot variant types ===
plt.figure(figsize=(10, 6))
plt.bar(variant_df['Variant_Type'].head(10), variant_df['Count'].head(10))
plt.title("Top 10 Variant Types")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_variant_types.png")
plt.show()
