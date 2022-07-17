#!/usr/bin/env Rscript

library(tidyr)
library(ape)
library(phangorn)

args = commandArgs(trailingOnly=TRUE)

# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "out.txt"
}


table <- read.table(args[1], sep = '\t', header = F)

table<-table[!(table$V1==table$V2),]
table$V3 <- 1 - (table$V3/100)
table$V4 <- NULL
table$V5 <- NULL

matrix <- spread(data = table, key = V1, value = V3 )

row.names(matrix) <- matrix$V2

UPGMA <- upgma(dist(matrix))

my_tree <- as.phylo(UPGMA)
write.tree(phy=my_tree, file=args[2])
