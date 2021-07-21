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

# delete
# patient_list_excel = pd.read_excel(os.path.join('/Data/McVeighLabSuper/wip/zhennong','Patients_We_need_to_reslice.xlsx'))
# patient_list = []
# for i in range(0,patient_list_excel.shape[0]):
#     patient_list.append([patient_list_excel.iloc[i]['Patient_Class'], patient_list_excel.iloc[i]['Patient_ID']])

# for i in range(0,len(patient_list)):
#     patient_class = patient_list[i][0]
#     patient_id = patient_list[i][1]
#     folder = os.path.join('/Data/local_storage/Zhennong/Resample_MPR',patient_class,patient_id)
#     if os.path.isdir(folder) == 1:
#         shutil.rmtree(folder)
#     else:
#         folder = os.path.join('/Data/local_storage/Zhennong/Resample_MPR_2020_after_Junes',patient_class,patient_id)
#         if os.path.isdir(folder) == 1:
#             shutil.rmtree(folder)
#         else:
#             print(patient_id)


# file transfer 
# patient_list = ff.find_all_target_files(['*/*'],os.path.join(cg.main_data_dir,'Plane_movies'))
# for p in patient_list:
#     patient_id = os.path.basename(p)
#     patient_class = os.path.basename(os.path.dirname(p))
#     ff.make_folder([os.path.join(cg.main_data_dir,'Plane_movies_only_movies',patient_class,patient_id)])
#     print(patient_class,patient_id)


#     movie_lists = ff.find_all_target_files(['*.mp4'],p)
#     assert len(movie_lists) == 2
#     for m in movie_lists:
#         if os.path.isfile(os.path.join(cg.main_data_dir,'Plane_movies_only_movies',patient_class,patient_id,os.path.basename(m))) ==0:
#             shutil.copy(m,os.path.join(cg.main_data_dir,'Plane_movies_only_movies',patient_class,patient_id,os.path.basename(m)))



#############################################  
# file transfer from octomore
folder = ff.find_all_target_files(['Resample_MPR'],'/Data/local_storage/Zhennong/')
print(folder)
for f in folder:
    shutil.copytree(f,os.path.join(cg.main_data_dir,'Resample_MPR'))

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