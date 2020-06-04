#!/bin/sh

# run locally
dcm2niix_fld="/Users/zhennongchen/Documents/GitHub/AI_reslice_orthogonal_view/dcm2niix_11-Apr-2019/"

PATIENTS=(/Volumes/McVeighLab/projects/Zhennong/AI/AI_datasets/ucsd_siemens/262829/ )

#PATIENTS[0]=/Volumes/McVeighLab/projects/Zhennong/AI/AI_datasets/ucsd_tavr_1/TAVR20170213090941/



# # slice list
SLICE[0]=2C
SLICE[1]=3C
SLICE[2]=4C
SLICE[3]=BASAL

dcm_folder="mpr_seth_dcm"
nii_folder="mpr_seth_nii"

for p in ${PATIENTS[*]};
do

    echo ${p}
    mkdir -p ${p}${nii_folder}/

    for s in ${SLICE[*]};
    do
        mkdir -p ${p}${nii_folder}/${s}
        IMGS=( ${p}${dcm_folder}/${s}/*)
        for i in $(seq 0 $(( ${#IMGS[*]} - 1 )));
        do
             
            echo ${IMGS[${i}]} # dcm2niix doesn't work (ignore image), remove -i y
            ${dcm2niix_fld}dcm2niix -i n -b n -m n -s y -o "${p}${nii_folder}/${s}/" -f "${i}" -9 -z y "${IMGS[${i}]}"
        done

    done

done

