#!/usr/bin/env python
# Python libraries
import os
import numpy as np
import nibabel as nb
import function_list as ff
import segcnn
from segcnn.generator import ImageDataGenerator
import segcnn.utils as ut
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
import dvpy as dv
import dvpy.tf
cg = segcnn.Experiment()

########
# define the prediction task
task_list = ['seg','2C-r','2C-t','3C-r','3C-t','4C-r','4C-t','BASAL-r','BASAL-t'] 
task_num_list = list(range(0,9)) # select the task 

#########
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

###########
# define patient CT image list
img_list = ff.find_all_target_files(['ucsd_*/*/img-nii-sm/*.nii.gz'],cg.patient_dir)
print('finish loading all patient images')

##########
# define the generator
valgen = dv.tf.ImageDataGenerator(3,input_layer_names=['input_1'],output_layer_names=['unet','t','x','y'],)

#########
# predict per patient
for task_num in task_num_list:
  print('current task is: ', task_list[task_num])
  ##### load saved weight
  model_file = os.path.join(cg.model_dir,'model-'+task_list[task_num]+'.hdf5')
  model.load_weights(model_file,by_name = True)
  print('finish loading saved weights: ',model_file)

  # predict
  for img in img_list:
    patient_id = os.path.basename(os.path.dirname(os.path.dirname(img)))
    patient_class = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(img))))
    time_frame = ff.find_timeframe(img,2)
    print(patient_class,patient_id,time_frame,'\n')

    # build the predict_generator
    u_pred,t_pred,x_pred,y_pred= model.predict_generator(valgen.predict_flow(np.asarray([img]),
        batch_size = cg.batch_size,
        input_adapter = ut.in_adapt,
        output_adapter = ut.out_adapt,
        shape = cg.dim,
        input_channels = 1,
        output_channels = cg.num_classes,),
        verbose = 1,
        steps = 1,)

    # save u_net segmentation
    if task_num == 0:
      u_gt_nii = nb.load(img)
      u_pred = np.argmax(u_pred[0], axis = -1).astype(np.uint8)
      u_pred = dv.crop_or_pad(u_pred, u_gt_nii.get_data().shape)
      u_pred = nb.Nifti1Image(u_pred, u_gt_nii.affine)
      save_dir = os.path.join(cg.patient_dir,patient_class,patient_id,'seg-pred')
      os.makedirs(save_dir,exist_ok = True)
      save_path = os.path.join(save_dir,'seg_'+os.path.basename(img))
      nb.save(u_pred, save_path)
  
  # save vectors
    if task_num != 0:
      x_n = ff.normalize(x_pred)
      y_n = ff.normalize(y_pred)
      matrix = np.concatenate((t_pred.reshape(1,3),x_n.reshape(1,3),y_n.reshape(1,3)))
      save_dir=os.path.join(cg.patient_dir,patient_class,patient_id,'vectors-pred')
      os.makedirs(save_dir, exist_ok = True)
      if time_frame == 0:
        save_path = os.path.join(save_dir,task_list[task_num])
        np.save(save_path,matrix)
  
  
  

  
