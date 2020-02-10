#!/bin/sh


set -o nounset
set -o errexit
set -o pipefail

# run locally
dcm2niix_fld="/Users/zhennongchen/Documents/GitHub/AI_reslice_orthogonal_view/dcm2niix_11-Apr-2019/"

PATIENTS=(/Volumes/McVeighLab/projects/Zhennong/AI/AI_datasets/ucsd_lvad/*/)

#PATIENTS[0]=/Volumes/McVeighLab/projects/Zhennong/AI/AI_datasets/ucsd_tavr_1/TAVR20170213090941/


for p in ${PATIENTS[*]};
do

    echo ${p}

    mkdir -p ${p}img-try-nii
    
    TIME_FRAMES=( ${p}img-try-dcm/*/)
    for t in ${TIME_FRAMES[*]};
    do
        echo ${t}
        IMGS=( ${t}*)
        #for i in $(seq 0 $(( ${#IMGS[*]} - 1 )));
        #do 
        ${dcm2niix_fld}dcm2niix -i n -b n -m y -s y -o "${p}img-try-nii/" -f "${i}" -9 -z y "${IMGS}"
        #done
        
    done
    

    # for s in ${SLICE[*]};
    # do
    #     mkdir -p ${p}mpr_new_nii/${s}
    #     IMGS=( ${p}mpr_new_dcm/${s}/*)
    #     for i in $(seq 0 $(( ${#IMGS[*]} - 1 )));
    #     do
    #         echo ${i}
    #         #echo ${IMGS[${i}]}
    #         ${dcm2niix_fld}dcm2niix -i n -b n -m n -s y -o "${p}mpr_new_nii/${s}/" -f "${i}" -9 -z y "${IMGS[${i}]}"
    #     done

    # done

done

