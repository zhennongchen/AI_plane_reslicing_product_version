#!/usr/bin/env python

# this script generates image with three LAX planes + A SAX stack

import function_list as ff
import os
import math
import numpy as np
import nibabel as nib 
import supplement
from PIL import Image
cg = supplement.Experiment()

save_folder = "/Data/McVeighLabSuper/projects/Zhennong/AI/Zhennong_WMA_Movie_dataset/CVC1901241836/planes_pred_high_res" 

pngs = ff.sort_timeframe(ff.find_all_target_files(['*.png'],save_folder),1)
print(pngs)
save_movie_path = os.path.join(save_folder,'predicted_planes.mp4')
print(save_movie_path)
ff.make_movies(save_movie_path,pngs,10)
print('finish')