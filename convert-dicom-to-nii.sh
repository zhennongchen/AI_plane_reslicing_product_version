#!/usr/bin/env bash

# run in terminal of your own laptop

##############
## Settings ##
##############

set -o nounset
set -o errexit
set -o pipefail

#shopt -s globstar nullglob

###########
## Logic ##
###########

# define the folder where dcm2niix function is saved
dcm2niix_fld="/Users/zhennongchen/Documents/GitHub/AI_reslice_orthogonal_view/dcm2niix_11-Apr-2019/"

# define patient lists
readonly PATIENTS=(/Volumes/McVeighLab/wip/ucsd_lvad/to_be_reviewed/CVC1709271428/)

for p in ${PATIENTS[*]};
do

  #echo ${p}

  output="/Volumes/McVeighLab/projects/Zhennong/AI/Product_Test"
  mkdir -p ${output}/img-nii/

  IMGS=(${p}img-dcm-try/*/)

	echo ${IMGS}

	for i in $(seq 0 $(( ${#IMGS[*]} - 1 )));
  		do

  	  ${dcm2niix_fld}dcm2niix -i y -m y -b n -o "${output}/img-nii/" -f "${i}" -9 -z y "${IMGS[${i}]}"

  done 



done
