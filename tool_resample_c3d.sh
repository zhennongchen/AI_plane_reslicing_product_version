#!/usr/bin/env bash
# run in docker c3d

# Include settings and ${CG_*} variables.
. ./main_step1_defaults.sh



# Get a list of patients.
readonly patients=( ${CG_PATIENT_DIR}AN51_*/ ) 

img_or_seg=1 # 1 is image, 0 is seg

if ((${img_or_seg} == 1))
then
img_folder="img-nii"
else
img_folder="seg-nii"
fi

for p in ${patients[*]};
do
    if ! [ -d ${p}${img_folder} ] ;then
        echo "no image/seg"
        continue
    fi

    # find out the patient id
    patient_id=$(basename ${p})
    echo ${patient_id}

    # set output folder
    if ((${img_or_seg} == 1));then
    o_dir=${p}img-nii-sm
    else
    o_dir=${p}seg-nii-sm
    fi
    mkdir -p ${o_dir}
    
    # check whether already done
    if [ -d ${o_dir} ] && [ "$(ls -A  ${o_dir})" ] ;then
        echo "already done"
        continue
    else
        echo ${patient_class}
        echo ${patient_id}

        # find all the data with original resolution
        IMGS=(${p}${img_folder}/*.nii.gz)
        for i in $(seq 0 $(( ${#IMGS[*]} - 1 )));
        do
            i_file=${IMGS[${i}]}
            o_file=${o_dir}/$(basename ${i_file})
            echo ${o_file}
            
            if ((${img_or_seg} == 1))
            then
                c3d ${i_file} -interpolation Cubic -resample-mm 1.5x1.5x1.5mm -o ${o_file}
            else
                c3d ${i_file} -interpolation NearestNeighbor -resample-mm 1.5x1.5x1.5mm -o ${o_file}
            fi
            
        done
    fi
  

done


