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
# folders = ff.find_all_target_files(['*/*/planes_pred_lines2'],cg.final_dir)
# print(folders.shape)
# for f in folders:
#     shutil.rmtree(f)
# folders = ff.find_all_target_files(['*/*/planes_pred_lines2'],cg.final_dir)
# print(folders.shape)




# file transfer 
# main_folder = os.path.join(os.path.dirname(cg.final_dir),'Validation_Dataset_for_EHJ_manuscript')
# print(main_folder)
# patient_list = pd.read_csv(os.path.join(os.path.dirname(main_folder),'Validation_patient_list_for_manuscript.csv'))
# new_patient_list = []
# for i in range(0,patient_list.shape[0]):
#     case = patient_list.iloc[i]
#     index = case['Index']
#     patient_id = case['Patient_ID']
#     patient_class = case['Patient_Class']
#     new_patient_list.append([index,patient_class,patient_id])

# new_patient_list = np.asarray(new_patient_list)
# np.random.shuffle(new_patient_list)
# #print(new_patient_list[0:10])


# result = []
# for i in range(0,new_patient_list.shape[0]):
#     p = new_patient_list[i]
#     index = p[0]
#     patient_id = p[-1]
#     patient_class = p[1]
#     print(i, index, patient_class,patient_id)
    
#     #ff.make_folder([os.path.join(main_folder,'Data','Case_'+str(i))])
    
#     plane_movie = ff.find_all_target_files(['*planes.mp4'],os.path.join(os.path.dirname(main_folder),'Planes',patient_class,patient_id,'planes_pred_lines_2'))
#     if plane_movie.shape[0] == 0:
#         plane_movie = ff.find_all_target_files(['*planes.mp4'],os.path.join(os.path.dirname(main_folder),'Planes',patient_class,patient_id,'planes_pred_lines_upsample'))
#         if plane_movie.shape[0] == 0:
#             plane_movie = ff.find_all_target_files(['*planes.mp4'],os.path.join(os.path.dirname(main_folder),'Planes',patient_class,patient_id,'planes_pred_lines'))

#             if plane_movie.shape[0] != 1:
#                 ValueError('no planes')
#     copy_des = os.path.join(main_folder,'Data','Case_'+str(i)+'_predicted_plane_movie.mp4')
#     if os.path.isfile(copy_des) == 0:
#         shutil.copy(plane_movie[0],copy_des)

#     # seg_files = ff.find_all_target_files(['*.txt','*no_id.eps'],os.path.join(os.path.dirname(main_folder),'Segs',patient_class,patient_id))
#     # if seg_files.shape[0] != 2:
#     #     ValueError('no segs')
#     # for s in seg_files:
#     #     copy_des = os.path.join(main_folder,'Data','Case_'+str(i),os.path.basename(s))
#     #     if os.path.isfile(copy_des) == 0:
#     #         shutil.copy(s,copy_des)
    
#     result.append([i, index, patient_class,patient_id])

# df = pd.DataFrame(result,columns = ['Index_random','Index','Patient_Class','Patient_ID'])
# df.to_excel(os.path.join(os.path.dirname(main_folder),'Random_Shuffle_Validation_Patient_List_For_Manuscript.xlsx'),index = False)
  
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
  