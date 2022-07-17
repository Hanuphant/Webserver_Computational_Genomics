#!/usr/bin/env python3

# script to perform comparative genomics at whole genome, gene, and SNP level

import subprocess
import sys
import re
import argparse
import os
from multiprocessing import Pool
import toytree
import toyplot
import toyplot.pdf

parser = argparse.ArgumentParser(description="Comparative Genomics Analysis. Type comparative.py -help for options")
parser.add_argument("-i", help="path to the directory that has all the assembled genomes as sub-directories", required=True)
parser.add_argument("-o", type = str, help = "to specify output file")
parser.add_argument("-t", help="number of cores; by default = 1", type=str, default="1")
# parser.add_argument("-j", help="Job ID", type=str, required=True)


args = parser.parse_args()


# Function for fastANI
def run_fastani(inputpath_file, job_output):
	# Enter the paths of all the isolates you want to run with the fastANI tool
	os.system(f"fastANI -q {inputpath_file} --rl /projects/groupa/inputpath_file.txt -o {job_output}fastani.out")

	os.system(f"Rscript /projects/groupa/Team1-WebServer/backend/scripts/fastANI2tree.R {job_output}fastani.out {job_output}fastani.nwk")
	# ### Visualisation ###
	with open(f"{job_output}fastani.nwk", 'r') as f:
		newick = f.read()
	tre = toytree.tree(newick)
	canvas, axes, mark = tre.draw(height = 450, node_labels = None, node_sizes = 5, node_colors = "red", layout = 'd', scalebar = True)

	os.system(f"Rscript /projects/groupa/Team1-WebServer/backend/scripts/fastANI_heatmap.R {job_output}")
	return canvas


if __name__ == "__main__":
	print("Running fastANI")
	
	job_output=args.o
	if not os.path.exists(job_output):
		os.makedirs(job_output)
	
	for files in os.listdir(args.i):
		input_file_txt = os.path.join(args.i, files, 'contigs.fasta')
	
	c = run_fastani(input_file_txt, job_output)

	toyplot.pdf.render(c, os.path.join(job_output, "phylogeny_tree.pdf"))
	
	print("Done! Exiting Now")
