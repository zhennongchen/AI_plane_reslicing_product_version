#!/usr/bin/env bash

# run in terminal of your own laptop (this script is written specifically for Jura)

##############
## Settings ##
##############

set -o nounset
set -o errexit
set -o pipefail

# define the folder where dcm2niix function is saved
dcm2niix_fld="/Users/bowmore1/Documents/Zhennong/sort_AUH_code/dcm2niix_11-Apr-2019/"


# define patient lists
readonly PATIENTS=(/Volumes/mcveighlab_01/Zhennong_AI_dataset/patients_for_movie/*/ )

# slice list
SLICE[0]=2C
SLICE[1]=3C
SLICE[2]=4C
SLICE[3]=BASAL

# define image folder
img_fld="mpr-dcm-zc"

for p in ${PATIENTS[*]};
do
    if  [ ! -d ${p}${img_fld} ];then
       continue
    fi

    echo ${p}
    output=${p}mp-nii-zc
    mkdir -p ${output}

    if [ -d ${output} ] && [ "$(ls -A  ${output})" ];then
        echo "already done"
        continue
    fi

    for s in ${SLICE[*]};
    do
        slice_folder=${p}${img_fld}/${s}
        slice_output=${output}/${s}
        mkdir -p ${slice_output}
        
        if [ "$(ls -A ${slice_folder})" ]; then
            IMGS=( ${p}${img_fld}/${s}/*)
            for i in $(seq 0 $(( ${#IMGS[*]} - 1 )));
            do
            
                echo ${IMGS[${i}]}
                ${dcm2niix_fld}dcm2niix -i n -b n -m n -s y -o "${slice_output}/" -f "${i}" -9 -z y "${IMGS[${i}]}"
        done
	fi
    done

done
