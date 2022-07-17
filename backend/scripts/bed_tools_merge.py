#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from glob import glob


parser=argparse.ArgumentParser(description="GenePrediction helper functions which runs individual tools")
parser.add_argument("-i", required=True, help="Path to input folder containing fasta files")
parser.add_argument("-o", required=True, help="Path to output folder")
args=parser.parse_args()

input_files = glob(args.i+"/**/*.fasta", recursive=True)

for input_file in input_files:
    output_folder = os.path.join(args.o, input_file.rsplit("/",2)[-2])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    gff_directory = os.path.join(output_folder, "gff_files/")
    if not os.path.exists(gff_directory):
        os.makedirs(gff_directory)
    
    sorted_directory = os.path.join(output_folder, "sorted_gff_files/")
    if not os.path.exists(sorted_directory):
        os.makedirs(sorted_directory)
    
    consensus_directory = os.path.join(output_folder, "consensus_and_fasta/")
    if not os.path.exists(consensus_directory):
        os.makedirs(consensus_directory)
    
    isolates = []
    gff_filelist = os.listdir(gff_directory)
    try:
        for file in gff_filelist:
            unsorted_gff = gff_directory + file #CGT1005_prodigal.gff
            toolext = (os.path.basename(unsorted_gff)).split(".")[0] #CGT1005_prodigal
            isolatename = toolext.split("_")[0] #CGT1005
            if isolatename not in isolates:
                isolates.append(isolatename)
            outputsorted = sorted_directory + toolext + "_sorted.gff"
            #gets tge sorted files
            os.system(f"bedtools sort -i {unsorted_gff} > {outputsorted}")
        
        for sample in isolates:
            gms2gff = sorted_directory +  sample + "_gms2_sorted.gff"
            prodigalgff = sorted_directory +  sample + "_prodigal_sorted.gff"
            glimmergff = sorted_directory +  sample + "_glimmer_sorted.gff"
            consensusfilepath = consensus_directory + sample + "_consensus.gff"
            uniq_consensusfilepath = consensus_directory + sample + "_uniq_consensus.gff"
            os.system(f"bedtools intersect -f 1.0 -r -a {gms2gff} -b {prodigalgff} {glimmergff} > {consensusfilepath}")
            os.system(f"uniq {consensusfilepath} > {uniq_consensusfilepath}")
            gff2fasta = consensus_directory + sample + "_uniq_consensus.fna"
            os.system(f"bedtools getfasta -fi {input_file} -bed {uniq_consensusfilepath} > {gff2fasta}")
            fnatofaa = consensus_directory + sample + "_uniq_consensus.faa"
            os.system(f"transeq -sequence {gff2fasta} -outseq {fnatofaa}")
    except Exception as e:
        print(e)
