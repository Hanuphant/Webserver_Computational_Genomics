#!/usr/bin/env Rscript
library("reshape2")
library("gplots")
# setwd("~/R/")
### get data, convert to matrix

args = commandArgs(trailingOnly=TRUE)


# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  print(args[1])
  args[2] = "out.txt"
}

fastani_out = file.path(args[1],'fastani.out')
x <- read.table(fastani_out)
matrix <- acast(x, V1~V2, value.var="V3")
matrix[is.na(matrix)] <- 70
matrix<-rbind(matrix, matrix[1, ])
### define the colors within 2 zones
breaks = seq(min(matrix), max(100), length.out=100)
gradient1 = colorpanel( sum( breaks[-1]<=98.8 ), "red", "white" )
gradient2 = colorpanel( sum( breaks[-1]>98.8 & breaks[-1]<=100), "white", "blue" )

hm.colors = c(gradient1, gradient2)
# out_path <- paste0(args[1]+"/fastaniheatmap.pdf")
pdf(file.path(args[1],'heatmap.pdf'))
heatmap.2(matrix, scale = "none", trace = "none", col = hm.colors, cexRow=0.50, cexCol=0.50, margins = c(18,12))
dev.off()
