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

cg = supplement.Experiment()

# delete
# folders = ff.find_all_target_files(['*/*/seg-pred-0.625-4classes'],cg.seg_data_dir)
# print(folders.shape)
# for f in folders:
#     shutil.rmtree(f)
# folders = ff.find_all_target_files(['*/*/seg-pred-0.625-4classes'],cg.seg_data_dir)
# print(folders.shape)



# file transfer 
print(cg.final_dir)
patient_list = ff.find_all_target_files(['Abnormal/*','Normal/*'],cg.final_dir)
main_folder = os.path.join(os.path.dirname(cg.final_dir),'Segs')
print(patient_list.shape)
for p in patient_list:
    patient_id = os.path.basename(p)
    patient_class = os.path.basename(os.path.dirname(p))
    print(patient_class,patient_id)
    
    
    ff.make_folder([os.path.join(main_folder,patient_class,patient_id)])
    
    # img_folder = os.path.join(p,'img-nii-1.5')
    # shutil.copytree(img_folder,os.path.join(cg.local_dir,patient_class,patient_id,'img-nii-1.5'))
   
    seg_folder = os.path.join(p,'seg-pred')
    shutil.copytree(seg_folder,os.path.join(main_folder,patient_class,patient_id,'seg-pred'))
    
#     #txt_file = os.path.join(cg.seg_data_dir,patient_class,patient_id,'time_frame_picked_for_pretrained_AI.txt')
#     #shutil.copy(txt_file,os.path.join(cg.local_dir,patient_class,patient_id,'time_frame_picked_for_pretrained_AI.txt'))


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
  