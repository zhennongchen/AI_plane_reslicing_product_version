#!/usr/bin/env python

# this script generates image with three LAX planes + A SAX stack in low resolution
# the generated planes can be used to decide which model to use
# for unknown reason, it can not be run in docker cuda_100_all_collection but can only run in Docker_AI_plane

import function_list as ff
import os
import math
import numpy as np
import nibabel as nib 
import supplement
from PIL import Image
cg = supplement.Experiment()

WL = 500
WW = 800  #####change the width!!!!!!!!!!!
native_res = 0
plane_image_size = [160,160,1]
color_box_size = [10,20]

scale = [1,1,0.67]
zoom_factor = 1 # in case the background in the plane is too large 


# function to make the image
def plane_image(save_path,volume_data,plane_image_size,WL,WW,zoom_factor,image_center, vector_2C,vector_3C,vector_4C,vector_SA, A_2C, A_3C, A_4C ,center_list):
    
    # define interpolation matrix
    inter = ff.define_interpolation(volume_data,Fill_value=volume_data.min(),Method='linear')
    
    zoom_factor = 1.1
    # reslice long axis
    twoc = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_2C['t'],vector_2C['x'],vector_2C['y'],vector_2C['s'][0]/zoom_factor,vector_2C['s'][1]/zoom_factor,inter)
    threec = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_3C['t'],vector_3C['x'],vector_3C['y'],vector_3C['s'][0]/zoom_factor,vector_3C['s'][1]/zoom_factor,inter)
    fourc = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_4C['t'],vector_4C['x'],vector_4C['y'],vector_4C['s'][0]/zoom_factor,vector_4C['s'][1]/zoom_factor,inter)

    zoom_factor = 1.25
    # reslice short axis
    sax_collection = []
    for i in range(0,9):
        sax_collection.append(ff.reslice_mpr(np.zeros(plane_image_size),center_list[i],vector_SA['x'],vector_SA['y'],vector_SA['s'][0]/zoom_factor,vector_SA['s'][1]/zoom_factor,inter))
    assert len(sax_collection) == 9

    # draw intersection lines: LAX lines on SAX
    sax_w_2c = []; sax_w_3c = []; sax_w_4c = []
    for ii in range(0,9):
        line2c,_,_ = ff.draw_plane_intersection(sax_collection[ii],vector_2C['x'],vector_2C['y'],A_2C,ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[ii],image_center,vector_SA)),volume_affine)
        line3c,_,_ = ff.draw_plane_intersection(sax_collection[ii],vector_3C['x'],vector_3C['y'],A_3C,ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[ii],image_center,vector_SA)),volume_affine)
        line4c,_,_ = ff.draw_plane_intersection(sax_collection[ii],vector_4C['x'],vector_4C['y'],A_4C,ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[ii],image_center,vector_SA)),volume_affine)
        sax_w_2c.append(line2c)
        sax_w_3c.append(line3c)
        sax_w_4c.append(line4c)
    
    
    
    # draw intersection lines: SAX lines on LAX
    twoc_line = np.copy(twoc); threec_line = np.copy(threec); fourc_line = np.copy(fourc)
    twoc_line,_,_ = ff.draw_plane_intersection(twoc_line,vector_SA['x'],vector_SA['y'],ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[2],image_center,vector_SA)),A_2C,volume_affine)
    twoc_line,_,_ = ff.draw_plane_intersection(twoc_line,vector_SA['x'],vector_SA['y'],ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[4],image_center,vector_SA)),A_2C,volume_affine)
    twoc_line,_,_ = ff.draw_plane_intersection(twoc_line,vector_SA['x'],vector_SA['y'],ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[6],image_center,vector_SA)),A_2C,volume_affine)
    threec_line,_,_ = ff.draw_plane_intersection(threec_line,vector_SA['x'],vector_SA['y'],ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[2],image_center,vector_SA)),A_3C,volume_affine)
    threec_line,_,_ = ff.draw_plane_intersection(threec_line,vector_SA['x'],vector_SA['y'],ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[4],image_center,vector_SA)),A_3C,volume_affine)
    threec_line,_,_ = ff.draw_plane_intersection(threec_line,vector_SA['x'],vector_SA['y'],ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[6],image_center,vector_SA)),A_3C,volume_affine)
    fourc_line,_,_ = ff.draw_plane_intersection(fourc_line,vector_SA['x'],vector_SA['y'],ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[2],image_center,vector_SA)),A_4C,volume_affine)
    fourc_line,_,_ = ff.draw_plane_intersection(fourc_line,vector_SA['x'],vector_SA['y'],ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[4],image_center,vector_SA)),A_4C,volume_affine)
    fourc_line,_,_ = ff.draw_plane_intersection(fourc_line,vector_SA['x'],vector_SA['y'],ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,ff.make_matrix_for_any_plane_in_SAX_stack(center_list[6],image_center,vector_SA)),A_4C,volume_affine)

    # normalize by WL and WW and then orient
    twoc_n = ff.set_window(twoc,WL,WW); twoc_n = np.flip(twoc_n.T,0)
    twoc_line_n = ff.set_window(twoc_line,WL,WW); twoc_line_n = np.flip(twoc_line_n.T,0)
    threec_n = ff.set_window(threec,WL,WW); threec_n = np.flip(threec_n.T,0)
    threec_line_n = ff.set_window(threec_line,WL,WW); threec_line_n = np.flip(threec_line_n.T,0)
    fourc_n = ff.set_window(fourc,WL,WW); fourc_n = np.flip(fourc_n.T,0)
    fourc_line_n = ff.set_window(fourc_line,WL,WW); fourc_line_n = np.flip(fourc_line_n.T,0)

    sax_w_2c_n = []; sax_w_3c_n = []; sax_w_4c_n = []
    for iii in range(0,9):
        line2c_n = ff.set_window(sax_w_2c[iii],WL,WW); line2c_n = line2c_n.T
        line3c_n = ff.set_window(sax_w_3c[iii],WL,WW); line3c_n = line3c_n.T
        line4c_n = ff.set_window(sax_w_4c[iii],WL,WW); line4c_n = line4c_n.T
        sax_w_2c_n.append(line2c_n)
        sax_w_3c_n.append(line3c_n)
        sax_w_4c_n.append(line4c_n)
    assert len(sax_w_4c_n) == 9
    

    # make image
    [h,w,d] = plane_image_size
    I = np.zeros((h*3,w*4,3))
    I[0:h,0:w,0] = ff.color_box(twoc_n,color_box_size[0],color_box_size[1]); I[0:h,0:w,1] = twoc_line_n; I[0:h,0:w,2] = twoc_n
    I[h:h*2,0:w,0] = threec_n; I[h:h*2,0:w,1] = ff.color_box(threec_line_n,color_box_size[0],color_box_size[1]); I[h:h*2,0:w,2] = threec_n
    I[h*2:h*3,0:w,0] = fourc_n; I[h*2:h*3,0:w,1] = fourc_line_n; I[h*2:h*3,0:w,2] = ff.color_box(fourc_n,color_box_size[0],color_box_size[1])
    I[0:h,w:w*2,0] = sax_w_2c_n[0]; I[0:h,w:w*2,1] = sax_w_3c_n[0]; I[0:h,w:w*2,2] = sax_w_4c_n[0]
    I[0:h,w*2:w*3,0] = sax_w_2c_n[1]; I[0:h,w*2:w*3,1] = sax_w_3c_n[1]; I[0:h,w*2:w*3,2] = sax_w_4c_n[1]
    I[0:h,w*3:w*4,0] = sax_w_2c_n[2]; I[0:h,w*3:w*4,1] = sax_w_3c_n[2]; I[0:h,w*3:w*4,2] = sax_w_4c_n[2]
    I[h:h*2,w:w*2,0] = sax_w_2c_n[3]; I[h:h*2,w:w*2,1] = sax_w_3c_n[3]; I[h:h*2,w:w*2,2] = sax_w_4c_n[3]
    I[h:h*2,w*2:w*3,0] = sax_w_2c_n[4]; I[h:h*2,w*2:w*3,1] = sax_w_3c_n[4]; I[h:h*2,w*2:w*3,2] = sax_w_4c_n[4]
    I[h:h*2,w*3:w*4,0] = sax_w_2c_n[5]; I[h:h*2,w*3:w*4,1] = sax_w_3c_n[5]; I[h:h*2,w*3:w*4,2] = sax_w_4c_n[5]
    I[h*2:h*3,w:w*2,0] = sax_w_2c_n[6]; I[h*2:h*3,w:w*2,1] = sax_w_3c_n[6]; I[h*2:h*3,w:w*2,2] = sax_w_4c_n[6]
    I[h*2:h*3,w*2:w*3,0] = sax_w_2c_n[7]; I[h*2:h*3,w*2:w*3,1] = sax_w_3c_n[7]; I[h*2:h*3,w*2:w*3,2] = sax_w_4c_n[7]
    I[h*2:h*3,w*3:w*4,0] = sax_w_2c_n[8]; I[h*2:h*3,w*3:w*4,1] = sax_w_3c_n[8]; I[h*2:h*3,w*3:w*4,2] = sax_w_4c_n[8]

    # save
    Image.fromarray((I * 255).astype('uint8')).save(save_path)


# main function for image
patient_list = ff.find_all_target_files(['172/172pre'],cg.save_dir)
# define which segmentation prediction batch will be used
batch_seg = 3

for batch in range(0,5):
    print('Batch is ', batch)
    for patient in patient_list:
        patient_id = os.path.basename(patient)
        patient_class = os.path.basename(os.path.dirname(patient))
        print(patient_class,patient_id)

        save_folder = os.path.join(patient,'planes_pred_low_res/batch_'+str(batch))
        ff.make_folder([os.path.dirname(save_folder),save_folder])

        # check whether already done
        #if os.path.isfile(os.path.join(save_folder,patient_id+'_predicted_planes.mp4')) == 1:
        # if os.path.isfile(os.path.join(save_folder,'0.png')) == 1:
        #     print('already done for this patient')
        #     continue

        seg = nib.load(os.path.join(patient,'seg-pred/batch_'+str(batch_seg),'pred_s_0.nii.gz')); seg_data = seg.get_fdata()
        volume_dim = nib.load(os.path.join(cg.local_dir,patient_class,patient_id,'img-nii-1.5/0.nii.gz')).shape
        image_center = np.array([(volume_dim[0]-1)/2,(volume_dim[1]-1)/2,(volume_dim[-1]-1)/2]) 

        # load vectors
        vector_2C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/batch_'+str(batch),'pred_2C_t.npy'),os.path.join(patient,'vector-pred/batch_'+str(batch),'pred_2C_r.npy'),scale, image_center)
        vector_3C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/batch_'+str(batch),'pred_3C_t.npy'),os.path.join(patient,'vector-pred/batch_'+str(batch),'pred_3C_r.npy'),scale, image_center)
        vector_4C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/batch_'+str(batch),'pred_4C_t.npy'),os.path.join(patient,'vector-pred/batch_'+str(batch),'pred_4C_r.npy'),scale, image_center)
        vector_SA = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/batch_'+str(batch),'pred_BASAL_t.npy'),os.path.join(patient,'vector-pred/batch_'+str(batch),'pred_BASAL_r.npy'),scale, image_center)

        # define plane num for SAX stack:
        normal_vector = ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])) 
        a,b = ff.find_num_of_slices_in_SAX(np.zeros([160,160,1]),image_center,vector_SA['t'],vector_SA['x'],vector_SA['y'],seg_data,0,2.59)
        #a = 3; b = 24
        print('a is ',a,'b is ',b)
        t_file = open(os.path.join(cg.save_dir,patient_class,patient_id,"slice_num_info_low_res_batch_"+str(batch)+".txt"),"w+")
        t_file.write("num of slices before basal = %d\nnum of slices after basal = %d" % (a, b))
        t_file.close()


        # get affine matrix
        volume_affine = ff.check_affine(os.path.join(cg.image_data_dir,patient_class,patient_id,'img-nii-1.5/0.nii.gz'))
        A_2C = ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,vector_2C)
        A_3C = ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,vector_3C)
        A_4C = ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,vector_4C)


        # get a center list of SAX stack
        pix_dim = ff.get_voxel_size(os.path.join(cg.image_data_dir,patient_class,patient_id,'img-nii-1.5/0.nii.gz'))
        pix_size = ff.length(pix_dim)
        center_list = ff.find_center_list_whole_stack(image_center + vector_SA['t'],normal_vector,a,b,8,2.59)

        # get the index of each planes of 9-plane SAX stack (9 planes should start from MV and end with apex, convering the whole LV)
        index_list,center_list9,gap = ff.resample_SAX_stack_into_particular_num_of_planes(range(2,center_list.shape[0]),9,center_list)
        if gap < 1:
            print('no LV segmentation')
            continue


        # reslice mpr for every time frame
        volume_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii-1.5/0.nii.gz'],os.path.join(cg.image_data_dir,patient_class,patient_id)),2)


        for v in volume_list:
            volume = nib.load(v)
            volume_data = volume.get_fdata()
            if len(volume_data.shape) > 3:
                print('this data has more than 3 dimen')
                if os.path.isfile(os.path.join(patient,"dimension_problem.txt")) == 0:
                    dimension_file = open(os.path.join(patient,"dimension_problem.txt"),"w+")
                    dimension_file.write("dimension is %d %d %d %d" % (volume_data.shape[0], volume_data.shape[1],volume_data.shape[2],volume_data.shape[3]))
                    dimension_file.close()
                volume_data = volume_data[:,:,:,1]
                print(volume_data.shape)
                assert len(volume_data.shape) == 3
            elif len(volume_data.shape) < 3:
                print('this data has less than 3 dimen')
                if os.path.isfile(os.path.join(patient,"dimension_problem.txt")) == 0:
                    dimension_file = open(os.path.join(patient,"dimension_problem.txt"),"w+")
                    dimension_file.write("dimension is %d %d" % (volume_data.shape[0], volume_data.shape[1]))
                    dimension_file.close()
                continue
            else:
                aa = 1

            time = ff.find_timeframe(v,2)
            save_path = os.path.join(save_folder,str(time) +'.png')
            plane_image(save_path,volume_data,plane_image_size,WL,WW,zoom_factor,image_center, vector_2C,vector_3C,vector_4C,vector_SA,A_2C, A_3C, A_4C,center_list9)
            print('finish time '+str(time))

        # make movie
        # pngs = ff.sort_timeframe(ff.find_all_target_files(['*.png'],os.path.join(save_folder,'pngs')),1)
        # save_movie_path = os.path.join(save_folder,patient_id+'_planes.mp4')
        # print(len(pngs))
        # if len(pngs) == 16:
        #     fps = 15 # set 16 will cause bug
        # elif len(pngs) > 20:
        #     fps = len(pngs)//2
        # else:
        #     fps = len(pngs)
        # ff.make_movies(save_movie_path,pngs,fps)

    print('finish batch ',batch)





    
    