#!/usr/bin/env python

# this script generates image with three LAX planes + A SAX stack

import function_list as ff
import os
import numpy as np
import nibabel as nib 
import supplement
from PIL import Image
cg = supplement.Experiment()

WL = 500
WW = 900
plane_image_size = [160,160,1]
scale = [1,1,0.67]



# function to make the image
def plane_image(save_path,volume_data,plane_image_size,WL,WW,vector_2C,vector_3C,vector_4C,vector_SA,center_list):
    
    # define interpolation matrix
    inter = ff.define_interpolation(volume_data,Fill_value=volume_data.min(),Method='linear')
    # define image center
    image_center = vector_2C['img_center']

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
        s_n = ff.set_window(sax_collection[ii],WL,WW); s_n = np.flip(s_n.T,0)
        sax_collection_n.append(s_n)
    

    # make image
    I = np.zeros((160*3,160*4,3))
    I[0:160,0:160,0] = twoc_n; I[0:160,0:160,1] = twoc_n; I[0:160,0:160,2] = twoc_n
    I[160:320,0:160,0] = threec_n; I[160:320,0:160,1] = threec_n; I[160:320,0:160,2] = threec_n
    I[320:480,0:160,0] = fourc_n; I[320:480,0:160,1] = fourc_n; I[320:480,0:160,2] = fourc_n
    I[0:160,160:320,0] = sax_collection_n[0]; I[0:160,160:320,1] = sax_collection_n[0]; I[0:160,160:320,2] = sax_collection_n[0]
    I[0:160,320:480,0] = sax_collection_n[1]; I[0:160,320:480,1] = sax_collection_n[1]; I[0:160,320:480,2] = sax_collection_n[1]
    I[0:160,480:640,0] = sax_collection_n[2]; I[0:160,480:640,1] = sax_collection_n[2]; I[0:160,480:640,2] = sax_collection_n[2]
    I[160:320,160:320,0] = sax_collection_n[3]; I[160:320,160:320,1] = sax_collection_n[3]; I[160:320,160:320,2] = sax_collection_n[3]
    I[160:320,320:480,0] = sax_collection_n[4]; I[160:320,320:480,1] = sax_collection_n[4]; I[160:320,320:480,2] = sax_collection_n[4]
    I[160:320,480:640,0] = sax_collection_n[5]; I[160:320,480:640,1] = sax_collection_n[5]; I[160:320,480:640,2] = sax_collection_n[5]
    I[320:480,160:320,0] = sax_collection_n[6]; I[320:480,160:320,1] = sax_collection_n[6]; I[320:480,160:320,2] = sax_collection_n[6]
    I[320:480,320:480,0] = sax_collection_n[7]; I[320:480,320:480,1] = sax_collection_n[7]; I[320:480,320:480,2] = sax_collection_n[7]
    I[320:480,480:640,0] = sax_collection_n[8]; I[320:480,480:640,1] = sax_collection_n[8]; I[320:480,480:640,2] = sax_collection_n[8]

    # save
    Image.fromarray((I * 255).astype('uint8')).save(save_path)


# main function for image
patient_list = ff.find_all_target_files(['*'],cg.patient_dir)
for patient in patient_list:
    patient_id = os.path.basename(patient)
    patient_class = os.path.basename(os.path.dirname(patient))
    print(patient_class,patient_id)

    # define save_folder
    save_folder = os.path.join(patient,'planes_manual')
    ff.make_folder([save_folder])


    # load vectors
    vector_2C = ff.get_ground_truth_vectors(os.path.join(patient,'vector-manual/manual_2C.npy'))
    vector_3C = ff.get_ground_truth_vectors(os.path.join(patient,'vector-manual/manual_3C.npy'))
    vector_4C = ff.get_ground_truth_vectors(os.path.join(patient,'vector-manual/manual_4C.npy'))
    vector_SA = ff.get_ground_truth_vectors(os.path.join(patient,'vector-manual/manual_BASAL.npy'))
    img_center = vector_2C['img_center']
    

    # get the centerpoint list of SAX stack
    normal_vector = ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])) 
    center_list = ff.find_center_list(img_center + vector_SA['t'],-normal_vector,9,8)

    
    
    
    # reslice mpr for every time frame
    volume_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii-sm/*.nii.gz'],patient),2)
    for v in volume_list:
        volume = nib.load(v)
        volume_data = volume.get_fdata()
        time = ff.find_timeframe(v,2)
        save_path = os.path.join(save_folder,str(time) +'.png')
        plane_image(save_path,volume_data,plane_image_size,WL,WW,vector_2C,vector_3C,vector_4C,vector_SA,center_list)
        print('finish time '+str(time))

    # make the movie
    pngs = ff.sort_timeframe(ff.find_all_target_files(['*.png'],save_folder),1)
    save_movie_path = os.path.join(save_folder,patient_id+'_manual_planes.mp4')
    if len(pngs) >= 10:
        framerate = len(pngs)
    else:
        framerate = 10
    ff.make_movies(save_movie_path,pngs,10)

print('finish making image')





    
    