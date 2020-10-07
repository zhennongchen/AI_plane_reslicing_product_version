import os
import numpy as np
import nibabel as nib
from nibabel.affines import apply_affine
import supplement
import supplement.utils as ut
import math
import function_list as ff
cg = supplement.Experiment()

o = [0,0,0]
x1 = [1,0,0]
y1 = [0,1,0]
z1 = [0,0,1]



# main function
def get_vectors(i,j,i_affine,j_affine): #i=img,j=mpr
    x=nib.load(i)
    y=nib.load(j)
    s1=x.shape
    s2=y.shape
    A = np.linalg.inv(i_affine).dot(j_affine)

    # translation of center
    mpr_center=np.array([(s2[0]-1)/2,(s2[1]-1)/2,0])
    img_center=np.array([(s1[0]-1)/2,(s1[1]-1)/2,(s1[-1]-1)/2])
    mpr_center_img = ff.convert_coordinates(i_affine,j_affine,mpr_center)
    translation_c = mpr_center_img - img_center

    # normalize translation into padding coordinate system
    x_pad = ut.in_adapt(i)
    p_size = x_pad.shape
    translation_c_n = np.array([translation_c[0]/p_size[0]*2,translation_c[1]/p_size[1]*2,translation_c[2]/p_size[2]*2])

    # x_direction 
    x_d = ff.convert_coordinates(i_affine,j_affine,x1) - ff.convert_coordinates(i_affine,j_affine,o)
    x_scale = np.linalg.norm(x_d)
    x_n = np.asarray([i/x_scale for i in x_d])
                
    # y_direction
    y_d = ff.convert_coordinates(i_affine,j_affine,y1) - ff.convert_coordinates(i_affine,j_affine,o)
    y_scale = np.linalg.norm(y_d)
    y_n = np.asarray([i/y_scale for i in y_d])


    # scale
    x_s = ff.length(x_d)/1
    y_s = ff.length(y_d)/1 
    scale = np.array([x_s,y_s])

    # vectors:
    vectors=np.array([translation_c, translation_c_n, x_n, y_n, img_center])
    return vectors


def get_voxel_size(i):
    ii = nib.load(i)
    h = ii.header
    return h.get_zooms()



chamber_list = ['2C','3C','4C','BASAL']
chamber_choice = [0,1,2,3]
patient_list = ff.find_all_target_files(['*'],cg.patient_dir)
img_fld = 'img-nii'
mpr_fld = 'mpr-nii-zc'


for p in patient_list:
    patient_id = os.path.basename(p)
    patient_class = os.path.basename(os.path.dirname(p))
    print(patient_class,patient_id)

    save_folder = os.path.join(p,'vector-manual')
    ff.make_folder([save_folder])


    for c in chamber_choice:
        chamber = chamber_list[c]

        #image 1.5mm
        i = os.path.join(p,img_fld,'0.nii.gz')
        i_affine = ff.check_affine(i)
    
        #mpr 1.5mm
        j = os.path.join(p,mpr_fld,chamber,'0.nii.gz')
        j_affine = nib.load(j).affine
        
        matrix=get_vectors(i,j,i_affine,j_affine)

        np.save(os.path.join(save_folder,'manual_'+chamber+'_high'),matrix)
        
        