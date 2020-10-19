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
print(cg.patient_dir)

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
vector = ff.get_predicted_vectors(os.path.join(cg.patient_dir,patient,'vector-pred/pred_2C_t.npy'),os.path.join(cg.patient_dir,patient,'vector-pred/pred_2C_r.npy'),scale, img_center)
#vector = ff.get_ground_truth_vectors_product_v(os.path.join(cg.patient_dir,patient,'vector-manual/manual_2C_high.npy'))
if native_res == 1:
    vector = ff.adapt_reslice_vector_for_native_resolution(vector,os.path.join(cg.patient_dir,patient,'img-nii-sm','0.nii.gz'),os.path.join(cg.patient_dir,patient,'img-nii','0.nii.gz'))

# re-slice
interpolation = ff.define_interpolation(volume_data,Fill_value = volume_data.min(),Method='linear')
plane = ff.reslice_mpr(np.zeros(plane_dim),img_center + vector['t'], ff.normalize(vector['x']), ff.normalize(vector['y']),0.557,0.783,interpolation)

# get the affine matrix
mpr_file = nib.load(os.path.join(cg.patient_dir,patient,'mpr-nii-zc/2C/0.nii.gz'))
nii = nib.Nifti1Image(plane, mpr_file.affine)
nib.save(nii, os.path.join(cg.patient_dir,'plane_high.nii.gz'))




