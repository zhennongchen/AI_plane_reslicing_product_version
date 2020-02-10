#!/usr/bin/env bash

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

# define the folder where you save the dcm2niix tool
dcm2niix_fld="/Users/zhennongchen/Documents/GitHub/AI_reslice_orthogonal_view/dcm2niix_11-Apr-2019/"

# define the patient list
readonly PATIENTS=(/Volumes/McVeighLab/wip/ucsd_lvad/to_be_reviewed/CVC1709271428/)

# convert dicom to nii
for p in ${PATIENTS[*]};
do

  #echo ${p}

  #rm -rf ${p}img-nii/
  mkdir -p ${p}/img-nii/

  IMGS=(${p}img-dcm/*/)

	echo ${IMGS}

	for i in $(seq 0 $(( ${#IMGS[*]} - 1 )));
  		do

  	${dcm2niix_fld}dcm2niix -i y -m y -b n -o "${p}img-nii/" -f "${i}" -9 -z y "${IMGS[${i}]}"
      echo ${i}
  done 



done
