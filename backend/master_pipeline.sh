#!/bin/bash

zip=0

while getopts j:z OPTION
do
    case "$OPTION" in
        j) job_id=${OPTARG};;
        z) zip=1;;
    esac
done


### Genome Assembly ###

source /projects/groupa/miniconda3/etc/profile.d/conda.sh
conda activate T1G1_final_assembly 
python /projects/groupa/Team1-WebServer/backend/scripts/assembly.py -i /projects/groupa/Team1-WebServer/app/media/uploaded_files/$job_id/ -o /projects/groupa/Team1-WebServer/app/media/$job_id/assemblies
conda deactivate


### Gene Prediction ###

source /projects/groupa/miniconda3/etc/profile.d/conda.sh
conda activate T1G2
python /projects/groupa/Team1-WebServer/backend/scripts/gene_prediction.py -i /projects/groupa/Team1-WebServer/app/media/$job_id/assemblies -o /projects/groupa/Team1-WebServer/app/media/$job_id/predictions -gl -gm -pg
python /projects/groupa/Team1-WebServer/backend/scripts/bed_tools_merge.py -i /projects/groupa/Team1-WebServer/app/media/$job_id/assemblies -o /projects/groupa/Team1-WebServer/app/media/$job_id/predictions
conda deactivate


### Functional Annotation ###

source /projects/groupa/miniconda3/etc/profile.d/conda.sh
conda activate T1G3
export PATH="$PATH:/projects/groupa/bin/usearch/"
export PATH="$PATH:/projects/groupa/bin/ncbi-blast-2.13.0+/bin/"
export PATH="$PATH:/projects/groupa/bin/lipop/LipoP1.0a/"
export PATH="$PATH:/projects/groupa/bin/signalp-5.0b/bin/"
export PATH="$PATH:/projects/groupa/bin/tmhmm-2.0c/bin/"
export PATH="$PATH:/projects/groupa/bin/kSNP3/"
python /projects/groupa/Team1-WebServer/backend/scripts/FunctionalAnnotationPipeline.py -i /projects/groupa/Team1-WebServer/app/media/$job_id/predictions/ -o /projects/groupa/Team1-WebServer/app/media/$job_id/annotation/ -a /projects/groupa/Team1-WebServer/app/media/$job_id/assemblies/ -c scripts/FAmodule/CRISPRFileToGFF_1.pl
conda deactivate

### Comparative Genomics ###
source /projects/groupa/miniconda3/etc/profile.d/conda.sh
conda activate T1G4
python /projects/groupa/Team1-WebServer/backend/scripts/comparative_pipeline.py -i /projects/groupa/Team1-WebServer/app/media/$job_id/assemblies -o /projects/groupa/Team1-WebServer/app/media/$job_id/comp_genomics/
conda deactivate 

rm -rf spades_outputs trimmed multiqc_data fastqc multiqc_report* group* log *.html itr* tmp* GMS2.mod 

conda activate base

cd /projects/groupa/Team1-WebServer/app/media/$job_id
zip comp_genomics.zip -r comp_genomics/
if [ $zip -eq 1 ]; then 
    zip assembly.zip -r assemblies/
    zip gene_predictions.zip -r predictions/
    zip functional_output.zip -r annotation/
fi

conda deactivate

cp /projects/groupa/Team1-WebServer/app/media/$job_id/comp_genomics/heatmap.pdf /projects/groupa/Team1-WebServer/app/media/$job_id/
cp /projects/groupa/Team1-WebServer/app/media/$job_id/comp_genomics/phylogeny_tree.pdf /projects/groupa/Team1-WebServer/app/media/$job_id/
mv /projects/groupa/Team1-WebServer/app/media/$job_id /projects/groupa/Team1-WebServer/app/media/results/
