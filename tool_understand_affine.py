#!/usr/bin/env python

import function_list as ff
import os
import numpy as np
import nibabel as nib 
import supplement
cg = supplement.Experiment()

patient = 'CVC1908280929'

# load vectors
m_low = np.load(os.path.join(cg.patient_dir,patient,'vector-manual/manual_2C.npy'),allow_pickle = True)
m_high = np.load(os.path.join(cg.patient_dir,patient,'vector-manual/manual_2C_high.npy'),allow_pickle = True)

#
t_low,x_low,y_low = [m_low[0],m_low[2],m_low[3]]
t_high,x_high,y_high = [m_high[0],m_high[2],m_high[3]]

print(t_low,x_low,y_low)
print(t_high,x_high,y_high)

# load affine
A_low = ff.check_affine(os.path.join(cg.patient_dir,patient,'img-nii-sm/0.nii.gz'))
A_high = ff.check_affine(os.path.join(cg.patient_dir,patient,'img-nii/0.nii.gz'))

# load dim
dim_low = ff.get_voxel_size(os.path.join(cg.patient_dir,patient,'img-nii-sm/0.nii.gz'))
dim_high = ff.get_voxel_size(os.path.join(cg.patient_dir,patient,'img-nii/0.nii.gz'))

# test x vector:
o = [0,0,0]
x1 = o + x_low
new_x = ff.convert_coordinates(A_high,A_low,x1) - ff.convert_coordinates(A_high,A_low,o)
print(ff.normalize(new_x))

# test y vector
o = [0,0,0]
y1 = o + y_low
new_y = ff.convert_coordinates(A_high,A_low,y1) - ff.convert_coordinates(A_high,A_low,o)
print(ff.normalize(new_y))

# test t vector
new_t = np.asarray([t_low[i] * dim_low[i] / dim_high[i] for i in range(0,t_low.shape[0])])
print(new_t,new_t.shape)

# 
vector = ff.get_ground_truth_vectors_product_v(os.path.join(cg.patient_dir,patient,'vector-manual/manual_2C.npy'))
vector = ff.adapt_reslice_vector_for_native_resolution(vector,os.path.join(cg.patient_dir,patient,'img-nii-sm/0.nii.gz'),os.path.join(cg.patient_dir,patient,'img-nii/0.nii.gz'))
print(vector)