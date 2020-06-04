#!/usr/bin/env python

'''in case the img-nii-spacing folder contains files with name of No-ph.nii.gz instead of No.nii.gz'''
import os
import numpy as np
import segcnn
import glob as gb
import shutil
import function_list as ff
cg = segcnn.Experiment()


def number(n):
    test = '0123456789.'
    for i in range(0,len(test)):
        if n == test[i]:
            return i
    return 100

def check_name(name):
    n = os.path.basename(name)
    if number(n[1]) == 10:
        return 0
    if number(n[1]) < 10:
        if number(n[2]) > 20:
            return 2
        else:
            return 0
    else:
        return 1 

            

def rename(file_list):
    for i in file_list:
        print(os.path.basename(i),check_name(i))
        if check_name(i) == 1:
            n = os.path.basename(i)
            shutil.copyfile(i,os.path.join(os.path.dirname(i),n[0]+'.nii.gz'))
            os.remove(i)
        if check_name(i) == 2:
            n = os.path.basename(i)
            shutil.copyfile(i,os.path.join(os.path.dirname(i),n[0:2]+'.nii.gz'))
            os.remove(i)
        

patient_list = ff.find_all_target_files(['*'],cg.main_dir)
print(patient_list)

# make folder for each patient
for p in patient_list:
    patient_id = os.path.basename(p)
    print(patient_id)
    #patient_cat = os.path.basename(os.path.dirname(p))
    #print(patient_cat,patient_id,'\n')
    
    a_file = ff.find_all_target_files(['*.nii.gz'],os.path.join(p,'img-nii-1.5'))
    rename(a_file)
