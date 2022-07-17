#!/usr/bin/env python3
import os
from os import listdir
from os.path import isfile,join

input_path = '/home/groupa/final_assemblies/assemblies/CGT1005.fasta'
out_path = '/home/groupa/gene_prediction/blast/'
refseq_path = '/home/groupa/gene_prediction/sequence.fasta'
database_path = '/home/groupa/gene_prediction/blast/reference_genome/database'


os.system(f"makeblastdb -in {refseq_path} -dbtype nucl -out {database_path}")

def blast(input_path, out_path, refseq_path, database_path):
	os.system(f" blastn -query {input_path} -db {database_path} -out {out_path}_blast.txt -max_target_seqs 1 -outfmt 6")
	return f"{out_path}_blast.txt"

blast('contigs.fasta', input_path, out_path, refseq_path, database_path)


