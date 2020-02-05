#!/usr/bin/env python
# Python libraries
import os
import numpy as np
import nibabel as nib
import function_list as ff
from plane_image_generate_function import generate_plane
import segcnn
import dvpy as dv
import dvpy.tf
import cv2 
import matplotlib
matplotlib.use('Agg')
cg = segcnn.Experiment()

# find the patient_list
patient_list = ff.find_all_target_files(['ucsd_*/*'],cg.patient_dir)

for patient in patient_list:
    patient_class = os.path.basename(os.path.dirname(patient))
    patient_id = os.path.basename(patient)
    print(patient_class,patient_id)

    # load universal parameters
    volume_dim = nib.load(os.path.join(patient,'img-nii-sm/0.nii.gz')).shape
    image_center = np.array([(volume_dim[0]-1)/2,(volume_dim[1]-1)/2,(volume_dim[-1]-1)/2]) # center of the CT volume
    plane_dim = [cg.dim[0],cg.dim[1],1] # default resliced plane dimension

    # load segmentation
    seg = nib.load(os.path.join(patient,'seg-pred/seg_0.nii.gz')); seg_data = seg.get_fdata()
    
    # load plane-specific vectors
    pred_2C = ff.get_predicted_vectors(patient,'vectors-pred/2C-t.npy','vectors-pred/2C-r.npy',image_center)
    pred_3C = ff.get_predicted_vectors(patient,'vectors-pred/3C-t.npy','vectors-pred/3C-r.npy',image_center)
    pred_4C = ff.get_predicted_vectors(patient,'vectors-pred/4C-t.npy','vectors-pred/4C-r.npy',image_center)
    pred_SA = ff.get_predicted_vectors(patient,'vectors-pred/BASAL-t.npy','vectors-pred/BASAL-r.npy',image_center)

    # get SAX stack center list
    n_SA = ff.normalize(np.cross(pred_SA['x'],pred_SA['y'])) # normal vector of SAX plane
    a,b = ff.find_num_of_slices_in_SAX(np.zeros(plane_dim),image_center,pred_SA['t'],pred_SA['x'],pred_SA['y'],seg_data)
    center_list = ff.find_center_list_whole_stack(image_center + pred_SA['t'],n_SA,a,b,cg.slice_thickness)

    # find the position of basal, mid-cavity, and apical image plane
    _,_,base,mid,apical = ff.particular_thirds_in_stack(a,b,9,3,5,7)
    base_center = center_list[0] + n_SA * cg.slice_thickness * (base-1) / cg.pixel_size
    mid_center = center_list[0] + n_SA * cg.slice_thickness * (mid-1) / cg.pixel_size
    apical_center = center_list[0] + n_SA * cg.slice_thickness * (apical-1) / cg.pixel_size

    # make directories to prepare the image + movie save
    save_folder = os.path.join(patient,'planes-pred')
    save_folder_img = os.path.join(save_folder,'images_for_each_time_frame')
    ff.make_folder([save_folder,save_folder_img])

    # make plane images for each time frame 
    volume_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii-sm/*.nii.gz'],patient),2)
    for v in volume_list:
        volume = nib.load(v)
        volume_data = volume.get_fdata()
        time_frame_num = ff.find_timeframe(v,2)
        image_save_path = os.path.join(save_folder_img,str(time_frame_num)+'.png')
        generate_plane(image_save_path,volume_data,plane_dim,pred_2C,pred_3C,pred_4C,pred_SA,center_list,base_center,mid_center,apical_center)
        print('finish '+str(time_frame_num))
    
    # make plane movie consisting of all time frames
    movie_array = []
    plane_img_list = ff.sort_timeframe(ff.find_all_target_files(['*.png'],save_folder_img),1)
    size = (0,0)
    for i in plane_img_list:
        img = cv2.imread(i)
        h,w,l = img.shape
        size = (w,h)
        movie_array.append(img)
    save_path = os.path.join(save_folder,patient_class+'_'+patient_id+'_plane_movie.avi')
    out_movie = cv2.VideoWriter(save_path,cv2.VideoWriter_fourcc(*'MJPG'),6,size)
    for j in range(len(movie_array)):
        out_movie.write(movie_array[j])
    out_movie.release()
    


    
