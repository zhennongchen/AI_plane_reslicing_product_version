## define parameters
export CUDA_VISIBLE_DEVICES="0"

export CG_NUM_CLASSES=4 
export CG_RELABEL_LVOT=1

export CG_SPACING=1.5

export CG_SEED=0

export CG_BATCH_SIZE=1

export CG_CROP_X=160
export CG_CROP_Y=160
export CG_CROP_Z=96

export CG_CONV_DEPTH_MULTIPLIER=1
export CG_FEATURE_DEPTH=8


# folders
export CG_MAIN_DATA_DIR="/Data/McVeighLab/wip/zhennong/"
export CG_IMAGE_DATA_DIR=${CG_MAIN_DATA_DIR}nii-images/
export CG_MODEL_DIR="/Data/McVeighLab/projects/Zhennong/AI/CNN/all-classes-all-phases-data-1.5/" 
# export CG_OCTOMORE_DIR="/Data/local_storage/Zhennong/Ashish_ResyncCT/"
export CG_OCTOMORE_DIR="/Data/ExtraDrive/workspaces/zhennong/VR_Data"
export CG_SAVE_DIR="/Data/McVeighLab/wip/zhennong/predicted_plane_vectors/"
export CG_FINAL_DIR="/Data/McVeighLab/wip/zhennong/DL_predicted_planes/"





