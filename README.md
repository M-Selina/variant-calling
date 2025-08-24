## Variant Calling & Interpretation Project

## Overview

This project presents the variant calling and interpretation workflow I applied to a multi-sample VCF dataset from a study on chronic immune dysregulation. The work covers the end-to-end pipeline from variant annotation to biological interpretation and therapeutic implications, with results and reasoning supported by literature and database references.

## Dataset

- Input: Multi-sample VCF (variants pre-annotated with gene names, variant consequences, allele changes, genomic coordinates, depth, and quality metrics).
- Disease context: Chronic immune dysregulation (polygenic, inflammatory pathways suspected).

## Analysis Workflow

# Variant Landscape

- Most common variant classes: intronic, upstream, downstream, missense, synonymous.

- Chromosomes with highest variant density: Chr1, Chr2, Chr3, Chr12, Chr17, Chr11, Chr4, Chr10, Chr19, Chr14.

- Top recurrent genes:

-- ZEB2 (20,618 variants)

-- FOXP1 (9,330)

-- PSEN1 (8,455)

-- PCBP1-AS1 (8,061)

-- NFE2L2 (7,994)

-- CD44 (7,600)

-- CCDC88A, ANKRD11, MBNL1, NFKB1

Interpretation: High missense/synonymous ratio suggests a mix of neutral and deleterious germline variants. Enrichment in immune and transcriptional regulators points to pathways relevant in autoimmunity or oncogenesis
.

# Variant Prioritization

Selected variants based on pathogenicity, functional consequence, recurrence, and disease relevance.

Examples:

- ISG15: Cluster of 9 missense variants within ~300 bp (potential hotspot; IFN signaling, innate immunity).

- SDF4: Calcium-binding & ER stress response; moderate impact.

Rationale: Both implicated in immune regulation and inflammation
.

## Disease Hypothesis

- Variants in ISG15 strongly suggest interferonopathy-related immune dysfunction or susceptibility to infection/autoimmunity.

- Supported by OMIM (#147571) and PubMed (PMIDs: 25642612, 22798673).

- SDF4 involvement may point to ER-stress–linked disorders (metabolic or cancer contexts).

## Therapeutic Implications

ISG15 is a potential target:

- Precise correction via base or prime editing could restore normal function.

- Full knockout considered risky due to ISG15’s essential antiviral role.

Concerns:

- Off-target edits (CRISPR/Cas9, base editors).

- Overexpression risks → autoimmunity or chronic inflammation.

- Vector delivery challenges (immune response to AAV/lentivirus).

## Tools & Methods

- VCF processing & statistics: Python (pandas, collections, re)

- Variant effect prediction: pre-annotated VCF (SnpEff/VEP style)

- References used: OMIM, ClinVar, PubMed, Ensembl

## References

- OMIM #147571, #616126

- PubMed: 25642612, 22798673, 31980635

- GATK Best Practices

- Ensembl VEP documentation

