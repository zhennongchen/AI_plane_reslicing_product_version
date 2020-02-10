#!/usr/bin/env bash

# run in octomore terminal
: '
The CCT volumes are too large to be trained on the network at their current resolution;
moreover, the input resolution is anisotropic, which is not ideal for training.
This script resamples all images and segmentations to a uniform, isotrpic spacing,
dictated by ${CG_SPACING}.
NOTES:
- Inputs come from {img,seg}-nii; outputs go in {img,seg}-nii-sm.
- The script takes quite a long time to run for all images; therefore, by default
it only runs on inputs which are newer than their corresponding resampled outputs.
To override this behavior, set `RUNALL` to `true`.
'

# Include settings and ${CG_*} variables.
. main_step1_default.sh
#. safe-bash.sh

# Get a list of patients.
readonly INPUT_DIRS=( ${CG_RAW_DIR}*/)

# This is the main function, which performs the resampling of either the images or
# segmentations for a single patient.  The input directory name, output directory name,
# interpolation order (0 = nearest neighbot, 1 = linear, 2 = quadratic, 3 = cubic, etc.),
# and whether to run all.

function RESAMPLE() {

  I_DIR=${1}
  O_DIR=${2}
  INTERPOLATION=${3}

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
    mkdir -p $(dirname $(dirname $(dirname ${O_DIR})))
    mkdir -p $(dirname $(dirname ${O_DIR}))
    mkdir -p $(dirname ${O_DIR})
    mkdir -p ${O_DIR}

    # Create the name of the output.
    o=${O_DIR}$(basename ${i})

    # Resample if:
    # - The output doesn't exist.
    # - The input is newer than the output.
    if [ "${i}" -nt "${o}" ]; then

      dv-resample-volume --input-image ${i} \
                         --output-image ${o} \
                         --spacing ${CG_RESAMPLE_SIZE} \
                         --interpolator ${INTERPOLATION}

    fi

  done

}


# Loop over patients.
for i_dir in ${INPUT_DIRS[*]};
do

    # Print the current patient.
    echo ${i_dir}
    o_dir=${CG_RESAMPLE_DIR}$(basename $(dirname $(dirname ${i_dir})))/$(basename $(dirname ${i_dir}))/$(basename ${i_dir})/
    echo ${o_dir}

    RESAMPLE ${i_dir}img-nii/ ${o_dir}img-nii-sm/ 3
    #RESAMPLE ${o_dir}2C/ ${o_dir}mpr-img-sm/ 3
    #RESAMPLE ${i_dir}seg-nii/ ${o_dir}seg-nii-sm/ 0     
    #RESAMPLE ${i_dir}seg-nii-rep-1/ ${o_dir}seg-nii-rep-1/ 0

    # Copy ES file
    #P=$(basename ${i_dir})
    #G=$(basename $(dirname ${i_dir}))

    #OUT=${CG_INPUT_DIR}${G}/${P}/

    #cp ${i_dir}es.txt ${OUT}
  done

