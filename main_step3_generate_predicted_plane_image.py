#!/usr/bin/env python

# this script generates image with three LAX planes + A SAX stack

import function_list as ff
import os
import math
import numpy as np
import nibabel as nib 
import supplement
from PIL import Image
cg = supplement.Experiment()

WL = 500
WW = 900
native_res = 1
if native_res == 1:
    plane_image_size = [480,480,1]
else:
    plane_image_size = [160,160,1]

scale = [1,1,0.67]


# function to make the image
def plane_image(save_path,volume_data,plane_image_size,WL,WW,image_center, vector_2C,vector_3C,vector_4C,vector_SA,center_list):
    
    # define interpolation matrix
    inter = ff.define_interpolation(volume_data,Fill_value=volume_data.min(),Method='linear')
    
    # reslice long axis
    twoc = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_2C['t'],vector_2C['x'],vector_2C['y'],1,1,inter)
    threec = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_3C['t'],vector_3C['x'],vector_3C['y'],1,1,inter)
    fourc = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_4C['t'],vector_4C['x'],vector_4C['y'],1,1,inter)

    # reslice short axis
    sax_collection = []
    for i in range(0,9):
        sax_collection.append(ff.reslice_mpr(np.zeros(plane_image_size),center_list[i],vector_SA['x'],vector_SA['y'],1,1,inter))
    assert len(sax_collection) == 9

    # normalize by WL and WW and then orient
    twoc_n = ff.set_window(twoc,WL,WW); twoc_n = np.flip(twoc_n.T,0)
    threec_n = ff.set_window(threec,WL,WW); threec_n = np.flip(threec_n.T,0)
    fourc_n = ff.set_window(fourc,WL,WW); fourc_n = np.flip(fourc_n.T,0)

    sax_collection_n = []
    for ii in range(0,9):
        s_n = ff.set_window(sax_collection[ii],WL,WW); s_n = s_n.T
        sax_collection_n.append(s_n)
    

    # make image
    [h,w,d] = plane_image_size
    I = np.zeros((h*3,w*4,3))
    I[0:h,0:w,0] = twoc_n; I[0:h,0:w,1] = twoc_n; I[0:h,0:w,2] = twoc_n
    I[h:h*2,0:w,0] = threec_n; I[h:h*2,0:w,1] = threec_n; I[h:h*2,0:w,2] = threec_n
    I[h*2:h*3,0:w,0] = fourc_n; I[h*2:h*3,0:w,1] = fourc_n; I[h*2:h*3,0:w,2] = fourc_n
    I[0:h,w:w*2,0] = sax_collection_n[0]; I[0:h,w:w*2,1] = sax_collection_n[0]; I[0:h,w:w*2,2] = sax_collection_n[0]
    I[0:h,w*2:w*3,0] = sax_collection_n[1]; I[0:h,w*2:w*3,1] = sax_collection_n[1]; I[0:h,w*2:w*3,2] = sax_collection_n[1]
    I[0:h,w*3:w*4,0] = sax_collection_n[2]; I[0:h,w*3:w*4,1] = sax_collection_n[2]; I[0:h,w*3:w*4,2] = sax_collection_n[2]
    I[h:h*2,w:w*2,0] = sax_collection_n[3]; I[h:h*2,w:w*2,1] = sax_collection_n[3]; I[h:h*2,w:w*2,2] = sax_collection_n[3]
    I[h:h*2,w*2:w*3,0] = sax_collection_n[4]; I[h:h*2,w*2:w*3,1] = sax_collection_n[4]; I[h:h*2,w*2:w*3,2] = sax_collection_n[4]
    I[h:h*2,w*3:w*4,0] = sax_collection_n[5]; I[h:h*2,w*3:w*4,1] = sax_collection_n[5]; I[h:h*2,w*3:w*4,2] = sax_collection_n[5]
    I[h*2:h*3,w:w*2,0] = sax_collection_n[6]; I[h*2:h*3,w:w*2,1] = sax_collection_n[6]; I[h*2:h*3,w:w*2,2] = sax_collection_n[6]
    I[h*2:h*3,w*2:w*3,0] = sax_collection_n[7]; I[h*2:h*3,w*2:w*3,1] = sax_collection_n[7]; I[h*2:h*3,w*2:w*3,2] = sax_collection_n[7]
    I[h*2:h*3,w*3:w*4,0] = sax_collection_n[8]; I[h*2:h*3,w*3:w*4,1] = sax_collection_n[8]; I[h*2:h*3,w*3:w*4,2] = sax_collection_n[8]

    # save
    Image.fromarray((I * 255).astype('uint8')).save(save_path)


# main function for image
patient_list = ff.find_all_target_files(['*'],cg.patient_dir)
for patient in patient_list:
    patient_id = os.path.basename(patient)
    patient_class = os.path.basename(os.path.dirname(patient))
    print(patient_class,patient_id)

    # define save_folder
    save_folder = os.path.join(patient,'planes_pred_high_res')
    ff.make_folder([save_folder])

    seg = nib.load(os.path.join(patient,'seg-pred/pred_s_0.nii.gz')); seg_data = seg.get_fdata()
    volume_dim = nib.load(os.path.join(patient,'img-nii-sm/0.nii.gz')).shape
    image_center = np.array([(volume_dim[0]-1)/2,(volume_dim[1]-1)/2,(volume_dim[-1]-1)/2]) 

    # load vectors
    vector_2C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/pred_2C_t.npy'),os.path.join(patient,'vector-pred/pred_2C_r.npy'),scale, image_center)
    vector_3C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/pred_3C_t.npy'),os.path.join(patient,'vector-pred/pred_3C_r.npy'),scale, image_center)
    vector_4C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/pred_4C_t.npy'),os.path.join(patient,'vector-pred/pred_4C_r.npy'),scale, image_center)
    vector_SA = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/pred_BASAL_t.npy'),os.path.join(patient,'vector-pred/pred_BASAL_r.npy'),scale, image_center)

    # define plane num for SAX stack:
    normal_vector = ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])) 
    a,b = ff.find_num_of_slices_in_SAX(np.zeros([160,160,1]),image_center,vector_SA['t'],vector_SA['x'],vector_SA['y'],seg_data,2.59)
    t_file = open(os.path.join(patient,"slice_num_info.txt"),"w+")
    t_file.write("num of slices before basal = %d\nnum of slices after basal = %d" % (a, b))
    t_file.close()
    print(a,b)


    # transfer translation vector into native res:
    if native_res == 1:
        # get native res:
        vector_2C = ff.adapt_reslice_vector_for_native_resolution(vector_2C,os.path.join(patient,'img-nii-sm/0.nii.gz'),os.path.join(patient,'img-nii/0.nii.gz'))
        vector_3C = ff.adapt_reslice_vector_for_native_resolution(vector_3C,os.path.join(patient,'img-nii-sm/0.nii.gz'),os.path.join(patient,'img-nii/0.nii.gz'))
        vector_4C = ff.adapt_reslice_vector_for_native_resolution(vector_4C,os.path.join(patient,'img-nii-sm/0.nii.gz'),os.path.join(patient,'img-nii/0.nii.gz'))
        vector_SA = ff.adapt_reslice_vector_for_native_resolution(vector_SA,os.path.join(patient,'img-nii-sm/0.nii.gz'),os.path.join(patient,'img-nii/0.nii.gz'))
        
        volume_dim = nib.load(os.path.join(patient,'img-nii/0.nii.gz')).shape
        image_center = np.array([(volume_dim[0]-1)/2,(volume_dim[1]-1)/2,(volume_dim[-1]-1)/2])

    # get a center list of SAX stack
    if native_res == 1:
        pix_dim = ff.get_voxel_size(os.path.join(patient,'img-nii/0.nii.gz'))
        pix_size = ff.length(pix_dim)
        print(pix_size)
        normal_vector = ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])) 
        center_list = ff.find_center_list_whole_stack(image_center + vector_SA['t'],normal_vector,a,b,8,pix_size)
    else:
        center_list = ff.find_center_list_whole_stack(image_center + vector_SA['t'],normal_vector,a,b,8,2.59)

    # get the index of each planes of 9-plane SAX stack
    index_list,center_list9 = ff.resample_SAX_stack_into_particular_num_of_planes(range(2,center_list.shape[0]),9,center_list)
    print(range(2,center_list.shape[0]),index_list)

    # reslice mpr for every time frame
    if native_res == 1:
        volume_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii/*.nii.gz'],patient),2)
    else:
        volume_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii-sm/*.nii.gz'],patient),2)

    for v in volume_list:
        volume = nib.load(v)
        volume_data = volume.get_fdata()
        time = ff.find_timeframe(v,2)
        save_path = os.path.join(save_folder,str(time) +'.png')
        plane_image(save_path,volume_data,plane_image_size,WL,WW,image_center, vector_2C,vector_3C,vector_4C,vector_SA,center_list9)
        print('finish time '+str(time))

    # make the movie
    pngs = ff.sort_timeframe(ff.find_all_target_files(['*.png'],save_folder),1)
    save_movie_path = os.path.join(save_folder,patient_id+'_predicted_planes.mp4')
    if len(pngs) >= 10:
        framerate = len(pngs)
    else:
        framerate = 10
    ff.make_movies(save_movie_path,pngs,10)

print('finish making image')





    
    