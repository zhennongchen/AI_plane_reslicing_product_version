#!/usr/bin/env python

# this script reslices the image volume (either in low-res or native-res) with vectors

import function_list as ff
import os
import numpy as np
import nibabel as nib 
import supplement
from PIL import Image
cg = supplement.Experiment()

scale = [1,1,0.67]

# define patient:
patient = 'CVC1908280929'

# define low res or high res
native_res = 1

# define plane dimension:
if native_res == 1:
    plane_dim = [480,480,1]
else:
    plane_dim = [160,160,1]

# define image volume
if native_res == 1:
    volume_file = os.path.join(cg.patient_dir,patient,'img-nii','0.nii.gz')
else:
    volume_file = os.path.join(cg.patient_dir,patient,'img-nii-sm','0.nii.gz')
volume = nib.load(volume_file)
volume_data = volume.get_fdata()

# define image_center:
img_center=np.array([(volume_data.shape[0]-1)/2,(volume_data.shape[1]-1)/2,(volume_data.shape[-1]-1)/2])

# define vectors:
#vector = ff.get_predicted_vectors(os.path.join(cg.patient_dir,patient,'vector-pred/pred_4C_t.npy'),os.path.join(cg.patient_dir,patient,'vector-pred/pred_4C_r.npy'),scale, img_center)
vector = ff.get_ground_truth_vectors_product_v(os.path.join(cg.patient_dir,patient,'vector-manual/manual_2C_high.npy'))
#if native_res == 1:
#    vector = ff.adapt_reslice_vector_for_native_resolution(vector,os.path.join(cg.patient_dir,patient,'img-nii-sm','0.nii.gz'),os.path.join(cg.patient_dir,patient,'img-nii','0.nii.gz'))

# re-slice
interpolation = ff.define_interpolation(volume_data,Fill_value = volume_data.min(),Method='linear')
plane = ff.reslice_mpr(np.zeros(plane_dim),img_center + vector['t'], ff.normalize(vector['x']), ff.normalize(vector['y']),1,1,interpolation)

# set WL,WW and orient
WL = 500
WW = 900
plane_n = ff.set_window(plane,WL,WW)
plane_n = np.flip(plane_n.T,0)
print(plane_n.shape)

# make image
I = np.zeros((plane_dim[0],plane_dim[1],3))
I[0:plane_dim[0],0:plane_dim[1],0] = plane_n
I[0:plane_dim[0],0:plane_dim[1],1] = plane_n
I[0:plane_dim[0],0:plane_dim[1],2] = plane_n

# save image 
Image.fromarray((I * 255).astype('uint8')).save(os.path.join(cg.patient_dir,'plane_high.png'))




