# SALADS (*SAL*monella enteric*A* pre**D**iction and **S**ubtyping)

**Team Members:** Amartya Mandal, Mannan Bhola, Erin Connolly, Varsha Bhat, Zack Mudge, Shreyash Gupta, Palak Aggarwal  

We present **SALADS** (***SAL**monella enteric**A*** pre**D**iction and **S**ubtyping), a browser-based predictive webserver to identify and analyze Salmonella strain diversity for users with limited coding experience. **SALADS** aims to support bioinformaticians with a functional toolbox, allowing seamless integration of de novo assembly with SNP-based and phylogenomic analytic pipelines for unprecedented precision and detection of pathogenic Salmonella strains. **SALADS** can perform the following analyses given an input of raw sequence reads:
* De novo assembly
* Strain identification
* Average Nucleotide Identity
* Computational phenotyping
* Visualization of results

## Background & Motivation

Infections caused by pathogens commonly transmitted by food are common, potentially all preventable and therefore of major public health importance. The global burden of foodborne illnesses estimates that each year as many as 600 million, or almost 1 in 10 people in the world, fall ill after consuming contaminated food. Of these, 420,000 people die, including 125,000 children under the age of 5 years [1]. Therefore, our ability to rapidly detect, investigate, and stop foodborne outbreaks is vital to public health. 

## Webserver Walkthrough

**File Upload, Enter Email, Run Pipeline!**
1. Click on “Choose File" to select the first of the paired reads and then select "Choose File" below to complete the pair. 
2. Enter your email 
3. Select ‘Run Pipeline’ You will be notified by email when the analysis is complete.

<br></br>
<img src="imgs/homepage_screenshot.png" width="800">

Congratulations! You have just completed your analysis.

## Results
<br></br>
<img src="imgs/results-screenshot.png" width="800">
## About the Webserver

### Technical Stack:
The technical stack implemented comprises:

* Django: Python web framework
* Gunicorn: Python web server gateway interface (WSGI) HTTP server
* NGINX: Reverse proxy
* Postgres: Database

<br></br>
<img src="imgs/tech-stack.png" width="800">

### System architecture:
<br></br>
<img src="imgs/Sys-arch.png" width="800">

## About the Pipeline

**General workflow**:
<br></br>
<img src="imgs/Overview-pipeline.png" width="800">

**Pipeline workflow**:
<br></br>
<img src="imgs/Pipeline.png" width="800">


## Step 1: Genome Assembly
**Main Aim:** To stitch together the original bacterial genome from the fragmented reads of DNA

**How do we assemble the genome?**

* The assembly pipeline performs read trimming and de novo assembly given paired-end read files in FASTQ format. Initial read quality assessment and trimming are performed with **FastQC** and **BBDuk**, respectively. **MultiQC** is used to compile read quality metrics for all isolates into one quality assessment output. Assemblies are produced using **SPAdes**, and assembly quality reports are produced using **QUAST**.

## Step 2: Gene Prediction
**Main Aim:** To computationally infer the portions of DNA sequence that are biologically significant

**How do we predict genes?**
* The prediction pipeline predicts coding and noncoding (RNA) genes given the output from genome assembly. Glimmer, Genemark-S2 and Prodigal predict the coding regions, and Infernal is used to predict the noncoding genes. Bedtools is used to merge the results from the aforementioned tools. The output comprises the GFF, FNA and FAA files with the predicted coding and noncoding genes

## Step 3: Functional Annotation
**Main Aim: To attach biological information about what cellular processes a gene carries out.**

**How do we predict genes?**
* The functional annotation pipeline uses both homology and ab-initio tools. For homology based prediction, Eggnog mapper, CARD-RGI(antibiotic resistance) and VFDB(virulence factors) are used. The ab-initio tools used for signal & membrane proteins annotation are SignalP and TMHMM. For non-coding genes, the assembled contigs are used as input for Piler-CR. The final output is a merged GFF file.

## Step 4: Comparative Genomics
**Main Aim: To identify outbreak strains through the genetic relatedness between isolates.**

**How do we compare isolates?**
* The comparative genomics pipeline takes fasta files from the genome assembly output and identifies clusters and similarities using fastANI. fastANI provides a phylogenetic tree and heatmap as output.

## References
1. “Who's First Ever Global Estimates of Foodborne Diseases Find Children under 5 Account for Almost One Third of Deaths.” World Health Organization, World Health Organization, 3 Dec. 2015, www.who.int/news/item/03-12-2015-who-s-first-ever-global-estimates-of-foodborne-diseases-find-children-under-5-account-for-almost-one-third-of-deaths. 
2. Andrews, S. (2010). FastQC: a quality control tool for high throughput sequence data. Available online at: http://www.bioinformatics.babraham.ac.uk/projects/fastqc
3. Chen, L., Yang, J., Yu, J., Yao, Z., Sun, L., Shen, Y., Jin, Q. (2005). VFDB: a reference database for bacterial virulence factors .Nucleic Acids Res. 33:D325-8.
4. Goris J, Konstantinidis KT, Klappenbach JA, Coenye T, Vandamme P, et al. (2007). DNA-DNA hybridization values and their relationship to whole-genome sequence similarities. Int J Syst Evol Micr 57: 81-91. doi:10.1099/ijs.0.64483-0.
5. Lomsadze A, Gemayel K, Tang S, Borodovsky M. Modeling leaderless transcription and atypical genes results in more accurate gene prediction in prokaryotes. 
6. Arthur L. Delcher, Kirsten A. Bratke, Edwin C. Powers, Steven L. Salzberg, Identifying bacterial genes and endosymbiont DNA with Glimmer, Bioinformatics
7. Hyatt D, Chen GL, Locascio PF, Land ML, Larimer FW, Hauser LJ. Prodigal: prokaryotic gene recognition and translation initiation site identification. BMC Bioinformatics. 2010 Mar 8;11:119. doi: 10.1186/1471-2105-11-119.
8. Pertea G and Pertea M. GFF Utilities: GffRead and GffCompare [version 1; peer review: 3 approved]. F1000Research 2020, 9:304

