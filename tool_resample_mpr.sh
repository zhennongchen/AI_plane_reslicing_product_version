#!/usr/bin/env bash
########################################
# run at mcveighlab-octomore, save locally at octomore, need to transfer back to NAS
# Currently can only run in octomore terminal, cd Developer, . .py35/bin/activate to activate the Virtual environment
# screen to have a new screen, screen -r to retrieve the previous
# ctrl +A +D to quit 
#######################################

. ./main_step1_defaults.sh

set -o nounset
set -o errexit
set -o pipefail

out_size=160;
out_spac=1.5;
out_value=-2047;

dv_utils_fld="/home/cnn/Documents/Repos/dv-commandline-utils/bin/"


# patient list
DATA_DIR="/media/McVeighLabSuper/projects/Zhennong/AI/Zhennong_WMA_Movie_dataset/"
SAVE_DIR="/home/cnn/Documents/Resample_mpr/"
readonly PATIENT=( ${DATA_DIR}*/)

SLICE[0]=2C
SLICE[1]=3C
SLICE[2]=4C
SLICE[3]=BASAL


# Folder where you want to put the reslice
fld_prefix=mpr-nii-zc-sm

# Folder where the volumes to be resliced reside
input_fld=img-nii

# Folder where the mpr nii sits with direction info
mpr_fld=mpr-nii-zc

for p in ${PATIENT[*]};
do
    echo ${p}${mpr_fld}
    if  [ ! -d ${p}${mpr_fld} ];then
        echo "no mpr image"
        continue
    fi
    echo ${p}
    save=${SAVE_DIR}$(basename $(dirname ${p}))/$(basename ${p})/
    echo ${save}
    mkdir -p ${SAVE_DIR}$(basename $(dirname ${p}))/
    mkdir -p ${SAVE_DIR}$(basename $(dirname ${p}))/$(basename ${p})/
    

    IMGS=(${p}${input_fld}/*.nii.gz) ###CHANGE IF MPR HAS A SERIES
     

    fld_name=${save}${fld_prefix}-${out_spac}/
    mkdir -p ${fld_name}

    for i in $(seq 0 $(( ${#IMGS[*]} - 1 )));
    do

        # For each volume, lets look at each MPR slice

        for s in ${SLICE[*]};
        do

            slc_name=${save}${fld_prefix}-${out_spac}/${s}/
            mkdir -p ${slc_name}

            REF=( ${p}${mpr_fld}/*${s}*/* )

            img_name=$(basename ${IMGS[${i}]}  .nii.gz);
            output_name=${slc_name}${img_name}.nii.gz
        
            echo ${IMGS[${i}]}
            echo ${REF[0]}
            echo $output_name

            ${dv_utils_fld}dv-resample-from-reference --input-image ${IMGS[${i}]} --reference-image ${REF[0]} --output-image $output_name --output-size $out_size --output-spacing $out_spac --outside-value $out_value
            
        done
    done
done