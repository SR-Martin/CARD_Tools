# CARD_Tools

Repository for tools used in analysis of entries in the CARD database. Below is a brief description of each file in the repository.

#### AMR_gene_grouper.py
* Takes a TSV BLAST output file (e.g. Resources/CARD_VS_CARD.out) in the format

query name \t ref name \t identity \t ...

and partitions the set of all sequences in the file into groups, based on similarity. In each group, each sequence has identity of at least some value (set by the user) to all other sequences in the group. Note that this grouping is non-unique, and that the similarity relationship is not transitive. 
* The output file is in the format 

group name \t number of genes in group \t gene1 \t gene2 \t ...

* Can also write a TSV file of pairwise identites i.e. a matrix where the ij entry is the identity between gene i and gene j.
* The user may supply a list of gene names or a list of ARO numbers. In either of these cases, only the sequences found in the list are compared, and all others are ignored.

#### AMRReporter.py
* Takes a TSV BLAST output file (e.g. Resources/CARD_VS_CARD.out) in the format 

query name \t ref name \t identity \t alignment length \t query length \t ref length

and writes (to standard output), for each sequence a list of all other sequences that contain an alignment of a minimum length and identity (these values are set by the user).

#### all_genes_grouping_70pc.txt
* The result of AMR_gene_grouper.py on all genes from the CARD database (version 1.1.1), with minimum identity set to 70%. 

#### Resources/CARD_VS_CARD.out
* BLAST output in the format qname \t rname \t identity \t alignment length \t query length \t ref length of a BLAST search of CARD 1.1.1  against itself. 