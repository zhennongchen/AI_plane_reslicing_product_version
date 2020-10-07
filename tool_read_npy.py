#!/usr/bin/env python
import numpy as np
import os
import nibabel as nb
import math
import supplement
import function_list as ff
np.set_printoptions(precision=3,suppress=True)

cg = supplement.Experiment()


data = np.load(os.path.join(cg.patient_dir,'CVC1901241836/vector-manual/manual_4C.npy'),allow_pickle=True)
print(ff.normalize(data[2]))

data = np.load(os.path.join(cg.patient_dir,'CVC1901241836/vector-manual/manual_4C_high.npy'),allow_pickle=True)
print(ff.normalize(data[2]))

volume_file = os.path.join(cg.patient_dir,'CVC1901241836','img-nii','0.nii.gz')
native_pix_dim = ff.get_voxel_size(volume_file)
print(native_pix_dim)

