#!/usr/bin/env python

# System
import argparse
import os

# Third Party
import numpy as np
import math
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras import backend as K
from keras.models import Model
from keras.layers import Input, \
                         Conv1D, Conv2D, Conv3D, \
                         MaxPooling1D, MaxPooling2D, MaxPooling3D, \
                         UpSampling1D, UpSampling2D, UpSampling3D, \
                         Reshape, Flatten, Dense
from keras.initializers import Orthogonal
from keras.regularizers import l2
import nibabel as nb

import supplement
from supplement.generator import ImageDataGenerator
import supplement.utils as ut
import dvpy as dv
import dvpy.tf
import function_list as ff
import model_list as mm
import pandas as pd

cg = supplement.Experiment()


# Define pre-trained model list
MODELS = mm.get_model_list()

# define patient CT image list
# by excel sheet
# excel_file = os.path.join('/Data/ContijochLab/projects/ct_gls','Andy_Khan_WMA_scores.xlsx')
# excel_data = pd.read_excel(excel_file)
# patient_list= []
# data_path1 = cg.image_data_dir
# data_path2 = os.path.join(cg.main_data_dir,'2020_after_Junes/nii-images')
# for i in range(0,excel_data.shape[0]):
#   case = excel_data.iloc[i]
#   if os.path.isdir(os.path.join(data_path1,case['Patient_Class'],case['Patient_ID'])) == 1:
#     belong_path = os.path.dirname(os.path.dirname(data_path1))
#   elif os.path.isdir(os.path.join(data_path2,case['Patient_Class'],case['Patient_ID'])) == 1:
#     belong_path = os.path.dirname(data_path2)
#   else:
#     ValueError('wrong!')
#   patient_list.append([case['Patient_Class'],case['Patient_ID'],belong_path])
# print(patient_list)

# by file search
patient_list = ff.find_all_target_files(['*/*'],cg.local_dir)
print(patient_list.shape) 
print('finish finding all patients')

# build the model
shape = cg.dim + (1,)
model_inputs = [Input(shape)]
model_outputs=[]
ds_layer, _, unet_output = dvpy.tf.get_unet(cg.dim,cg.num_classes,cg.conv_depth,layer_name='unet',
                                      dimension =len(cg.dim),unet_depth = cg.unet_depth,)(model_inputs[0])
ds_flat = Flatten()(ds_layer)
Loc= Dense(384,kernel_initializer=Orthogonal(gain=1.0),kernel_regularizer = l2(1e-4),
                                      activation='relu',name='Loc')(ds_flat)
translation = Dense(3,kernel_initializer=Orthogonal(gain=1e-1),kernel_regularizer = l2(1e-4),
                                      name ='t')(Loc)
x_direction = Dense(3,kernel_initializer=Orthogonal(gain=1e-1),kernel_regularizer = l2(1e-4),
                                      name ='x')(Loc)
y_direction = Dense(3,kernel_initializer=Orthogonal(gain=1e-1),kernel_regularizer = l2(1e-4),
                                      name ='y')(Loc)
model_outputs += [unet_output]
model_outputs += [translation]
model_outputs += [x_direction]
model_outputs += [y_direction]
model = Model(inputs = model_inputs,outputs = model_outputs)
print('finish building the model')



for batch in [0,1,2,3,4]:
  MODEL = []
  for ii in range(0,len(MODELS)):
    MODEL.append(MODELS[ii][batch])
  print(MODEL)

  # prediction task list
  task_list = ['s','2C_t','2C_r','3C_t','3C_r','4C_t','4C_r','BASAL_t','BASAL_r'] 
  task_num_list = [0,1,2,3,4,5,6,7,8]

  # define the generator
  valgen = dv.tf.ImageDataGenerator(3,input_layer_names=['input_1'],output_layer_names=['unet','t','x','y'],)

  # predict per patient
  for task_num in task_num_list:
    print('current task is: ', task_list[task_num])
    if task_list[task_num] == 's':
      view = '2C'
    else:
      view = task_list[task_num].split('_')[0]
      vector = task_list[task_num].split('_')[1]
    print(view)
    ##### load saved weight
    model_file_name = MODEL[task_num]
    model_files = ff.find_all_target_files([model_file_name],cg.model_dir)
    assert len(model_files) == 1
    model.load_weights(model_files[0],by_name = True)
    print('=======\n=======\n')
    print('finish loading saved weights: ',model_files[0])

    # predict
    for p in patient_list:
      patient_class = os.path.basename(os.path.dirname(p))
      patient_id = os.path.basename(p)
      print(patient_class, patient_id)
      # patient_class = p[0]
      # patient_id = p[1]
      # belong_path = p[2]
      print(patient_class,patient_id,p)
      p = os.path.join(cg.local_dir,patient_class,patient_id)

      if os.path.isdir(os.path.join(cg.local_dir,patient_class,patient_id,'img-nii-1.5')) == 0:
        print('no data')
        continue
      
      # for  already done:
      if task_list[task_num] == 's':
        if os.path.isfile(os.path.join(cg.save_dir,patient_class,patient_id,'seg-pred/batch_'+str(batch),'pred_s_0.nii.gz')) == 1:
          print('already done segmentation')
          continue
      else:
        if os.path.isfile(os.path.join(cg.save_dir,patient_class,patient_id,'vector-pred/batch_' + str(batch),'pred_'+task_list[task_num]+'.npy')) == 1:
          print('already done ', task_list[task_num])
          continue

      # find the input images for all time frames:
      if task_list[task_num] == 's':
        img_list = ff.sort_timeframe(ff.find_all_target_files(['img-nii-1.5/*.nii.gz'],p),2)
      else:
        img_list = ff.find_all_target_files(['img-nii-1.5/0.nii.gz'],p)

      for img in img_list:
        time_frame = ff.find_timeframe(img,2)
        print(time_frame)

        # build the predict_generator
        u_pred,t_pred,x_pred,y_pred= model.predict_generator(valgen.predict_flow(np.asarray([img]),
            batch_size = cg.batch_size,
            view = view,
            relabel_LVOT = cg.relabel_LVOT,
            input_adapter = ut.in_adapt,
            output_adapter = ut.out_adapt,
            shape = cg.dim,
            input_channels = 1,
            output_channels = cg.num_classes,),
            verbose = 1,
            steps = 1,)

        # save u_net segmentation
        if task_list[task_num] == 's':
          u_gt_nii = nb.load(img)
          u_pred = np.argmax(u_pred[0], axis = -1).astype(np.uint8)
          u_pred = dv.crop_or_pad(u_pred, u_gt_nii.get_data().shape)
          u_pred[u_pred == 3] = 4
          u_pred = nb.Nifti1Image(u_pred, u_gt_nii.affine)
          save_path = os.path.join(cg.save_dir,patient_class,patient_id,'seg-pred/batch_'+str(batch),'pred_'+task_list[task_num]+'_'+os.path.basename(img))
          ff.make_folder([os.path.join(cg.save_dir,patient_class), os.path.join(cg.save_dir,patient_class,patient_id),os.path.join(cg.save_dir,patient_class,patient_id,'seg-pred'), os.path.join(cg.save_dir,patient_class,patient_id,'seg-pred/batch_'+str(batch))])
          nb.save(u_pred, save_path)
      
      # save vectors
        if task_list[task_num] != 's':
          x_n = ff.normalize(x_pred)
          y_n = ff.normalize(y_pred)
          matrix = np.concatenate((t_pred.reshape(1,3),x_n.reshape(1,3),y_n.reshape(1,3)))
          save_path = os.path.join(cg.save_dir,patient_class,patient_id,'vector-pred/batch_'+str(batch),'pred_'+task_list[task_num])
          ff.make_folder([os.path.join(cg.save_dir,patient_class), os.path.join(cg.save_dir,patient_class,patient_id),os.path.join(cg.save_dir,patient_class,patient_id,'vector-pred'), os.path.join(cg.save_dir,patient_class,patient_id,'vector-pred/batch_'+str(batch))])
          np.save(save_path,matrix)
