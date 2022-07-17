#!/usr/bin/env python3
import os
from os import listdir
from os.path import isfile,join

input_path = '/home/groupa/final_assemblies/assemblies/CGT1005'
out_path = '/home/groupa/gene_prediction/gms2/final/'

def gms2(file, input_path, out_path):
	command = '/home/groupa/gene_prediction/gms2/gms2.pl'
	os.system(f"perl {command} --seq {input_path}/{file} --genome-type auto --format gff --output {out_path}/{file}_gms2.gff")
	return f"{out_path}/{file}_gms2.gff"

gms2('contigs.fasta', input_path, out_path)
					
