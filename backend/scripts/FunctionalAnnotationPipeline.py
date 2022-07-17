#!/usr/bin/python
# -*- coding: utf-8 -*-

## General Command
    #  outdir = "/home/sgupta755/gitfolder/Debugging/output"
    # indir = "/home/sgupta755/gitfolder/Debugging/predictions"
    # assembly_dir = "/home/sgupta755/gitfolder/Debugging/assemblies"
    # piler_cr_converter = "/home/sgupta755/gitfolder/Team1-FunctionalAnnotation/CRISPRFileToGFF_1.pl"
# python FunctionalAnnotationPipeline.py -i /home/sgupta755/gitfolder/Team1-FunctionalAnnotation/sample_output -o /home/sgupta755/gitfolder/Team1-FunctionalAnnotation/functional_output -a /home/sgupta755/gitfolder/Team1-FunctionalAnnotation/assemblies -c FAmodule/CRISPRFileToGFF_1.pl

# Each tool will have their own functions

import argparse
import os
import re
import subprocess
import time
from FAmodule.signalp_script_func import signalP
from FAmodule.eggScript import getFile
from FAmodule.tmhmm import tmhmm, converttogff
from FAmodule.pilercr_module import piler_cr_module
from FAmodule.vfdb_module import vfdb_module
from FAmodule.GFF_merger import GFF_Merge
import multiprocessing as mp
import time
from tqdm import tqdm

# USearch Clustering



def usearch_command(sample, path, outputpath = ".", pid = 0.97):
    # Running usearch command
    try:
        os.mkdir(os.path.join(outputpath, sample))
    except:
        print("Folder already made")
    cmd = "cat "+ path + "> " + "ClusterFaa"
    # cmd = cmd.split()
    os.system(cmd)
    command = "usearch -cluster_fast " + "ClusterFaa" + " -id "+str(pid)+" -centroids " + os.path.join(outputpath) + "/Centroids.fasta -uc " + os.path.join(outputpath, sample) + "/Clusters.uc"
    command = command.split()
    subprocess.check_output(command)
    os.system("rm CLusterFaa")


def usearch_multi_runner(dirpath=".", output2 = ".", pid=0.97):
    # Running usearch on multiple
    faainputs = []
    for root, dirs, files in os.walk(dirpath, topdown=False):
        for name in files:
            if re.search(pattern=".faa", string=root + name) and re.search(pattern="uniq", string=root + name):
                faainputs.append(os.path.join(root, name))
    faainputs = list(zip(faainputs, dirs))
    # print(dirs)
    # for dir in dirs:
    #     print(dir)
    patho = ""
    for fi, isolate in faainputs:
        patho += fi + " "
    usearch_command("", patho, output2, pid)
    print("USearch clustering done")

def rgi_2_gff(temp_file):
    with open(temp_file, encoding='latin-1') as f:
        lines = f.readlines()
        del lines[0]
    out_content = '##gff-version  3\n'
    for line in lines:
        items = [l for l in line.replace(' ', '\t').split('\t') if l]
        out_content += items[0] + '\t'
        out_content += 'RGI-CARD\tAntibiotic resistant genes\t'
        start, end = items[2],items[4]
        out_content += '{}\t{}\t'.format(start, end)
        out_content += '.\t.\t.\t'
        out_content += ';'.join(items[8:-2])
        out_content += '\n'
    out_content = out_content[:-1]
    with open("%s.gff"%(temp_file), 'w') as f:
        f.write(out_content)

def card_rgi_runner(indir, outdir):
    """

    :param indir: Input directory
    :param outdir: Output directory
    :return: None. Just runs the command.
    """
    print(outdir)
    try:
        os.mkdir(os.path.join(outdir, "database"))
        print(f"{os.path.join(outdir, 'database')} created")
    except:
        print("Folder already exists")
    # try:
    #     os.chdir(os.path.join(outdir, "database"))
    # except:
        print("Already there")
    if not os.path.exists(os.path.join(outdir, "database", 'card.json')):
        print(f"wget -P {os.path.join(outdir, 'database')} https://card.mcmaster.ca/latest/data")
        subprocess.check_output(["wget", "-P",os.path.join(outdir, "database"),"https://card.mcmaster.ca/latest/data"])
        print(f"tar -xvf {os.path.join(outdir, 'database', 'data')} -C {os.path.join(outdir, 'database')}")
        subprocess.check_output(["tar", "-xvf", os.path.join(outdir,"database","data"), "-C",os.path.join(outdir, "database")])
        subprocess.call(["rgi", "load", "--card_json", os.path.join(outdir, "database", "card.json")])
    try:
        os.mkdir(os.path.join(outdir))
    except:
        print("Already made")

    inputsfile = []
    for root, dirs, files in os.walk(indir, topdown=False):
        for name in files:
            if re.search(pattern=".fasta", string=root + name) and not re.search(pattern=".fai", string=root + name):
                inputsfile.append(os.path.join(root, name))
    isolates = [f for f in os.listdir(os.path.join(indir))]
    inputs = list(zip(inputsfile, isolates))

    for ins, isos in inputs:
        print(f"Running card-rgi main for {isos} where assembly file is in {ins}")
        start = time.time()
        try:
            os.mkdir(os.path.join(outdir, "CardOutput", isos))
        except:
            print("Folder already exists")
        command = "rgi main -i "+os.path.join(ins)+" -o "+os.path.join(outdir,"CARD"+isos)+" -n 6"
        command = command.split()
        subprocess.check_output(command)
        stop = time.time()
        rgi_2_gff(os.path.join(outdir,"CARD"+isos+".txt"))
        print(f"Time taken for {isos} is {stop-start}s")
    # os.chdir(os.path.join(outdir))
    # subprocess.check_output(["rm", "-r", "contigs*"])
    # subprocess.check_output(["rm", "-r", "*json"])
    return None


def tmhmm_runner(indir, outdir):
    tmhmm(indir, outdir)
    converttogff(outdir)
    return None
    
# TODO: merge command function

def main():
    # warnings.filterwarnings("ignore")
    # Calling argparse and creating the parser class object

    parser = argparse.ArgumentParser(description="Parser for functional annotation")
    parser.add_argument("-i", metavar="Absolute path of the directory containing the isolates", type=str, required=True)
    parser.add_argument("-o", metavar="Relative output directory path",
                        help="Path for output directory. If it does not exist it "
                             "will be created.", type=str, required=True)
    parser.add_argument("-a", metavar="Absolute path of assembly fastq files", type=str, required=True) # Required for pilerCR and CARD-RGI
    parser.add_argument("-c", metavar="Perl GFF Converter for CRISPR", type=str, required=True)
    parser.add_argument("-p", metavar="Percentage of identity", type=float, default=0.97)
    
    args = parser.parse_args()
    
    currentdirectory = os.getcwd()
    #
    try:
        os.mkdir(os.path.join(currentdirectory, args.o))
    except:
        print("Folder already exists")
    
    

    # Input directory and output directory
    indir = args.i
    outdir = args.o
    assembly_dir = args.a
    piler_cr_converter = args.c

    # outdir = "/home/sgupta755/gitfolder/Debugging/output"
    # indir = "/home/sgupta755/gitfolder/Debugging/predictions"
    # assembly_dir = "/home/sgupta755/gitfolder/Debugging/assemblies"
    # piler_cr_converter = "/home/sgupta755/gitfolder/Team1-FunctionalAnnotation/CRISPRFileToGFF_1.pl"
    
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    t1 = time.time()
    
    if not os.path.exists(os.path.join(outdir, "CardRGI")):
        os.mkdir(os.path.join(outdir, "CardRGI"))
    if not os.path.exists(os.path.join(outdir, "VFDB")):
        os.mkdir(os.path.join(outdir, "VFDB"))
    if not os.path.exists(os.path.join(outdir, "pilerCR")):
        os.mkdir(os.path.join(outdir, "pilerCR"))
    if not os.path.exists(os.path.join(outdir, "signalP")):
        os.mkdir(os.path.join(outdir, "signalP"))
    if not os.path.exists(os.path.join(outdir, "eggNOG-mapper")):
        os.mkdir(os.path.join(outdir, "eggNOG-mapper"))
    if not os.path.exists(os.path.join(outdir, "tmhmm")):
        os.mkdir(os.path.join(outdir, "tmhmm"))

    vfdb_module(input_dir=indir, output_dir=os.path.join(outdir, "VFDB"))
    piler_cr_module(assembly_dir, os.path.join(outdir, "pilerCR"), piler_cr_converter)
    t3 = time.time()
    signalP(mypath = indir, path = os.path.join(outdir, "signalP"))
    print(f"Time taken for signalP is {time.time()-t3}s")

    # card_rgi_runnerp = mp.Process(target=card_rgi_runner, args=(assembly_dir, os.path.join(outdir, "CardRGI")))
    getfilep = mp.Process(target=getFile, args=(indir, os.path.join(outdir, "eggNOG-mapper")))
    tmhmm_runnerp = mp.Process(target=tmhmm_runner, args=(indir, os.path.join(outdir, "tmhmm")))
    processes = [tmhmm_runnerp, getfilep]
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
    try:
        os.mkdir(os.path.join(outdir, "FinalResults"))
    except:
        print("File already made")
    GFF_Merge(outdir, os.path.join(outdir, "FinalResults"), indir)
    t2 = time.time()
    print(f"Total time taken is {t2-t1}s")

    # Clean up
    os.system("rm -r " + os.path.join(outdir, "CardRGI"))
    os.system("rm -r " + os.path.join(outdir, "VFDB"))
    os.system("rm -r " + os.path.join(outdir, "pilerCR"))
    os.system("rm -r " + os.path.join(outdir, "signalP"))
    os.system("rm -r " + os.path.join(outdir, "eggNOG-mapper"))
    os.system("rm -r " + os.path.join(outdir, "tmhmm"))
    os.system("rm -r TMH*")
    os.system("rm -r *.gff")
    os.system("rm -r " + "TMHMM*")
    
if __name__ == "__main__":
    main()
