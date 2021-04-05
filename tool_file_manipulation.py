#!/usr/bin/env python

## 
# this script can do file copy and removal
##

import os
import numpy as np
import function_list as ff
import shutil
import pandas as pd
import supplement

np.random.seed(0)
cg = supplement.Experiment()

# # delete
# folders = ff.find_all_target_files(['*/*/slice_num_info.txt'],cg.save_dir)
# print(folders.shape)
# for f in folders:
#     #shutil.rmtree(f)
#     os.remove(f)
# folders = ff.find_all_target_files(['*/*/slice_num_info.txt'],cg.save_dir)
# print(folders.shape)




# file transfer 
main_folder = '/Data/ContijochLab/workspaces/zhennong/AUH_data/nii-images/'
case_list = ff.find_all_target_files(['*/*'],main_folder)
for c in case_list:
    print(os.path.basename(c))
    nii_image_folder = os.path.join(c,'img-nii')
    ff.make_folder([nii_image_folder])
    image_list = ff.find_all_target_files(['*.nii.gz'],c)
    for i in image_list:
        shutil.move(i,os.path.join(nii_image_folder,os.path.basename(i)))
    

#############################################  
# file transfer from octomore
# folder = ff.find_all_target_files(['Resample_MPR'],'/Data/local_storage/Zhennong/')
# print(folder)
# for f in folder:
#     shutil.copytree(f,os.path.join(cg.main_data_dir,'Resample_MPR'))

# # compress
# patient_list = ff.get_patient_list_from_csv(os.path.join(cg.spreadsheet_dir,'Final_patient_list_include.csv'))
# print(len(patient_list))
# for p in patient_list:
#     print(p[0],p[1])
#     f1 = os.path.join(cg.seg_data_dir,p[0],p[1],'seg-nii-1.5-upsample-retouch-adapted-LV')
#     f2 = os.path.join(cg.seg_data_dir,p[0],p[1],'seg-nii-1.5-upsample-retouch-adapted')
#     shutil.make_archive(os.path.join(cg.seg_data_dir,p[0],p[1],'seg-nii-1.5-upsample-retouch-adapted-LV'),'zip',f1)
#     shutil.make_archive(os.path.join(cg.seg_data_dir,p[0],p[1],'seg-nii-1.5-upsample-retouch-adapted'),'zip',f2)
#     shutil.rmtree(f1)
#     shutil.rmtree(f2)

# transfer file to octomore
# patient_list = ff.find_all_target_files(['*/*'],cg.image_data_dir)
# for p in patient_list:
#     patient_id = os.path.basename(p)
#     patient_class = os.path.basename(os.path.dirname(p))
    

#     image_file = ff.find_all_target_files(['img-nii-1.5/0.nii.gz'],p)
#     assert len(image_file) == 1

#     if os.path.isdir(os.path.join(cg.local_dir,patient_class,patient_id,'img-nii-1.5')) == 0:
#         print(patient_class,patient_id)
#         ff.make_folder([os.path.join(cg.local_dir,patient_class),os.path.join(cg.local_dir,patient_class,patient_id),os.path.join(cg.local_dir,patient_class,patient_id,'img-nii-1.5')])
#         shutil.copy(image_file[0],os.path.join(cg.local_dir,patient_class,patient_id,'img-nii-1.5',os.path.basename(image_file[0])))