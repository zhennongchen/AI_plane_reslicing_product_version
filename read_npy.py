#!/usr/bin/env python
import numpy as np
import segcnn
import os
import nibabel as nb
np.set_printoptions(precision=3,suppress=True)
import math
import dvpy as dv
import dvpy.tf
import segcnn
import function_list as ff

cg = segcnn.Experiment()


data = np.load(os.path.join(cg.patient_dir,'ucsd_lvad/CVC1709271428/vectors-pred/4C-t-ES.npy'),allow_pickle=True)
print(data)

previous_folder = '/Data/McVeighLab/projects/Zhennong/AI/CNN/all-classes-all-phases-1.5'
data2 = np.load(os.path.join(previous_folder,'ucsd_lvad/CVC1709271428/matrix-pred/U_4C_t.npy'),allow_pickle=True)
print(data2)

