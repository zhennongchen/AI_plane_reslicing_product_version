#!/usr/bin/env python

# this script generates plane product based on the batch selection we made


import function_list as ff
import os
import math
import numpy as np
import nibabel as nib 
import supplement
from PIL import Image
import pandas as pd
import shutil
cg = supplement.Experiment()

WL = 500
WW = 800
native_res = 1
if native_res == 1:
    plane_image_size = [480,480,1]
    color_box_size = [30,60]
else:
    plane_image_size = [160,160,1]
    color_box_size = [10,20]

scale = [1,1,0.67]
zoom_factor = 1 # in case the background in the plane is too large 


# function to make the image
def plane_image(save_path,volume_data,plane_image_size,WL,WW,zoom_factor,image_center, vector_2C,vector_3C,vector_4C,vector_SA, A_2C, A_3C, A_4C ,center_list):
    
    # define interpolation matrix
    inter = ff.define_interpolation(volume_data,Fill_value=volume_data.min(),Method='linear')
    
    # reslice long axis
    twoc = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_2C['t'],vector_2C['x'],vector_2C['y'],vector_2C['s'][0]/zoom_factor,vector_2C['s'][1]/zoom_factor,inter)
    threec = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_3C['t'],vector_3C['x'],vector_3C['y'],vector_3C['s'][0]/zoom_factor,vector_3C['s'][1]/zoom_factor,inter)
    fourc = ff.reslice_mpr(np.zeros(plane_image_size),image_center + vector_4C['t'],vector_4C['x'],vector_4C['y'],vector_4C['s'][0]/zoom_factor,vector_4C['s'][1]/zoom_factor,inter)

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

# Get patient_list
patient_list = ff.get_patient_list_from_csv(os.path.join('/Data/McVeighLabSuper/projects/Zhennong','Cases_for_Cardiowise_list_batch_selection.csv'))
csv_file = pd.read_csv(os.path.join('/Data/McVeighLabSuper/projects/Zhennong','Cases_for_Cardiowise_list_batch_selection.csv'))
print(patient_list)

for i in range(0,len(patient_list)):
    patient_class = patient_list[i][0]
    patient_id = patient_list[i][1]
    if patient_id != 'CVC2002271407':
        continue
   
    print(patient_class,patient_id)

    case = csv_file.iloc[i]
    assert case['Patient_ID'] == patient_id

    [seg_batch,twoc_batch,threec_batch,fourc_batch,sax_batch] = [case['seg_batch'],
    case['2C'],case['3C'],case['4C'],case['SAX']]
    
    # check whether this patient is exclude
    if seg_batch == 'x' and threec_batch == 'x':
        print('this case is exclude!!!')
        continue
    else:
        ff.make_folder([os.path.join(cg.final_dir,patient_class,patient_id)])
    
    plane_batch_selection = [twoc_batch,threec_batch,fourc_batch,sax_batch]
    
    if os.path.isfile(os.path.join(cg.final_dir,patient_class,patient_id,patient_id+'_planes.mp4')) == 10:
        print('already done')
    else:
        #if len(list(set(plane_batch_selection))) == 1:
        if 1 == 2:
            # copy image if the selection of batch is consistent among views
            print('this one has same batch choices, batch '+ twoc_batch + ' ,directly copy')
            plane_folder = os.path.join(cg.save_dir,patient_class,patient_id,'planes_pred','batch_'+twoc_batch)
            copy_plane_folder = os.path.join(cg.final_dir,patient_class,patient_id,'planes_pred')
            if os.path.isdir(copy_plane_folder) == 0:
                shutil.copytree(plane_folder,copy_plane_folder)

        else:
            # re-do 
            print('this one has difference batch choices, ', plane_batch_selection)

            patient = os.path.join(cg.save_dir,patient_class,patient_id)

            save_folder = os.path.join(cg.final_dir,patient_class,patient_id)
            ff.make_folder([save_folder])


            seg = nib.load(os.path.join(patient,'seg-pred/batch_'+str(seg_batch),'pred_s_0.nii.gz')); seg_data = seg.get_fdata()
            volume_dim = nib.load(os.path.join(cg.local_dir,patient_class,patient_id,'img-nii-1.5/0.nii.gz')).shape
            image_center = np.array([(volume_dim[0]-1)/2,(volume_dim[1]-1)/2,(volume_dim[-1]-1)/2]) 

            # load vectors
            vector_2C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/batch_'+str(twoc_batch),'pred_2C_t.npy'),os.path.join(patient,'vector-pred/batch_'+str(twoc_batch),'pred_2C_r.npy'),scale, image_center)
            vector_3C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/batch_'+str(threec_batch),'pred_3C_t.npy'),os.path.join(patient,'vector-pred/batch_'+str(threec_batch),'pred_3C_r.npy'),scale, image_center)
            vector_4C = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/batch_'+str(fourc_batch),'pred_4C_t.npy'),os.path.join(patient,'vector-pred/batch_'+str(fourc_batch),'pred_4C_r.npy'),scale, image_center)
            vector_SA = ff.get_predicted_vectors(os.path.join(patient,'vector-pred/batch_'+str(sax_batch),'pred_BASAL_t.npy'),os.path.join(patient,'vector-pred/batch_'+str(sax_batch),'pred_BASAL_r.npy'),scale, image_center)

            print('x,y are ',ff.normalize(vector_SA['x']),ff.normalize(vector_SA['y']))
            print('normal vector is ',ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])))

            # define plane num for SAX stack:
            normal_vector = ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])) 
            a,b = ff.find_num_of_slices_in_SAX(np.zeros([160,160,1]),image_center,vector_SA['t'],vector_SA['x'],vector_SA['y'],seg_data,0,2.59)
            a = 2
            b = 23
            print(a,b)
            #t_file = open(os.path.join(patient,"slice_num_info.txt"),"w+")
            #t_file.write("num of slices before basal = %d\nnum of slices after basal = %d" % (a, b))
            #t_file.close()

            # transfer vector into native res:
            if native_res == 1:
                V = []
                for v in [vector_2C,vector_3C,vector_4C,vector_SA]:
                    v = ff.adapt_reslice_vector_for_native_resolution(v,os.path.join(cg.image_data_dir,patient_class,patient_id,'img-nii-1.5/0.nii.gz'),os.path.join(cg.image_data_dir,patient_class,patient_id,'img-nii/0.nii.gz'))
                    v['s'] = ff.set_scale_for_unequal_x_and_y(v)
                    V.append(v)
                [vector_2C,vector_3C,vector_4C,vector_SA] = [V[0],V[1],V[2],V[3]] 

                volume_dim = nib.load(os.path.join(cg.image_data_dir,patient_class,patient_id,'img-nii/0.nii.gz')).shape
                image_center = np.array([(volume_dim[0]-1)/2,(volume_dim[1]-1)/2,(volume_dim[-1]-1)/2])

            print('new x,y are ',ff.normalize(vector_SA['x']),ff.normalize(vector_SA['y']))
            print('new normal vector is ',ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])))

            # get affine matrix
            volume_affine = ff.check_affine(os.path.join(cg.image_data_dir,patient_class,patient_id,'img-nii/0.nii.gz'))
            A_2C = ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,vector_2C)
            A_3C = ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,vector_3C)
            A_4C = ff.get_affine_from_vectors(np.zeros(plane_image_size),volume_affine,vector_4C)
            
            # get a center list of SAX stack
            if native_res == 1:
                pix_dim = ff.get_voxel_size(os.path.join(cg.image_data_dir,patient_class,patient_id,'img-nii/0.nii.gz'))
                pix_size = ff.length(pix_dim)
                normal_vector = ff.normalize(np.cross(vector_SA['x'],vector_SA['y'])) 
                center_list = ff.find_center_list_whole_stack(image_center + vector_SA['t'],normal_vector,a,b,8,pix_size)
            else:
                center_list = ff.find_center_list_whole_stack(image_center + vector_SA['t'],normal_vector,a,b,8,2.59)

            print('new_centerlist: ',center_list)

            # get the index of each planes of 9-plane SAX stack (9 planes should start from MV and end with apex, convering the whole LV)
            index_list,center_list9,gap = ff.resample_SAX_stack_into_particular_num_of_planes(range(2,center_list.shape[0]),9,center_list)
            if gap < 1:
                ValueError('no LV segmentation')
            print('new_centerlist9: ',center_list9)

            # reslice mpr for every time frame
            if native_res == 1:
                volume_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii/*.nii.gz'],os.path.join(cg.image_data_dir,patient_class,patient_id)),2)
            else:
                volume_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii-1.5/*.nii.gz'],os.path.join(cg.image_data_dir,patient_class,patient_id)),2)


            for v in volume_list:
                volume = nib.load(v)
                volume_data = volume.get_fdata()
                if len(volume_data.shape) > 3:
                    print('this data has more than 3 dimen')
                    volume_data = volume_data[:,:,:,1]
                    print(volume_data.shape)
                    assert len(volume_data.shape) == 3
                elif len(volume_data.shape) < 3:
                    print('this data has less than 3 dimen')
                    continue
                else:
                    aa = 1

                time = ff.find_timeframe(v,2)
                save_path = os.path.join(save_folder,'pngs',str(time) +'.png')
                ff.make_folder([os.path.dirname(save_path)])
                plane_image(save_path,volume_data,plane_image_size,WL,WW,zoom_factor,image_center, vector_2C,vector_3C,vector_4C,vector_SA,A_2C, A_3C, A_4C, center_list9)
                print('finish time '+str(time))

            # make the movie
            pngs = ff.sort_timeframe(ff.find_all_target_files(['*.png'],os.path.join(save_folder,'pngs')),1)
            save_movie_path = os.path.join(save_folder,patient_id+'_planes.mp4')
            if len(pngs) >= 10:
                framerate = len(pngs)
            else:
                framerate = 10
            ff.make_movies(save_movie_path,pngs,10)


    # # copy the segmentation 
    # seg_folder = os.path.join(cg.save_dir,patient_class,patient_id,'seg-pred','batch_'+str(seg_batch))
    # if os.path.isdir(seg_folder) == 0:
    #     ValueError('no predicted seg!')
    # if os.path.isdir(os.path.join(cg.final_dir,patient_class,patient_id,'seg-pred')) == 0:
    #     shutil.copytree(seg_folder,os.path.join(cg.final_dir,patient_class,patient_id,'seg-pred'))

    # # copy the txt file
    # txt_files = ff.find_all_target_files(['*.txt'],os.path.join(cg.save_dir,patient_class,patient_id))
    # for t in txt_files:
    #     if os.path.isfile(os.path.join(cg.final_dir,patient_class,patient_id,os.path.basename(t))) == 0:
    #         shutil.copyfile(t,os.path.join(cg.final_dir,patient_class,patient_id,os.path.basename(t)))

  
    
