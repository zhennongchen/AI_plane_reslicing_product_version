# System
import os

class Experiment():

  def __init__(self):
    # main directory
    self.main_dir = os.environ['CG_MAIN_DIR']

    # raw data (not resampled image)
    self.raw_dir = os.environ['CG_RAW_DIR']

    # input data (patient directory).
    self.patient_dir = os.environ['CG_PATIENT_DIR']

    # model 
    self.model_dir = os.environ['CG_MODEL_DIR']

  
    # Dimension of padded input, for training.
    self.dim = (int(os.environ['CG_CROP_X']), int(os.environ['CG_CROP_Y']), int(os.environ['CG_CROP_Z']))
  
    # Seed for randomization.
    self.seed = int(os.environ['CG_SEED'])
  
    # Number of Classes (Including Background)
    self.num_classes = int(os.environ['CG_NUM_CLASSES'])

    # pixel dimension in mm (resampled image)
    self.pixel_size = float(os.environ['CG_RESAMPLE_SIZE'])

    # slice thickness in SAX stack
    self.slice_thickness = int(os.environ['CG_SAX_STACK_THICKNESS'])
  
    # UNet Depth
    self.unet_depth = 5
  
    # Depth of convolutional feature maps
    self.conv_depth_multiplier = int(os.environ['CG_CONV_DEPTH_MULTIPLIER'])
    self.conv_depth = [16, 32, 64, 128, 256, 256, 128, 64, 32, 16, 16]
    self.conv_depth = [self.conv_depth_multiplier*x for x in self.conv_depth]
  
    assert(len(self.conv_depth) == (2*self.unet_depth+1))
  
    # How many images should be processed in each batch?
    self.batch_size = int(os.environ['CG_BATCH_SIZE'])
  
    # Translation Range
    self.xy_range = float(os.environ['CG_XY_RANGE'])
  
    # Scale Range
    self.zm_range = float(os.environ['CG_ZM_RANGE'])

    # Rotation Range
    self.rt_range=float(os.environ['CG_RT_RANGE'])
  
    # Should Flip
    self.flip = False


