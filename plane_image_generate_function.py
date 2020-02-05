#!/usr/bin/env python

# this script defines the function to generator the plane image
import function_list as ff
import numpy as np
from PIL import Image

# product
def generate_plane(save_path,volume_data,plane_dim,vector_2C,vector_3C,vector_4C,vector_SA,center_list,base_center,mid_center,apical_center):
    
    # define interpolation
    inter_vol = ff.define_interpolation(volume_data,Fill_value=volume_data.min(),Method='linear')
    image_center = vector_2C['img_center']
    
    # reslice long axis
    twoc = ff.reslice_mpr(np.zeros(plane_dim),image_center + vector_2C['t'],vector_2C['x'],vector_2C['y'],1,1,inter_vol)
    threec = ff.reslice_mpr(np.zeros(plane_dim),image_center + vector_3C['t'],vector_3C['x'],vector_3C['y'],1,1,inter_vol)
    fourc = ff.reslice_mpr(np.zeros(plane_dim),image_center + vector_4C['t'],vector_4C['x'],vector_4C['y'],1,1,inter_vol)
    # reslice short axis
    base = ff.reslice_mpr(np.zeros(plane_dim),base_center,vector_SA['x'],vector_SA['y'],1,1,inter_vol)
    mid = ff.reslice_mpr(np.zeros(plane_dim),mid_center,vector_SA['x'],vector_SA['y'],1,1,inter_vol)
    apical = ff.reslice_mpr(np.zeros(plane_dim),apical_center,vector_SA['x'],vector_SA['y'],1,1,inter_vol)
    
    # set window width + level 
    twoc_n = ff.set_window(twoc[:,:,0],500,900); threec_n = ff.set_window(threec[:,:,0],500,900); fourc_n = ff.set_window(fourc[:,:,0],500,900)
    base_n = ff.set_window(base[:,:,0],500,900); mid_n = ff.set_window(mid[:,:,0],500,900); apical_n = ff.set_window(apical[:,:,0],500,900)
    
    # build an array saved as image    
    ii = np.zeros((160*2,160*3,3))
   
    # first row
    ii[0:160,0:160,0] = np.flip(twoc_n.T,0); ii[0:160,0:160,1] = np.flip(twoc_n.T,0); ii[0:160,0:160,2] = np.flip(twoc_n.T,0)
    ii[0:160,160:320,0] = np.flip(threec_n.T,0); ii[0:160,160:320,1] = np.flip(threec_n.T,0); ii[0:160,160:320,2] = np.flip(threec_n.T,0)
    ii[0:160,320:480,0] = np.flip(fourc_n.T,0); ii[0:160,320:480,1] = np.flip(fourc_n.T,0); ii[0:160,320:480,2] = np.flip(fourc_n.T,0)
    # second row
    ii[160:320,0:160,0] = base_n.T; ii[160:320,0:160,1] = base_n.T; ii[160:320,0:160,2] = base_n.T
    ii[160:320,160:320,0] = mid_n.T; ii[160:320,160:320,1] = mid_n.T; ii[160:320,160:320,2] = mid_n.T
    ii[160:320,320:480,0] = apical_n.T; ii[160:320,320:480,1] = apical_n.T; ii[160:320,320:480,2] = apical_n.T
    

    Image.fromarray((ii*255).astype('uint8')).save(save_path)


