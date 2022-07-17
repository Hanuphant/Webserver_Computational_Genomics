#!/usr/bin/env python3
# Genemark Automation code

import os
from os import listdir

command = "/home/groupa/gene_prediction/gms2/gms2.pl"
paths = "/home/groupa/final_assemblies/assemblies"
out_path = "/home/groupa/gene_prediction/gms2/output_gms2_gff/"
input_file = "contigs.fasta"
dirs = os.listdir(paths)
print(dirs)

for i in range(len(dirs)):
	os.system(f"perl {command} --seq {paths}/{dirs[i]}/{input_file} --genome-type auto --format gff --output {out_path}/{dirs[i]}_gms2.gff") 
