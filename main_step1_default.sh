# enter the name of main directory
export CG_MAIN_DIR="/Data/McVeighLabSuper/projects/Zhennong/Dataset/Tendyne_Patients_processed/"

# if you have non-resampled image:
# enter the name of folder where you save all the patient cases with original images (not resampled)
# e.g. if the cases are saved as /home/jack/patient_000, CG_RAW_DIR = '/home/jack/'
#export CG_RAW_DIR="/media/McVeighLab/wip/ucsd_lvad/to_be_reviewed/"
#export CG_RESAMPLE_DIR="/home/cnn/Documents/Resample_Data/"
export CG_RAW_DIR="/Data/McVeighLabSuper/projects/Zhennong/Dataset/Tendyne_Patients_processed/"


# if you already resample all your images:
# enter the name of folder where you save all the patient cases with resampled images
# all the predicted output will also be saved in each patient individual sub-folder in this folder
# e.g. if the cases are saved as /home/jack/patient_000, CG_INPUT_DIR = '/home/jack/'
export CG_PATIENT_DIR="/Data/McVeighLabSuper/projects/Zhennong/AI/Product_Test/Patient_Folder/" 

# enter the name of folder where you save the trained deep learning model 
export CG_MODEL_DIR="/Data/McVeighLabSuper/projects/Zhennong/AI/CNN/all-classes-all-phases-data-1.5/Model/" 



# define some parameters

export CUDA_VISIBLE_DEVICES="1" # GPU you use: 0 or 1

export CG_NUM_CLASSES=5 # the number of labels: 10 for LV, 14 for RV

export CG_RESAMPLE_SIZE=1.5 # resampled pixel size in mm

export CG_SAX_STACK_THICKNESS=8 # the thickness between two adjacenet SAX stack slices in mm
 
# parameters for generator
export CG_BATCH_SIZE=1
export CG_XY_RANGE="0.1"   #0.1
export CG_ZM_RANGE="0.1"  #0.1
export CG_RT_RANGE="10"   #15

# the dimension we crop or pad the image to have uniform size
export CG_CROP_X=160
export CG_CROP_Y=160
export CG_CROP_Z=96

export CG_SEED=0 # seed for randomization

export CG_CONV_DEPTH_MULTIPLIER=1 



