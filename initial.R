vcf <- read.table("/Users/selina/Downloads/annotated_subject_2.vcf", sep = "\t", header = FALSE, comment.char = "#", stringsAsFactors = FALSE)
colnames(vcf) <- c("CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT", "SAMPLE")

# Extract Annotation and Gene Name
extract_ann <- function(info_string) {
  match <- regmatches(info_string, regexpr("ANN=[^;]+", info_string))
  if (length(match) > 0) {
    ann <- strsplit(gsub("ANN=", "", match), ",")[[1]][1]
    fields <- strsplit(ann, "\\|")[[1]]
    return(c(fields[2], fields[4]))  # Annotation, Gene Name
  } else {
    return(c(NA, NA))
  }
}

annotations <- t(apply(vcf, 1, function(row) extract_ann(row["INFO"])))
vcf$Annotation <- annotations[,1]
vcf$Gene <- annotations[,2]


library(tidyr)
library(dplyr)

# Filter for non-NA genes
vcf_clean <- vcf %>% filter(!is.na(Gene))

# Count variants per gene per chromosome
gene_chr_matrix <- vcf_clean %>%
  count(Gene, CHROM) %>%
  tidyr::pivot_wider(names_from = CHROM, values_from = n, values_fill = 0) %>%
  as.data.frame()  # convert tibble to regular data.frame

rownames(gene_chr_matrix) <- gene_chr_matrix$Gene
gene_chr_matrix <- gene_chr_matrix[, -which(names(gene_chr_matrix) == "Gene")]



library(ggplot2)
library(dplyr)
library(tidyr)
library(reshape2)

# Convert scaled matrix (with rownames = genes) to long format
scaled_matrix <- scale(gene_chr_matrix[, -ncol(gene_chr_matrix)])  # excluding Cluster
heatmap_df <- as.data.frame(scaled_matrix)
heatmap_df$Gene <- rownames(gene_chr_matrix)
heatmap_df$Cluster <- as.factor(gene_chr_matrix$Cluster)

# Reshape to long format for ggplot
heatmap_long <- melt(heatmap_df, id.vars = c("Gene", "Cluster"), variable.name = "Chromosome", value.name = "Zscore")

# Optional: reorder genes by cluster
heatmap_long$Gene <- factor(heatmap_long$Gene, levels = heatmap_df$Gene[order(heatmap_df$Cluster)])

ggplot(heatmap_long, aes(x = Chromosome, y = Gene, fill = Zscore)) +
  geom_tile() +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
  facet_grid(Cluster ~ ., scales = "free_y", space = "free") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 5),
        axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(title = "Gene Variant Distribution by Cluster",
       x = "Chromosome",
       y = "Gene")
print(
  ggplot(heatmap_long, aes(x = Chromosome, y = Gene, fill = Zscore)) +
    geom_tile() +
    scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
    facet_grid(Cluster ~ ., scales = "free_y", space = "free") +
    theme_minimal() +
    theme(axis.text.y = element_text(size = 5),
          axis.text.x = element_text(angle = 45, hjust = 1)) +
    labs(title = "Gene Variant Distribution by Cluster",
         x = "Chromosome",
         y = "Gene")
)

dim(heatmap_long)
head(heatmap_long)

subset_data <- heatmap_long %>% filter(Gene %in% unique(Gene)[1:30])

ggplot(subset_data, aes(x = Chromosome, y = Gene, fill = Zscore)) +
  geom_tile() +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
  facet_grid(Cluster ~ ., scales = "free_y", space = "free") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 6),
        axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(title = "Top 30 Genes Heatmap by Chromosome",
       x = "Chromosome",
       y = "Gene")
ggsave("gene_cluster_heatmap.png", width = 10, height = 8, dpi = 300)

print(variant_df.head(10))


