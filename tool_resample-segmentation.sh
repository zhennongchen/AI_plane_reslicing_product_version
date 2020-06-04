#!/usr/bin/env bash

################ Lastest version of resampling

: '
The CCT volumes are too large to be trained on the network at their current resolution;
moreover, the input resolution is anisotropic, which is not ideal for training.
This script resamples all images and segmentations to a uniform, isotropic spacing,
dictated by the spacing defined in the experiment.

NOTES:

- Inputs come from {img,seg}-nii; outputs go in {img,seg}-nii-sm.

- The script takes quite a long time to run for all images; therefore, by default
it only runs on inputs which are newer than their corresponding resampled outputs.
To override this behavior, set `RUNALL` to `true`.
'

######### Run in Docker: Docker_Resample_Laura, start the docker by start_docker_resample.sh

# Include settings and ${CG_*} variables.
#. defaults.sh
. safe-bash.sh

# Get a list of patients.
readonly INPUT_DIRS=(${CG_RAW_DIR}*/ ) 

# This is the main function, which performs the resampling of either the images or
# segmentations for a single patient.  The input directory name, output directory name,
# interpolation order (0 = nearest neighbot, 1 = linear, 2 = quadratic, 3 = cubic, etc.),
# and whether to run all.

function RESAMPLE() {

  I_DIR=${1}
  O_DIR=${2}
  INTERPOLATION=${3}
  SPACING=${4}

  # Get a list of inputs.
  IMGS=( ${I_DIR}*.nii.gz )

  if [ "${#IMGS[*]}" -le 1 ];
  then
    return
  fi

  # Loop over the images.
  for i in ${IMGS[*]};
  do

    # Ensure that the output directory exists.
    mkdir -p ${O_DIR}

    # Create the name of the output.
    o=${O_DIR}$(basename ${i})

    # Resample if:
    # - The output doesn't exist.
    # - The input is newer than the output.
    #if [ "${i}" -nt "${o}" ]; then
    echo "resampling..."
    echo ${i}
    echo ${o}
    dv-resample-volume --input-image ${i} \
                      --output-image ${o} \
                      --spacing ${SPACING} \
                      --interpolator ${INTERPOLATION}

    #fi

  done

}

#readonly SPACINGS=(1.0 1.5 2.0)
#readonly SPACINGS=(0.5 1.0 1.5 2.5 3.0)
#readonly SPACINGS=(1.0 1.5 2.5 3.0)
readonly SPACINGS=(1.5)

for spacing in ${SPACINGS[*]};
do
  echo "Spacing: ${spacing}"

  # Loop over patients.
  for i_dir in ${INPUT_DIRS[*]};
  do

    # Print the current patient.
    echo ${i_dir}
    
    # set output folder
    o_dir=${i_dir}

    # check whether already done
    small_folder=${o_dir}img-nii-1.5
    if [ -d ${small_folder} ] && [ "$(ls -A  ${small_folder})" ];then
      echo "already done"
      continue
    fi
    
    # check whether nii folder is empty
    nii_folder=${o_dir}img-nii/
    if [ "$(ls -A  ${nii_folder})" ];then
      echo "not empty nifti image"
    else
      echo "empty nifiti image folder!"
      continue
    fi
    
    
    RESAMPLE ${i_dir}img-nii/ ${o_dir}img-nii-1.5/ 1 ${spacing}    '''use 1 for volume image, 2 here for segmentation'''
    #RESAMPLE ${i_dir}seg-nii/ ${o_dir}seg-nii-0.5/ 2 ${spacing}     
    #RESAMPLE ${i_dir}seg-nii-rep-1/ ${o_dir}seg-nii-rep-1/ 0 ${spacing}
 
    # Copy ES file 
    #OUT=${B}/${G}/${P}/
    #cp ${i_dir}es.txt ${OUT}

  done

done
