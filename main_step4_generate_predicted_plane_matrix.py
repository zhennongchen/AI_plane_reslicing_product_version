#!/usr/bin/env python

# this script generates numpy matrix of predicted planes. this numpy matrix can be saved into mat file
# and then convert to dicom image in MATLAB.
# the most important thing here is to get the correct x and y vector with correct length, which not required when generating images. 
# see tool_understand_native_and_resampled_dimension.npy for related info.

import function_list as ff
import os
import math
import numpy as np
import nibabel as nib 
import supplement
from PIL import Image
import scipy.io as sio
cg = supplement.Experiment()

native_res = 1
if native_res == 1:
    plane_image_size = [480,480,1]
else:
    plane_image_size = [160,160,1]


task_list = ['2C','3C','4C']
save_numpy = 1
save_mat = 1

# function to make the image
def plane_matrix(volume_data,plane_image_size,image_center,vector_2C,vector_3C,vector_4C,vector_SA,center_list):
    
    # define interpolation matrix
    inter = ff.define_interpolation(volume_data,Fill_value=volume_data.min(),Method='linear')
    
    # reslice long axis
    twoc = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_2C['t'],vector_2C['x'],vector_2C['y'],vector_2C['final_s'][0],vector_2C['final_s'][1],inter)
    threec = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_3C['t'],vector_3C['x'],vector_3C['y'],vector_3C['final_s'][0],vector_3C['final_s'][1],inter)
    fourc = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_4C['t'],vector_4C['x'],vector_4C['y'],vector_4C['final_s'][0],vector_4C['final_s'][1],inter)

    # reslice short axis
    sax_collection = []
    for i in range(0,9):
        if i < 11:
            sax_collection.append(ff.reslice_mpr(np.zeros(plane_image_size),center_list[i],vector_SA['x'],vector_SA['y'],vector_SA['final_s'][0],vector_SA['final_s'][1],inter))
        else:
            sax_collection.append(ff.reslice_mpr(np.zeros(plane_image_size),center_list[i],vector_SA['x'],vector_SA['y'],vector_SA['final_s'][0],vector_SA['final_s'][1],inter))
    assert len(sax_collection) == 9
    sax_collection = np.asarray(sax_collection).reshape((plane_image_size[0],plane_image_size[1],9))

    return twoc,threec,fourc,sax_collection



# main function for image
patient_list = ff.find_all_target_files(['AN32_*','AN51_*'],cg.patient_dir)
for patient in patient_list:
    patient_id = os.path.basename(patient)
    patient_class = os.path.basename(os.path.dirname(patient))
    print(patient_class,patient_id)

    # define save_folder
    save_folder = os.path.join(patient,'planes_pred_high_res_npy')
    ff.make_folder([save_folder,os.path.join(save_folder,'2C'),os.path.join(save_folder,'3C'),os.path.join(save_folder,'4C'),os.path.join(save_folder,'SAX')])

    seg = nib.load(os.path.join(patient,'seg-pred/pred_s_0.nii.gz')); seg_data = seg.get_fdata()
    volume_dim = nib.load(os.path.join(patient,'img-nii-sm/0.nii.gz')).shape
    image_center = np.array([(volume_dim[0]-1)/2,(volume_dim[1]-1)/2,(volume_dim[-1]-1)/2]) 

    # load vectors
    scale = [1,1,0.67] # default
    vector_2C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/pred_2C_t.npy'),os.path.join(patient,'vector-pred/pred_2C_r.npy'),scale, image_center)
    vector_3C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/pred_3C_t.npy'),os.path.join(patient,'vector-pred/pred_3C_r.npy'),scale, image_center)
    vector_4C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/pred_4C_t.npy'),os.path.join(patient,'vector-pred/pred_4C_r.npy'),scale, image_center)
    vector_SA = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/pred_BASAL_t.npy'),os.path.join(patient,'vector-pred/pred_BASAL_r.npy'),scale, image_center)

    # define plane num for SAX stack:
    normal_vector = ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])) 
    a,b = ff.find_num_of_slices_in_SAX(np.zeros([160,160,1]),image_center,vector_SA['t'],vector_SA['x'],vector_SA['y'],seg_data,2.59) # 2.59 is the length of [1.5,1.5,1.5]

    # transfer vector into native res:
    if native_res == 1:
        V = []
        for v in [vector_2C,vector_3C,vector_4C,vector_SA]:
            v = ff.adapt_reslice_vector_for_native_resolution(v,os.path.join(patient,'img-nii-sm/0.nii.gz'),os.path.join(patient,'img-nii/0.nii.gz'))
            v['s'] = ff.set_scale_for_unequal_x_and_y(v)
            V.append(v)
        [vector_2C,vector_3C,vector_4C,vector_SA] = [V[0],V[1],V[2],V[3]] 

        volume_dim = nib.load(os.path.join(patient,'img-nii/0.nii.gz')).shape
        image_center = np.array([(volume_dim[0]-1)/2,(volume_dim[1]-1)/2,(volume_dim[-1]-1)/2])

    # get a center list of SAX stack
    if native_res == 1:
        pix_dim = ff.get_voxel_size(os.path.join(patient,'img-nii/0.nii.gz'))
        pix_size = ff.length(pix_dim)
        normal_vector = ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])) 
        center_list = ff.find_center_list_whole_stack(image_center + vector_SA['t'],normal_vector,a,b,8,pix_size)
    else:
        center_list = ff.find_center_list_whole_stack(image_center + vector_SA['t'],normal_vector,a,b,8,2.59)

    # get the index of each planes of 9-plane SAX stack (9 planes should start from MV and end with apex, convering the whole LV)
    index_list,center_list9 = ff.resample_SAX_stack_into_particular_num_of_planes(range(2,center_list.shape[0]),9,center_list)

    # reslice mpr for every time frame
    if native_res == 1:
        volume_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii/*.nii.gz'],patient),2)
    else:
        volume_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii-sm/*.nii.gz'],patient),2)

    count = 0
    if save_numpy == 1:
        lax_collection = [ [] for j in range(0,len(task_list))]
        for v in volume_list:
            volume = nib.load(v)
            volume_data = volume.get_fdata()
            time = ff.find_timeframe(v,2)
            twoc,threec,fourc,_ = plane_matrix(volume_data,plane_image_size,image_center,vector_2C,vector_3C,vector_4C,vector_SA,center_list9)
            # save into numpy matrix
            for i in range(0,len([twoc,threec,fourc])):
                c = [twoc,threec,fourc][i]
                lax_collection[i].append(c[:,:,0])
                np.save(os.path.join(save_folder,task_list[i],task_list[i]+'_'+str(time)),c)
            if count == 0:
                twoc_collection = np.copy(twoc)
                threec_collection = np.copy(threec)
                fourc_collection = np.copy(fourc)
            else:
                twoc_collection = np.concatenate((twoc_collection,twoc),axis = 2)
                threec_collection = np.concatenate((threec_collection,threec),axis = 2)
                fourc_collection = np.concatenate((fourc_collection,fourc),axis = 2)
            print('finish time frame ',time)
            count += 1
            
        
        print(twoc_collection.shape)
                       
        np.save(os.path.join(save_folder,'2C','2C_full_cycle'),twoc_collection)
        np.save(os.path.join(save_folder,'3C','3C_full_cycle'),threec_collection)
        np.save(os.path.join(save_folder,'4C','4C_full_cycle'),fourc_collection)


    if save_mat == 1:
        twoc_collection = np.load(os.path.join(save_folder,'2C','2C_full_cycle.npy'),allow_pickle = True)
        threec_collection = np.load(os.path.join(save_folder,'3C','3C_full_cycle.npy'),allow_pickle = True)
        fourc_collection = np.load(os.path.join(save_folder,'4C','4C_full_cycle.npy'),allow_pickle = True)

        sio.savemat(os.path.join(save_folder,patient_id+'_LAX_collection.mat'), {'twoc':twoc_collection,'threec':threec_collection,'fourc':fourc_collection})

    

    

    





    
    