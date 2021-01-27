#!/usr/bin/env python

# this scipt tests how the plane vector we predicted under low res can be converted to high res.
# the goal is that the re-sliced mpr by the converted vector should have the same pixel dimension as original CT volume.

import function_list as ff
import os
import numpy as np
import nibabel as nib 
import supplement
import math
cg = supplement.Experiment()
np.set_printoptions(precision=2,suppress=True)

# define your patient
patient = 'CVC1901241836'

# first: check the pixel dimension:
pix_dim_high = ff.get_voxel_size(os.path.join(cg.patient_dir, patient,'img-nii/0.nii.gz'))
pix_dim_low = ff.get_voxel_size(os.path.join(cg.patient_dir, patient,'img-nii-sm/0.nii.gz'))
pix_dim_mpr_high = ff.get_voxel_size(os.path.join(cg.patient_dir, patient,'mpr-nii-zc/2C/0.nii.gz'))
pix_dim_mpr_low = ff.get_voxel_size(os.path.join(cg.patient_dir, patient,'mpr-nii-zc-sm-1.5/2C/0.nii.gz'))
print('pixel dimension of original CT volume: ', pix_dim_high)
print('pixel dimension of MPR re-sliced from original volume: ', pix_dim_mpr_high)
print('pixel dimension of resampled CT volume: ', pix_dim_low)
print('pixel dimension of MPR re-sliced from resampled volume: ', pix_dim_mpr_low)

# load vectors for both low res and native res
m_low = np.load(os.path.join(cg.patient_dir,patient,'vector-manual/manual_2C.npy'),allow_pickle = True)
m_high = np.load(os.path.join(cg.patient_dir,patient,'vector-manual/manual_2C_high.npy'),allow_pickle = True)

t_low,x_low,y_low,scale_low = [m_low[0],m_low[2],m_low[3],m_low[-1]]
t_high,x_high,y_high,scale_high = [m_high[0],m_high[2],m_high[3],m_high[-1]]

# now let's print out the vectors and their vector length
print('unit plane vectors for low res: \n', t_low,x_low,y_low,)
print('the length of plane vectors in low res: \n', scale_low)
print('unit plane vectors in native res: \n',t_high,x_high,y_high)
print('the length of plane vectors in high res: \n', scale_high)

print('\nnow HOW do we convert vector for low res to high res? \nANSWER: use affine transformation! \n')

# load affine
A_low = ff.check_affine(os.path.join(cg.patient_dir,patient,'img-nii-sm/0.nii.gz'))
A_high = ff.check_affine(os.path.join(cg.patient_dir,patient,'img-nii/0.nii.gz'))

# test t vector
new_t = np.asarray([t_low[i] * pix_dim_low[i] / pix_dim_high[i] for i in range(0,t_low.shape[0])])
print('converted translation vector: \n',new_t)

# test x and y
o = [0,0,0]
x1 = o + x_low
new_x = ff.convert_coordinates(A_high,A_low,x1) - ff.convert_coordinates(A_high,A_low,o)
print('converted x vector: \n',ff.normalize(new_x))

y1 = o + y_low
new_y = ff.convert_coordinates(A_high,A_low,y1) - ff.convert_coordinates(A_high,A_low,o)
print('converted y vector: \n',ff.normalize(new_y))

print('\nNow we should get converted vector == vector for native res. Let''s test with home-made function: \n')

# test with our function
vector = ff.get_ground_truth_vectors_product_v(os.path.join(cg.patient_dir,patient,'vector-manual/manual_2C.npy'))
vector = ff.adapt_reslice_vector_for_native_resolution(vector,os.path.join(cg.patient_dir,patient,'img-nii-sm/0.nii.gz'),os.path.join(cg.patient_dir,patient,'img-nii/0.nii.gz'))
print('after applying home-made function that automatically do the conversion, vector is: \n',vector)


# to get the correct vector scale that correspond to original pixel dimension
print('\nNext question: we now have the correct converted unit vector, how do you get the scale that corresponds to orginial pix dim?\n')
print('vector with real value = unit_vector * scale(length)\n')

print('theory: final_scale = length_of_converted_vector / pix_dim(3D)_low_res * pix_dim_high_res\n')

print('scale of converted_vector: ',ff.length(new_x),ff.length(new_y))
print('ground truth scale: ', m_high[-1])
print('calculated by theory, scale becomes: ',ff.length(new_x)/pix_dim_low[0]*pix_dim_mpr_high[0],ff.length(new_y)/pix_dim_low[1]*pix_dim_mpr_high[1])