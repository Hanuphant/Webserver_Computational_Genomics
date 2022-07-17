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
## TODO: Discuss and add output path ###

source ~/.bashrc
conda activate T1G1_final_assembly 
# python /home/paggarwal39/Team1-WebServer/scripts/assembly.py -i /home/groupa/webserver/Team1-WebServer/sample_input/ -o /home/groupa/webserver/Team1-WebServer/$job_id/assemblies/
### Path to be integrated ###
python /usr/src/app/webapp/pipeline/scripts/assembly.py -i /usr/src/app/media/uploaded_files/$job_id/ -o /usr/src/app/media/results/$job_id/assemblies/

cd /usr/src/app/media/results/$job_id
if [ $zip -eq 1 ]; then 
    zip assembly.zip -r assemblies/
    rm -r assemblies/
fi

conda deactivate
