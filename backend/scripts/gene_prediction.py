#!/usr/bin/env python3

import os
import shutil
import argparse
import subprocess
# from multiprocessing import Pool 
from glob import glob

parser=argparse.ArgumentParser(description="GenePrediction helper functions which runs individual tools")
parser.add_argument("-i", required=True, help="Path to the directory containing the assembled genomes. Please look into the directory structure")
parser.add_argument("-o", required=True, help="Path to the results folder which will get created")
#parser.add_argument("-refseq","--reference_sequence", required=True, help="Reference Sequence path of the organism")
#parser.add_argument("-db", required=True, help="Path to Rfam database input for infernal tool")
#parser.add_argument("-db_blast", required=True, help="Path to store database for blast")
parser.add_argument("-gl", action="store_true", help="Runs glimmer")
parser.add_argument("-gm", action="store_true", help="Runs genemarkS2")
# parser.add_argument("-fg", action="store_true", help="Runs fraggenescan")
parser.add_argument("-pg", action="store_true", help="Runs prodigal")
parser.add_argument("-inf", action="store_true", help="Runs infernal")
parser.add_argument("-blast", action="store_true", help="Runs blast")
# parser.add_argument("-j", help="Job ID", type=str, required=True)
# parser.add_argument("-t", default=1, help="Number of threads") # Calm!!!! Multithreading not working for fgs, gms2 and infernal! 

args=parser.parse_args()
print(args.i)
#database_path = args.db_blast
# database_path = '/home/groupa/gene_prediction/blast/reference_genome/database'
#infernal_rfam_db = args.db
#refseq_path = args.refseq

def glimmer(fasta_file, gff_directory):
    filename = (os.path.basename(fasta_file)).split(".")[0]
    print(filename)
    output_name = temp_directory + filename
    print(output_name)
    subprocess.call(["/projects/groupa/Team1-WebServer/backend/res/g3-from-scratch.csh", fasta_file, output_name])
    predict_file = output_name + ".predict"
    glimmer_gff_file = open(gff_directory + filename + "_glimmer.gff", "w")
    #subprocess.call(["/projects/groupa/Team1-WebServer/backend/res/Glimmer_GFF_conversion.py", predict_file], stdout=glimmer_gff_file)
    # subprocess.call(["perl GlimmerPredict2Gff3.pl", predict_file], stdout=glimmer_gff_file)
    
def gms2(fasta_file, gff_directory):
    command = '/projects/groupa/Team1-WebServer/backend/res/gms2/gms2.pl'
    filename = (os.path.basename(fasta_file)).split(".")[0]
    os.system(f"perl {command} --seq {fasta_file} --genome-type auto --format gff --output {gff_directory}/{filename}_gms2.gff")
#     return f"{gff_directory}/{fasta_file}_gms2.gff"

def FragGeneScan(fasta_file):
    filename = (os.path.basename(fasta_file)).split(".")[0]
    print("\nRunning FragGeneScan for: "+filename)
    frag_gene_scan_gff_file = open(gff_directory + filename + "_fraggenescan.gff", "a")
    subprocess.run("/projects/groupa/Team1-WebServer/backend/res/run_FragGeneScan.pl -genome"+str(fasta_file)+"-out="+str(frag_gene_scan_gff_file) +"-complete=1" + "-train=complete")

def prodigal(fasta_file, gff_directory):
    filename = (os.path.basename(fasta_file)).split(".")[0]
    output_name = gff_directory + filename + "_prodigal.gff"
    subprocess.call(["/projects/groupa/Team1-WebServer/backend/res/prodigal.linux", "-i", fasta_file, "-f", "gff", "-o", output_name])
    
# def infernal(fasta_file,infernal_rfam_db):
#     print("Indexing Rfam db to run infernal")
#     subprocess.check_output(["cmpress", infernal_rfam_db]) 
#     print("Infernal running the cmscan program to annotate RNAs represented in Rfam")
#     subprocess.check_output(["cmscan", "--rfam", "--noali", "--tblout", "res/infernal.tblout", "--fmt", "2", "--clanin", "res/infernal_db/Rfam.clanin", "res/infernal_db/Rfam.cm", fasta_file])
#     print("Converting infernal tabular output to gff")
#     filename = (os.path.basename(fasta_file)).split(".")[0]
#     output_name = gff_directory + filename + "_infernal.gff"
#     gff = "perl ./res/infernal-tblout2gff.pl --cmscan --fmt2 res/infernal.tblout > {inf}".format(inf = output_name)
#     os.popen(gff)
#     #subprocess.check_output(["perl","infernal-tblout2gff.pl", "--cmscan", "--fmt2", "infernal.tblout", ">", infernal_output])

#     return True
    
#def blast(input_fasta, database_path, output_folder):
#    filename = (os.path.basename(input_fasta)).split(".")[0]
#    output_name = output_folder + "/"+filename + "_blast.txt"
#    os.system(f" blastn -query {input_fasta} -db {database_path} -out {output_name} -max_target_seqs 1 -outfmt 6 -num_threads {int(args.t)}")
#    return f"{output_name}"


if __name__ == "__main__":
    
    print("Running blast database")

    input_files = glob(args.i+"/**/*.fasta", recursive=True)

#    os.system(f"makeblastdb -in {refseq_path} -dbtype nucl -out {database_path}")
    # iso_file = os.listdir(args.i)[0]
    # total_path = os.path.join(args.i,iso_file)
    # input_files = ''
    # for root, dirs, files in os.walk(os.path.join(args.i,iso_file)):
    #    for file in files:
    #       if file.endswith('.fasta'):
    #input_files = glob(args.i+"/**/*.fasta",recursive=True) #calm down! Emergency measures being taken!
    #input_files = os.listdir(args.i)
            #  input_files = [os.path.join(total_path,str(file))]
#Have to look at job ids here~~~~~s
    
    for input_file in input_files:
        output_folder = os.path.join(args.o, input_file.rsplit("/",2)[-2])
        # output_folder = args.o
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        temp_directory = os.path.join(output_folder, "tmp/")
        if not os.path.exists(temp_directory):
            os.makedirs(temp_directory)
        gff_directory = os.path.join(output_folder, "gff_files/")
        if not os.path.exists(gff_directory):
            os.makedirs(gff_directory)
        #Running the individual tools
        if args.gl:
            print("Running GLIMMER")
            glimmer(input_file, gff_directory)
            #print(input_file)
        if args.pg:
            print("Running Prodigal")
            prodigal(input_file, gff_directory)
    #    if args.inf:
    #        infernal(input_file, infernal_rfam_db)
        if args.gm: 
            print("Running Gene Mark S2")
            gms2(input_file, gff_directory)
            os.system('rm *.lst *.mod log')

#        if args.blast:
#            blast(input_file, str(database_path), output_folder)

        shutil.rmtree(temp_directory)
